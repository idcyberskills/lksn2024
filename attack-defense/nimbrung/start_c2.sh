#!/bin/bash

CONTAINER_NAME="nimbo_c2"

if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

docker run -it --rm --name $CONTAINER_NAME -p 80:80 -v $(pwd):/Nimbo-C2 -w /Nimbo-C2 itaymigdal/nimbo-dependencies
