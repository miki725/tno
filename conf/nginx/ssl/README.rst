Private Key
-----------

Private key if stored in VCS should be encrypted.
If so, to decrypt::

    $ openssl rsa -in tno.io.prv.key -out tno.io.key

SSL Chain
---------

SSL Chain contains the end certificate plus intermediate cert.
There is no need to include root cert since it should be already
in client trust chains::

    $ cat tno.io.crt intermediate2.crt intermediate1.crt > tno.io.sslchain.crt

Trust Chain
-----------

Trust Chain is used for nginx to enable OCSP Stapling hence it
needs to have a chain of certs to verify client cert.
Therefore end certificate is not included however root
and intermediate certs are required::

    $ cat root.crt intermediate1.crt intermediate2.crt > tno.io.trustchain.crt
