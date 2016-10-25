from typing import Union

from django.core.exceptions import ObjectDoesNotExist


class NoIssuerCertificateFound(ObjectDoesNotExist):
    def __init__(self, subject: dict, issuer: Union[None, dict]=None):
        self.subject = subject
        self.issuer = issuer


class NoRootCertificateFound(NoIssuerCertificateFound):
    pass


class NoTrustCertificateFound(NoIssuerCertificateFound):
    pass


class UnsupportedPublicKeyType(Exception):
    pass


class InvalidCertificate(Exception):
    def __init__(self, server: str, reason: str, certificates=None):
        super(InvalidCertificate, self).__init__()
        self.server = server
        self.reason = reason
        self.certificates = certificates

    def __str__(self) -> str:
        return '{} is invalid due to "{}"'.format(self.server, self.reason)
