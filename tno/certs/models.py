import typing
import uuid
from binascii import hexlify
from fnmatch import fnmatch

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPublicKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.x509 import (
    DNSName,
    ExtensionNotFound,
    ExtensionOID,
    NameOID,
    load_pem_x509_certificate,
)
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_auxilium.models import CreatedModel
from django_auxilium.utils.functools.cache import cache_property

from .exceptions import NoIssuerCertificateFound, UnsupportedPublicKeyType
from .openssl import x509_from_server
from .utils import get_attribute_from_x509_by_oid, get_json_from_x509_name


class CertificateManager(models.Manager):
    def get_or_create_by_fingerprint(self, cert: 'Certificate') -> typing.Tuple['Certificate', bool]:
        try:
            return self.get(fingerprint_sha2=cert.fingerprint_sha2), False
        except self.model.DoesNotExist:
            cert.save()
            return cert, True


class CertificateQuerySet(models.QuerySet):
    def get_by_subject(self, subject: dict, *, default=None) -> 'Certificate':
        return self.get(subject__contains=subject)


class Certificate(models.Model):
    KEY_TYPE_CHOICES = [
        ('RSA', 'RSA'),
        ('DSA', 'DSA'),
        ('EC', 'Elliptic Curve'),
    ]
    KEY_TYPE_MAPPING = {
        RSAPublicKey: 'RSA',
        DSAPublicKey: 'DSA',
        EllipticCurvePublicKey: 'EC',
    }

    x509 = models.TextField()

    # information extracted from x509 cert but is useful to be stored
    # in separate columns for better searching
    subject = JSONField()
    serial_number = models.CharField(max_length=256)
    valid_not_before = models.DateTimeField()
    valid_not_after = models.DateTimeField()
    key_type = models.CharField(max_length=3, choices=KEY_TYPE_CHOICES)
    key_size = models.PositiveIntegerField(null=True, blank=True)

    # other metadata about the cert which is inferred from x509
    # but is useful to be stored in DB for reference
    fingerprint_sha2 = models.CharField('Fingerprint SHA256', max_length=64, unique=True, db_index=True)

    # this is required here and we cant simply infer that information
    # by the lack of trust_certificate because not all root
    # certs should be trusted. Sometimes intermediate certs are directly
    # added to the trust store hence root cert itself will not be found
    # but the child certificate should still be marked as non-root
    # hence this flag
    is_root = models.BooleanField(default=False)
    # this is required for similar reasons. since some non-root certs
    # are in trust store, we need to indicate that somehow.
    # in addition, since the model can store other non-trusted roots
    # this is useful to see which certs are in standard trust stores
    # (we currently use mozilla trust store here)
    is_trusted = models.BooleanField(default=False)

    # relations
    trust_certificate = models.ForeignKey(
        'Certificate',
        related_name='leaf_certificates',
        null=True,
        blank=True,
        help_text=''
    )
    issuer_certificate = models.ForeignKey(
        'Certificate',
        related_name='children_certificates',
        null=True,
        blank=True,
    )

    objects = CertificateManager.from_queryset(CertificateQuerySet)()

    def __str__(self) -> str:
        return self.common_name or self.organization

    @property
    def actual_trust_certificate(self):
        return self if self.is_trusted else self.trust_certificate

    @property
    def common_name(self) -> str:
        return self.subject.get(NameOID.COMMON_NAME._name)

    @property
    def organization(self) -> str:
        return self.subject.get(NameOID.ORGANIZATION_NAME._name)

    @property
    def country(self) -> str:
        return self.subject.get(NameOID.COUNTRY_NAME._name)

    @cache_property
    def as_x509(self):
        return load_pem_x509_certificate(self.x509.encode('ascii'), default_backend())

    def is_for_host(self, host: str) -> bool:
        host_lower = host.lower()

        common_name = get_attribute_from_x509_by_oid(self.as_x509.subject, NameOID.COMMON_NAME)
        if fnmatch(host_lower, common_name.lower()):
            return True

        try:
            san = self.as_x509.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        except ExtensionNotFound:
            return False
        else:
            values = san.value.get_values_for_type(DNSName)
            return any(fnmatch(host_lower, i.lower()) for i in values)

    @classmethod
    def from_x509(cls, pem_data: bytes, is_trusted: bool = False, find_parents: bool = True) -> 'Certificate':
        raw = load_pem_x509_certificate(pem_data, default_backend())

        subject = get_json_from_x509_name(raw.subject)
        issuer = get_json_from_x509_name(raw.issuer)

        is_root = raw.issuer == raw.subject
        issuer_certificate = None
        trust_certificate = None

        if not is_root and find_parents:
            try:
                issuer_certificate = cls.objects.get_by_subject(issuer)
            except cls.DoesNotExist:
                # if cert by itself is trusted, its root is not required
                # to be in trust store so we might never find it
                # so exception should not be raised
                if not is_trusted:
                    raise NoIssuerCertificateFound(
                        subject=subject,
                        issuer=issuer,
                    )
            else:
                trust_certificate = issuer_certificate.actual_trust_certificate

                assert trust_certificate

        public_key = raw.public_key()
        public_key_type = None

        for klass, v in cls.KEY_TYPE_MAPPING.items():
            if isinstance(public_key, klass):
                public_key_type = v
                break

        if not public_key_type:
            raise UnsupportedPublicKeyType(type(public_key))

        cert = cls(
            x509=pem_data.decode('ascii'),

            subject=subject,
            valid_not_before=raw.not_valid_before,
            valid_not_after=raw.not_valid_after,

            serial_number=str(raw.serial_number),
            key_type=public_key_type,
            key_size=getattr(public_key, 'key_size', None),

            fingerprint_sha2=hexlify(raw.fingerprint(hashes.SHA256())).decode('ascii'),

            is_root=is_root,
            is_trusted=is_trusted,
            trust_certificate=trust_certificate,
            issuer_certificate=issuer_certificate,
        )
        cert.as_x509 = raw
        return cert

    @staticmethod
    def find_leaf_cert_from_certs(certs: typing.Iterable['Certificate'], host: str) -> 'Certificate':
        return next(
            (c for c in certs if c.is_for_host(host)),
            None
        )


