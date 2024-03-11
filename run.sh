#!/usr/bin/env bash

CURR_DIR=$(pwd)
export CURR_DIR

if [ "$1" == "dev" ]; then
    docker-compose -f Dockerfiles/docker-compose.dev.yaml --env-file="$CURR_DIR"/.env up --build
else
    SCREEN_NAME="my_docker_session"

    if screen -list | grep -q "$SCREEN_NAME"; then
        echo "Session '$SCREEN_NAME' already exists."
    else
        screen -dmS "$SCREEN_NAME" /bin/bash \
         -c "docker-compose -f Dockerfiles/docker-compose.yaml --env-file=\"$CURR_DIR\"/.env up --build; exec sh"
    fi
fi

unset CURR_DIR

