#!/bin/sh
(docker inspect pgdata >/dev/null 2>&1) || \
docker run \
    --name pgdata \
    miki725/pgdata

trap "docker stop postgres; exit 0;" 2 15

(docker start -ai postgres || \
docker run \
    -v `pwd`/logs:/var/log/postgresql \
    -p 127.0.0.1:5432:5432 \
    --volumes-from=pgdata \
    --name postgres \
    miki725/postgres) \
& wait $!
