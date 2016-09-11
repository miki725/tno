#! /usr/bin/env fish

docker run -it --rm \
  --env-file=prod.env \
  --link=tno-postgres:postgres \
  --volume=tno-data:/data \
  tnodocker_web ./manage.py $argv
