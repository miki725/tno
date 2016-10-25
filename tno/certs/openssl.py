import os
import re
import subprocess
import typing

import certifi

from .constants import CERT_PATTERN
from .exceptions import InvalidCertificate


VALIDATION_OK_PATTERN = re.compile(
    rb'^Verification: OK$',
    re.MULTILINE
)
VALIDATION_ERROR_PATTERN = re.compile(
    rb'^Verification error: (?P<reason>.*)$',
    re.MULTILINE
)


def x509_from_server(host: str, port: int = 443) -> typing.List[bytes]:
    cmd = (
        'env openssl s_client '
        '-showcerts '
        '-CAfile {ca_file} '
        '-servername {host} '
        '-verify_hostname {host} '
        '-connect {host}:{port}'
    ).format(ca_file=certifi.where(), host=host, port=port)

    with open(os.devnull, 'rb') as devnull:
        args = cmd.split(' ')
        output = subprocess.check_output(args, stdin=devnull, stderr=subprocess.PIPE)

    if not VALIDATION_OK_PATTERN.search(output):
        reason = VALIDATION_ERROR_PATTERN.search(output).groupdict()['reason'].decode('utf-8')
        raise InvalidCertificate(host, reason)

    return CERT_PATTERN.findall(output)


def x509_text_from_x509(x509: bytes) -> str:
    cmd = (
        'openssl '
        'x509 '
        '-in - '
        '-text'
        # '-noout'
    )

    p = subprocess.Popen(
        cmd.split(' '),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = p.communicate(x509)
    return stdout.decode('utf-8')
