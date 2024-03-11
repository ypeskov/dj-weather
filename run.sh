#!/usr/bin/env bash

CURR_DIR=$(pwd)
export CURR_DIR

run_docker() {
    SCREEN_NAME="my_docker_session"
    if [ "$1" == "dev" ]; then
        docker-compose -f Dockerfiles/docker-compose.dev.yaml --env-file="$CURR_DIR"/.env up --build
    elif [ "$1" == "stop" ]; then
        echo "Stopping all containers..."
    else
        if screen -list | grep -q "$SCREEN_NAME"; then
            echo "Session '$SCREEN_NAME' is already running. Restarting the containers in it."
            screen -S "$SCREEN_NAME" -X stuff $'docker-compose -f Dockerfiles/docker-compose.yaml --env-file="$CURR_DIR"/.env up --build -d\n'
        else
            echo "Session '$SCREEN_NAME' is not found. Creating a new one and starting the containers in it."
            screen -dmS "$SCREEN_NAME" /bin/bash -c "\
            docker-compose -f Dockerfiles/docker-compose.yaml --env-file=\"$CURR_DIR\"/.env up --build -d; exec sh"
        fi
    fi
}

# Check the first command line argument
if [ "$1" == "stop" ]; then
    # Stop the containers based on the environment
    if [ "$2" == "dev" ]; then
        docker-compose -f Dockerfiles/docker-compose.dev.yaml --env-file="$CURR_DIR"/.env down
    else
        docker-compose -f Dockerfiles/docker-compose.yaml --env-file="$CURR_DIR"/.env down
    fi
else
    # Restart the containers
    run_docker "$1"
fi

unset CURR_DIR
