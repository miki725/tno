#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import argparse
import getpass
import os
import subprocess


ENV_VAR = 'PROTECTION_PASSWORD'
PROTECTED = '.protected'
FILES = (
    'prod.env{}',
)

parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--decrypt',
    action='store_true',
    default=False,
)


class IncorrectPassword(Exception):
    pass


if __name__ == '__main__':
    args = parser.parse_args()

    password = getpass.getpass()
    os.environ[ENV_VAR] = password

    encrypting = 'Decrypting' if args.decrypt else 'Encrypting'

    try:
        for f in FILES:
            if args.decrypt:
                source = f.format(PROTECTED)
                destination = f.format('')
            else:
                source = f.format('')
                destination = f.format(PROTECTED)

            if not os.path.exists(source):
                raise Exception('{} not found'.format(source))

            print('{} file {}'.format(encrypting, source))

            cmd = filter(None, [
                'openssl',
                'aes-256-cbc',
                '-base64',
                '-salt',
                '-d' if args.decrypt else None,
                '-pass',
                'env:{}'.format(ENV_VAR),
                '-in',
                source,
                '-out',
                destination,
            ])

            try:
                subprocess.check_output(cmd)
            except subprocess.CalledProcessError:
                raise IncorrectPassword('Incorrect password')

    except Exception as e:
        parser.error(str(e))

    finally:
        del os.environ[ENV_VAR]
