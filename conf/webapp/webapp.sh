#!/bin/sh
PROJECT_DIR=$(echo $(pwd) | sed "s%/conf/webapp%%")

DEFAULT_SETTINGS=tno.settings.prod
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:=$DEFAULT_SETTINGS}

DEFAULT_NEW_RELIC_ENVIRONMENT=prod
NEW_RELIC_ENVIRONMENT=${NEW_RELIC_ENVIRONMENT:=DEFAULT_NEW_RELIC_ENVIRONMENT}

HOST_IP=$(ifconfig eth0 | grep inet | grep -v inet6 | awk '{print $2}' | sed "s/addr://")

trap "docker stop webapp; exit 0;" 2 15

(docker start -ai webapp || \
docker run \
    -v "$PROJECT_DIR":/webapp \
    -e "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE" \
    -e "NEW_RELIC_CONFIG_FILE=/webapp/tno/conf/newrelic.ini" \
    -e "NEW_RELIC_ENVIRONMENT=$NEW_RELIC_ENVIRONMENT" \
    -e "HOST_IP=$HOST_IP" \
    -p 127.0.0.1:8888:8888 \
    -w /webapp/tno \
    --name webapp \
    miki725/tnowebapp \
        newrelic-admin run-python \
            /usr/local/bin/gunicorn \
            --config conf/gunicorn.py \
            tno.wsgi:application) \
& wait $!
