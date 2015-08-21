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

Deployment
----------

For the ease of deployment, TNO is packaged as a Docker container.
Docker allows to easily deploy the application with minimal setup.
The packaged `Dockerfile` only runs the Django webapp by using
[gunicorn](http://gunicorn.org/) web server and requires access
to a PostgreSQL database. Therefore it is recommended to run
TNO as part of a [docker-compose](https://docs.docker.com/compose/)
application. Example docker-compose application:

```yaml
data:
  image: busybox
  volumes:
    - /data

pgdata:
  image: miki725/pgdata

postgres:
  image: miki725/postgres
  expose:
    - 5432
  volumes_from:
    - pgdata

web:
  image: miki725/tno
  env_file: ./my.env
  expose:
    - 8888
  ports:
    - 8888:8888
  links:
    - postgres
  volumes_from:
    - data
```

Blank environment file will have a structure something like:

```ini
DJANGO_SETTINGS_MODULE=tno.settings.prod
ALLOWED_HOSTS=
SECRET_KEY=

DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

NEW_RELIC_ENABLED=true
NEW_RELIC_LICENSE_KEY=
NEW_RELIC_APP_NAME=TNO

OPBEAT_ENABLED=true
OPBEAT_ORGANIZATION_ID=
OPBEAT_APP_ID=
OPBEAT_SECRET_TOKEN=
```

To run the application, ``docker-compose`` can be used:

```bash
$ docker-compose up -d
```

That however will simply run the application.
When starting the application for the first time, some setup will be required.

1. Create database for TNO::

```bash
$ docker run -it --rm --link=tno_postgres_1:postgres miki725/postgres psql --host=postgres
sql> CREATE ROLE tno WITH
     NOSUPERUSER
     NOCREATEDB
     NOCREATEROLE
     NOINHERIT
     LOGIN
     ENCRYPTED PASSWORD '';
sql> CREATE DATABASE tno WITH
     OWNER="tnouser"
     ENCODING='UTF8';
```

2. Migrate Django application database to bring the schema up to date with the code:

```bash
$ docker run -it --rm \
    --env-file=my.env \
    --link=tno_postgres_1:postgres \
    tno_web ./manage.py migrate
```

3. Collect all the static files:

```bash
$ docker run -it --rm \
    --env-file=my.env \
    --link=tno_postgres_1:postgres \
    --volumes-from=tno_data_1 \
    tnobuild_web ./manage.py collectstatic --noinput
```

Credits
-------

* Miroslav Shubernetskiy - https://github.com/miki725
