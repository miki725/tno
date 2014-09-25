from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_auxilium.models import UUIDModel


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

    class Meta(object):
        verbose_name = 'One Time Secret'

    def generate_uuid(self, force=False):
        if not self.uuid or force:
            self.uuid = uuid4().get_hex()

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.generate_uuid()

        return super(OTSecret, self).save(*args, **kwargs)

    def __str__(self):
        return '{} expiring {}'.format(self.uuid, self.expires)
