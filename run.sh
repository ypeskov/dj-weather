#!/usr/bin/env bash

CURR_DIR=$(pwd)
export CURR_DIR

if [ "$1" == "dev" ]; then
    docker-compose -f Dockerfiles/docker-compose.dev.yaml --env-file="$CURR_DIR"/.env up --build
else
    docker-compose -f Dockerfiles/docker-compose.yaml --env-file="$CURR_DIR"/.env up --build
fi

unset CURR_DIR
