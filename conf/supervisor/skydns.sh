#!/bin/sh

trap "docker stop skydns; exit 0;" 2 15

(docker start -ai skydns || \
docker run \
    -p 172.17.42.1:53:53/udp \
    --name skydns \
    crosbymichael/skydns \
        -nameserver 8.8.8.8:53 \
        -domain docker) \
& wait $!
