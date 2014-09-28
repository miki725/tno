#!/bin/sh
PROJECT_DIR=$(echo $(pwd) | sed "s%/conf/nginx%%")

trap "docker stop nginx; exit 0;" 2 15

(docker start -ai nginx || \
docker run \
    -v `pwd`/conf:/etc/nginx \
    -v `pwd`/ssl:/ssl \
    -v `pwd`/logs:/var/log/nginx \
    -v "$PROJECT_DIR"/data:/data \
    -p 80:80 \
    -p 443:443 \
    -p 127.0.0.1:888:888 \
    --name nginx \
    miki725/nginx) \
& wait $!
