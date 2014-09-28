#!/bin/sh

container_name=postgres
database=tnodb
user=tnouser
backup_location_check=/webapp
backup_location=/webapp/backup

dump_cmd="pg_dump $database -U $user -h $container_name"
date_file="backup.`date -u +"%Y-%m-%dT%H-%M-%S"`.sql.gz"

STDERR () {
    cat - 1>&2
}

# check that webapp exists
if [ ! -d "$backup_location_check" ]; then
    echo "'/webapp' does not exist so backup cannot be created" | STDERR
    exit 1
fi

# create backup subdirectory if not there
[ -d "$backup_location" ] || mkdir -p "$backup_location"

# check that container exists
docker inspect "$container_name" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Container $container_name does not exist" | STDERR
    exit 1
fi

# check that postgres is running
if [ $(docker inspect -f "{{.State.Running}}" "$container_name") = "false" ]; then
    echo "postgres is not running to take a backup" | STDERR
    exit 1
fi

docker run \
    --rm \
    -v "$backup_location":/backup \
    --link "$container_name":"$container_name" \
    miki725/postgres \
        bash -c "$dump_cmd | gzip > /backup/$date_file"
