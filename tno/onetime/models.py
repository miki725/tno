# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from base64 import b64decode, b64encode
from uuid import uuid4

import six
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django_auxilium.models import UUIDModel

from .conf import EXPIRES_IN_DAYS
from .crypto import decrypt, derive_key, encrypt
from .utils import get_entropy


class OTSecretQuerySet(models.QuerySet):
    def expired(self):
        return self.filter(expires__lte=now())


class OTSecretManager(models.Manager):
    def encrypt(self, password, secret):
        entropy = get_entropy(80)

        iv = entropy[:32]
        salt = entropy[32:64]
        associated_data = entropy[64:]

        key = derive_key(password, salt)

        ciphertext, tag = encrypt(iv, key, associated_data, secret)

        return self.create(
            iv=iv,
            salt=salt,
            associated_data=associated_data,
            tag=tag,
            ciphertext=b64encode(ciphertext)
        )


@python_2_unicode_compatible
class OTSecret(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='one_time_secrets',
                             null=True, blank=True)

    uuid = models.CharField(max_length=32, editable=False, blank=True,
                            unique=True, db_index=True)

    salt = models.BinaryField(max_length=32)
    iv = models.BinaryField(max_length=32)
    associated_data = models.BinaryField(max_length=16)
    tag = models.BinaryField(max_length=16)
    ciphertext = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()

    objects = OTSecretManager.from_queryset(OTSecretQuerySet)()

    class Meta(object):
        verbose_name = 'One Time Secret'

    def generate_uuid(self, force=False):
        if not self.uuid or force:
            self.uuid = uuid4().get_hex()

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.generate_uuid()
        if not self.expires:
            self.expires = now() + relativedelta(days=EXPIRES_IN_DAYS)

        return super(OTSecret, self).save(*args, **kwargs)

    def decrypt(self, password):
        key = derive_key(password, six.binary_type(self.salt))

        return decrypt(six.binary_type(self.iv),
                       key,
                       six.binary_type(self.associated_data),
                       six.binary_type(self.tag),
                       b64decode(self.ciphertext))

    def __str__(self):
        return '{} expiring {}'.format(self.uuid, self.expires)
