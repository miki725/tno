from rest_framework import renderers
from rest_framework.serializers import ListSerializer, Serializer

from ..openssl import x509_text_from_x509


class CertificatePEMRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'pem'

    @staticmethod
    def render_underscore_key_abbreviation(key: str) -> str:
        return ''.join(i[0].upper() for i in key.split('_'))

    @staticmethod
    def get_label_from_serializer(serializer: Serializer, key: str) -> str:
        if isinstance(serializer, ListSerializer):
            serializer = serializer.child

        try:
            return serializer.fields[key].label
        except KeyError:
            return key

    def render_value(self, value) -> str:
        if isinstance(value, dict):
            return ' '.join(
                '{}={}'.format(self.render_underscore_key_abbreviation(k), v)
                for k, v in sorted(value.items())
            )
        else:
            return value

    def render_data(self, data: dict, serializer: Serializer, exclude: list = None) -> str:
        exclude = exclude or []
        return '\n'.join(
            '# {}: {}'.format(self.get_label_from_serializer(serializer, key), self.render_value(value))
            for key, value in data.items()
            if key not in exclude
        )

    def render_certificate(self, cert: dict, context: dict, serializer: Serializer) -> bytes:
        exclude = [
            'x509',
            'trust_certificate',
            'issuer_certificate',
        ]
        return (
            '{data}\n'
            '{x509}'
            ''.format(data=self.render_data(cert, serializer, exclude=exclude),
                      x509=cert['x509'])
        ).encode('utf-8')

    def render_certificates(self, certs: dict, context: dict, serializer: Serializer) -> bytes:
        header = self.render_data(
            {'URL': context['request'].build_absolute_uri()},
            serializer,
        )
        header += '\n'
        header += self.render_data(
            certs,
            serializer,
            exclude=['results'],
        )

        return b'\n\n'.join(
            [header.encode('utf-8')] +
            [self.render_certificate(i, context, serializer) for i in certs['results']]
        )

    def render(self, data, media_type=None, renderer_context=None):
        if 'results' in data:
            return self.render_certificates(data, renderer_context, data['results'].serializer)
        else:
            return self.render_certificate(data, renderer_context, data.serializer)


class CertificateOpenSSLTextRenderer(renderers.BaseRenderer):
    media_type = 'text/x-openssl-x509'
    format = 'x509'

    @staticmethod
    def render_certificate(cert: dict) -> bytes:
        return x509_text_from_x509(cert['x509'].encode('utf-8')).encode('utf-8')

    def render_certificates(self, data: dict) -> bytes:
        return b'\n\n'.join(self.render_certificate(i) for i in data['results'])

    def render(self, data, media_type=None, renderer_context=None):
        if 'results' in data:
            return self.render_certificates(data)
        else:
            return self.render_certificate(data)
