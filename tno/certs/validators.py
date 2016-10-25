# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class HostOnlyValidator(object):
    message = _('Enter only a host value.')
    code = 'host_only'

    def __call__(self, value):
        parsed = urlparse(value)

        if any([parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment]):
            raise ValidationError(self.message, code=self.code)


class PortValidator(object):
    messages = {
        'port_required': _('Port is required.'),
        'invalid_port': _('Port %(port)s is not allowed.'),
    }

    code = 'invalid_port'
    scheme_port_mapping = {
        'http': 80,
        'https': 443,
    }

    def __init__(self, allowed_port: int, must_be_explicit: bool = False):
        self.allowed_port = allowed_port
        self.must_be_explicit = must_be_explicit

    def __call__(self, value):
        parsed = urlparse(value)

        given_port = parsed.port
        if not given_port:
            if self.must_be_explicit:
                raise ValidationError(self.messages['port_required'], code=self.code)
            given_port = self.scheme_port_mapping.get(parsed.scheme, given_port)

        if given_port != self.allowed_port:
            raise ValidationError(self.messages['invalid_port'], code=self.code, params={'port': given_port})
