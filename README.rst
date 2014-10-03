Trust No One
============

* GitHub - https://github.com/miki725/tno
* Site - https://tno.io

TNO which stands for Trust No One is a project which implements
a set of web tools all following TNO cryptography principle.
TNO principle is an application approach where no sensitive
user information is stored on the server. Instead all information
is encrypted in the "client" (e.g. web browser) and only the
ciphertext is sent to the server for storage. As a result,
since the server does not store the decryption key or any
information to derive the decryption key, it is unable to
read the stored data.

This repository contains source code for the https://tno.io site.

Services
--------

Currently TNO.io provides the following services:

* **One Time Secrets** - A way to share secrets which
  self-destruct after they are viewed. This is perfect
  for sending passwords in emails instead of sending
  actual passwords via inherently insecure medium.

RESTful API
-----------

APIs are awesome and should be public! TNO.io provides an
open API which anybody can use to interact with various
services we provide. In fact, we eat our own dog food and
use the same APIs to power our site.

Currently the following endpoints are available.
For each information about each endpoint, you can make
``OPTIONS`` request to get tons more information.

* ``/api/v1/entropy/:bytes/``
* ``/api/v1/one-time-secrets/``
* ``/api/v1/one-time-secrets/:uuid/``

You can also query https://tno.io/api/v1/ to get all endpoints
as well.

Credits
-------

* Miroslav Shubernetskiy - https://github.com/miki725

License
-------

::

    The MIT License (MIT)

    Copyright (c) 2014 Miroslav Shubernetskiy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
