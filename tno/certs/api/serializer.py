from rest_framework import serializers

from user.api.serializers import UserSerializer

from ..models import Certificate, Site, SiteCollection
from ..utils import underscorize


class UnderscoreDictField(serializers.DictField):
    def to_representation(self, value):
        value = super(UnderscoreDictField, self).to_representation(value)
        return {
            underscorize(k): v for k, v in value.items()
        }


class CertificateBaseSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        'api:certificates-detail',
        label='URL',
        lookup_field='fingerprint_sha2',
        lookup_url_kwarg='fingerprint_sha2',
        read_only=True,
    )
    subject = UnderscoreDictField(read_only=True)

    class Meta(object):
        model = Certificate
        writable_fields = [
            'x509',
        ]
        fields = [
            'url',
            'x509',
            'subject',
            'serial_number',
            'valid_not_before',
            'valid_not_after',
            'key_type',
            'key_size',
            'fingerprint_sha2',
            'is_root',
            'is_trusted',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))


class CertificateSerializer(CertificateBaseSerializer):
    trust_certificate_url = serializers.HyperlinkedRelatedField(
        'api:certificates-detail',
        source='trust_certificate',
        label='Trust Certificate URL',
        lookup_field='fingerprint_sha2',
        lookup_url_kwarg='fingerprint_sha2',
        read_only=True,
    )
    issuer_certificate_url = serializers.HyperlinkedRelatedField(
        'api:certificates-detail',
        source='issuer_certificate',
        label='Issuer Certificate URL',
        lookup_field='fingerprint_sha2',
        lookup_url_kwarg='fingerprint_sha2',
        read_only=True,
    )

    class Meta(CertificateBaseSerializer.Meta):
        writable_fields = CertificateBaseSerializer.Meta.writable_fields
        fields = CertificateBaseSerializer.Meta.fields + [
            'trust_certificate_url',
            'issuer_certificate_url',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))


class CertificateNestedSerializer(CertificateBaseSerializer):
    trust_certificate = CertificateSerializer(read_only=True)
    issuer_certificate = CertificateSerializer(read_only=True)

    class Meta(CertificateBaseSerializer.Meta):
        writable_fields = CertificateBaseSerializer.Meta.writable_fields
        fields = CertificateBaseSerializer.Meta.fields + [
            'trust_certificate',
            'issuer_certificate',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))


class SiteBaseSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        'api:sites-detail',
        label='URL',
        lookup_field='host',
        lookup_url_kwarg='host',
        read_only=True,
    )
    # as per RFC 1034 max length for netloc is
    # 255 bytes - 2 bytes (length + trailing dot) = 253 bytes
    # TODO correctly validate host
    host = serializers.CharField(max_length=253, read_only=True)
    # only support 443 port for now which will only support
    # standard https sites served under 443
    port = serializers.IntegerField(min_value=443, max_value=443, read_only=True)

    class Meta(object):
        model = Site
        writable_fields = []
        fields = [
            'url',
            'host',
            'port',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))

    def __init__(self, *args, **kwargs):
        writable_fields = kwargs.pop('writable_fields', [])
        super(SiteBaseSerializer, self).__init__(*args, **kwargs)

        for f in writable_fields:
            self.fields[f].read_only = False

    def create(self, validated_data):
        return Site.objects.create_with_certificate(**validated_data)


class SiteSerializer(SiteBaseSerializer):
    certificate_url = serializers.HyperlinkedRelatedField(
        'api:certificates-detail',
        source='certificate',
        label='Certificate URL',
        lookup_field='fingerprint_sha2',
        lookup_url_kwarg='fingerprint_sha2',
        read_only=True,
    )

    class Meta(SiteBaseSerializer.Meta):
        writable_fields = SiteBaseSerializer.Meta.writable_fields
        fields = SiteBaseSerializer.Meta.fields + [
            'certificate_url',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))


class SiteNestedSerializer(SiteBaseSerializer):
    certificate = CertificateNestedSerializer(read_only=True)

    class Meta(SiteBaseSerializer.Meta):
        writable_fields = SiteBaseSerializer.Meta.fields
        fields = SiteBaseSerializer.Meta.fields + [
            'certificate',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))


class SiteCollectionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        'api:site-collections-detail',
        label='URL',
        read_only=True,
    )
    owner = UserSerializer(read_only=True)
    sites = SiteSerializer(many=True, read_only=True)

    class Meta(object):
        model = SiteCollection
        writable_fields = [
            'name',
            'description',
        ]
        fields = [
            'url',
            'name',
            'description',
            'owner',
            'sites',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))
