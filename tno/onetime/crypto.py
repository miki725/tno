# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import six
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .conf import PBKDF2_ITERATIONS


def derive_key(password, salt):
    assert isinstance(password, six.text_type)
    assert isinstance(salt, six.binary_type)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))


def encrypt(iv, key, associated_data, plaintext):
    assert isinstance(plaintext, six.text_type)
    assert isinstance(iv, six.binary_type)
    assert isinstance(key, six.binary_type)
    assert isinstance(associated_data, six.binary_type)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend(),
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = (encryptor.update(plaintext.encode('utf-8')) +
                  encryptor.finalize())

    return ciphertext, encryptor.tag


def decrypt(iv, key, associated_data, tag, ciphertext):
    assert isinstance(iv, six.binary_type)
    assert isinstance(key, six.binary_type)
    assert isinstance(associated_data, six.binary_type)
    assert isinstance(tag, six.binary_type)

    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return (decryptor.update(ciphertext) +
            decryptor.finalize()).decode('utf-8')
