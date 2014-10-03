# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import base64

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.viewsets import GenericViewSet, ViewSet

from ..models import OTSecret
from ..utils import get_entropy
from .serializers import OTSecretSerializer


class EntropyViewSet(ViewSet):
    """
    API endpoint to generate requested (at most 1024) number of bytes
    of entropy which can be used by the client to combine server entropy
    with client entropy to increase overall randomness quality.

    Currently the random data is encoded using standard "base64"
    encoding (not url-safe) for better support.
    """
    http_method_names = ('get', 'head',)
    lookup_field = 'bytes'
    lookup_value_regex = r'[\d]+'

    def retrieve(self, request, *args, **kwargs):
        length = min(int(kwargs['bytes']), 1024)
        entropy = get_entropy(length)
        data = {
            'entropy': base64.b64encode(entropy),
            'format': 'base64',
            'bytes': length,
        }
        return Response(data)

    def list(self, request, *args, **kwargs):
        data = {
            'entropy': reverse(
                request.resolver_match.url_name.replace('list', 'detail'),
                kwargs={
                    'bytes': 123,
                },
                request=request,
                format=kwargs.get('format', None)
            ).replace('123', ':bytes')
        }
        return Response(data, status=HTTP_405_METHOD_NOT_ALLOWED)


class OneTimeSecretViewSet(CreateModelMixin,
                           RetrieveModelMixin,
                           GenericViewSet):
    """
    API endpoint for interacting with one-time-secrets.
    Currently the following methods are allowed:

    * `OPTIONS /` - get metadata about the endpoint
      which also describes all serialized fields
    * `POST /` - factory endpoint to create new one-time-secrets
    * `GET /<uuid>/` - retrieve one-time-secret by its uuid

    **Note**: by the very definition of one-time-secret (OTS),
    the secret can only be accessed one time - meaning
    as soon as the OTS is retrieved by the API via `GET /<uuid>/`,
    it is automatically deleted hence `DELETE` HTTP verb
    is not explicitly allowed. Alternatively each OTS is
    automatically deleted after it expires.

    ## Encryption

    Here are cryptographic primitives used:

    * `AES256` cipher
    * `GCM AES` block mode
    * `PBKDF2` key derivation using `SHA256` `HMAC` with 30000 iterations

    Due to the nature of "Trust No One", all encryption happens on
    the client and only ciphertext is sent to the server. In addition
    to ciphertext, only required encryption metadata is sent to the server
    for storage however server has no technical capability to decrypt
    secret message.

    ## encryption scheme breakdown:

    1. Since browsers and js are not famous for their entropy sources,
       client requests server for some additional randomness entropy
       (to be specific 80 bytes or 640 bits).

    2. Client generates 640 bytes (or 640 bits) of its own entropy.

    3. Client `XOR`s server and client entropy to increase randomness
       sample quality.

    4. Randomness sample is divided into the following blocks which
       will be used in operations to follow:

        * 32 bytes (256 bits) for `IV` (Initialization vector)
        * 32 bytes (256 bits) for `SALT` to salt user password
        * 16 bytes (128 bits) for `ADATA` (associated data) which will be used
          in `AES-GCM` for message authentication instead of `HMAC`
          (`GCM` has message encryption and authentication baked
          into single algorithm)

    5. Client calculates the AES `KEY` by using `PBKDF2` key derivation
       function with `pass` (user-supplied password) (which should be
       of good quality by its own so no "monkey"s are allowed).
       `PBKDF2` is used with `HMAC` `SHA256` with 30000 iterations.
       30000 iterations were chosen because they seem to provide
       excellent security with reasonable performance on both desktop
       and mobile (couple of seconds).
       `PBKDF2` was primarily chosen because it has much wider
       support in JS browser-compatible libraries and has much
       better performance on mobile devices unlike `scrypt`
       (although we might switch to `scrypt` in the future).

    6. Client encrypts secret message plaintext by using:
       `AES256-GCM(message, IV, KEY, ADATA)`. That in turn produces
       `ciphertext` and `tag`. `ciphertext` is obviously the encrypted
       secret message and `tag` is the result of `GCM` message
       authentication. It can be used by the client when ciphertext
       needs to be decrypted to verify the validity of the password.

    7. Finally, information listed below is sent to the server.
       Please note that `pass` is not sent to the server. However because
       it must of good quality and is required to compute the encryption
       key, the server will not have the capability to decrypt ciphertext
       after the fact without doing brute-force attack on ciphertext.

        * `IV`
        * `SALT`
        * `ADATA`
        * `tag`
        * `ciphertext`

    8. When client needs to decrypt data back, it retrieves all the
       necessary information from the server and tries to decrypt
       the ciphertext by using user-supplied password. It then uses
       `tag` generated during encryption to verify password.
    """
    lookup_field = 'uuid'
    # uuid is stored as hex value
    lookup_value_regex = r'[a-f0-9]{32}'

    model = OTSecret
    serializer_class = OTSecretSerializer

    def get_object(self, queryset=None):
        obj = super(OneTimeSecretViewSet, self).get_object(queryset)
        pk = obj.pk
        # delete object when being accessed
        obj.delete()
        # restore pk in case will be used somewhere
        obj.pk = pk
        return obj

    def pre_save(self, obj):
        super(OneTimeSecretViewSet, self).pre_save(obj)

        if self.request.user.is_authenticated():
            obj.user = self.request.user
