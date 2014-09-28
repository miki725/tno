#!/bin/sh
DEFAULT_SETTINGS=tno.settings.prod
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:=$DEFAULT_SETTINGS}

docker run \
    --rm \
    --volumes-from=webapp \
    -e "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE" \
    miki725/tnowebapp \
        /webapp/tno/manage.py \
            collectstatic --noinput
