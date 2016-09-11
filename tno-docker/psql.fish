#! /usr/bin/env fish

docker run -it --rm \
    --link=tno-postgres:postgres \
    miki725/postgres psql --host=postgres $argv
