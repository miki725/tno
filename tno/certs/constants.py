import re


CERT_PATTERN = re.compile(
    rb'-+BEGIN CERTIFICATE-'
    rb'+[A-Za-z0-9/+=\n]+'
    rb'-+END CERTIFICATE-+\n',
    re.MULTILINE,
)
