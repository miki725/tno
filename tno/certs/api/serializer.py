from rest_framework import serializers

from ..models import Certificate, Site
from ..utils import underscorize


class UnderscoreDictField(serializers.DictField):
    def to_representation(self, value):
        value = super(UnderscoreDictField, self).to_representation(value)
        return {
            underscorize(k): v for k, v in value.items()
        }


class CertificateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        'api:certificates-detail',
        label='URL',
        lookup_field='fingerprint_sha2',
        lookup_url_kwarg='fingerprint_sha2',
        read_only=True,
    )
    text_url = serializers.HyperlinkedIdentityField(
        'api:certificates-text',
        label='text',
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
            'text_url',
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


class CertificateNestedSerializer(CertificateSerializer):
    trust_certificate = CertificateSerializer(read_only=True)
    issuer_certificate = CertificateSerializer(read_only=True)

    class Meta(CertificateSerializer.Meta):
        fields = CertificateSerializer.Meta.fields + [
            'trust_certificate',
            'issuer_certificate',
        ]
        read_only_fields = list(set(fields) - set(CertificateSerializer.Meta.writable_fields))


class SiteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        'api:sites-detail',
        label='URL',
        lookup_field='host',
        lookup_url_kwarg='host',
        read_only=True,
    )
    # as per RFC 1034 max length for netloc is
    # 255 bytes - 2 bytes (length + trailing dot) = 253 bytes
    host = serializers.CharField(max_length=253, read_only=True)
    # only support 443 port for now which will only support
    # standard https sites served under 443
    port = serializers.IntegerField(min_value=443, max_value=443, read_only=True)
    certificate = CertificateNestedSerializer(read_only=True)

    class Meta(object):
        model = Site
        writable_fields = []
        fields = [
            'url',
            'host',
            'port',
            'certificate',
        ]
        read_only_fields = list(set(fields) - set(writable_fields))

    def __init__(self, *args, **kwargs):
        writable_fields = kwargs.pop('writable_fields', [])
        super(SiteSerializer, self).__init__(*args, **kwargs)

        for f in writable_fields:
            self.fields[f].read_only = False

    def create(self, validated_data):
        return Site.objects.create_with_certificate(**validated_data)
