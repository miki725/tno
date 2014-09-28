#!/bin/sh
set -e

STDERR () {
    cat - 1>&2
}

if [ "$1" = 'postgres' ]; then
    # exit if postgres directory does not already exist
    [ -d "$PGDATA" ] || (echo "PGDATA=$PGDATA does not exist" | STDERR && exit 1)

    chown -R postgres "$PGDATA"

    # if data directory does not have any files
    # initialize database in its place
    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb --encoding="UTF8"

        sed -ri "s/^#(listen_addresses\s*=\s*)\S+/\1'*'/" "$PGDATA"/postgresql.conf

        { echo; echo 'host all all 0.0.0.0/0 trust'; } >> "$PGDATA"/pg_hba.conf
    fi

    exec gosu postgres "$@"
fi

# command is a postgres executable hence execute it as postgres user
if [ -x "/usr/lib/postgresql/$POSTGRES_VERSION/bin/$1" ]; then
    exec gosu postgres "$@"
else
    exec "$@"
fi