class SiteManager(models.Manager):
    def get_or_create_with_certificate(self, host: str, port: int, **kwargs) -> typing.Tuple['Site', bool]:
        try:
            return self.get(host=host), False
        except self.model.DoesNotExist:
            return self.create_with_certificate(host=host, port=port, **kwargs), True

    def create_with_certificate(self, host: str, port: int, **kwargs) -> 'Site':
        certificates = [
            Certificate.from_x509(c, find_parents=False)
            for c in x509_from_server(host, port)
        ]
        certificates_mapping = {
            c.as_x509.subject: c
            for c in certificates
        }

        child_certificate = Certificate.find_leaf_cert_from_certs(certificates, host)
        chain_certificates = [child_certificate]

        assert child_certificate, 'leaf certificate was not found'

        while True:
            try:
                parent_certificate = Certificate.objects.get_by_subject(
                    get_json_from_x509_name(child_certificate.as_x509.issuer)
                )

            except Certificate.DoesNotExist:
                parent_certificate = certificates_mapping.pop(child_certificate.as_x509.issuer)

            else:
                break

            finally:
                chain_certificates.append(parent_certificate)
                child_certificate = parent_certificate

        for i, (parent, child) in enumerate(reversed(list(zip(chain_certificates[1:], chain_certificates[0:])))):
            # already saved. move on
            if child.pk:
                continue

            child.issuer_certificate = parent
            child.trust_certificate = parent.actual_trust_certificate

            chain_certificates[i] = Certificate.objects.get_or_create_by_fingerprint(child)[0]

        return self.create(host=host, port=port, certificate=chain_certificates[0], **kwargs)


class Site(CreatedModel):
    host = models.CharField(max_length=256, unique=True, db_index=True)
    certificate = models.ForeignKey(Certificate, related_name='sites')

    objects = SiteManager()

    def update_certificate(self, commit: bool=True) -> None:
        certificate = None
        for x509_data in reversed(x509_from_server(self.host, 443)):
            certificate = self.get_or_create_by_fingerprint(Certificate.from_x509(x509_data))
        assert certificate

        self.certificate = certificate

        if commit:
            self.save(update_fields=['certificate'])

    def __str__(self) -> str:
        return self.host


class SiteCollection(CreatedModel):
    uuid = models.UUIDField(
        editable=False,
        unique=True,
        db_index=True,
        default=uuid.uuid4,
    )
    name = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='site_collections', blank=True, null=True)
    sites = models.ManyToManyField(Site, related_name='site_collections', blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def uuid_hex(self):
        try:
            return self.uuid.hex
        except AttributeError:
            return None
