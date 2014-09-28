#!/bin/sh

trap "docker stop skydock; exit 0;" 2 15

(docker start -ai skydock || \
docker run \
    -v /var/run/docker.sock:/docker.sock \
    --name skydock \
    crosbymichael/skydock \
        -ttl 31556900 \
        -environment tno \
        -s /docker.sock \
        -domain docker \
        -name skydns) \
& wait $!
