#!/bin/sh
DEFAULT_SETTINGS=tno.settings.prod
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:=$DEFAULT_SETTINGS}

migrate_cmd="/webapp/tno/manage.py migrate"

docker run \
    --rm \
    --volumes-from=webapp \
    -e "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE" \
    miki725/tnowebapp \
        bash -c "$migrate_cmd"
