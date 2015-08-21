# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals


def len_base64(n_bytes):
    """
    Calculate the length of base64 string given specified number of bytes.
    """
    return ((n_bytes - 1) // 3) * 4 + 4


def get_entropy(length):
    """
    Get good-quality entropy from /dev/random
    """
    with open('/dev/random', 'rb') as fid:
        return fid.read(length)
