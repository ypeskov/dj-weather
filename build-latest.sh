#!/usr/bin/env bash

build_and_tag() {
    docker build -f Dockerfiles/Dockerfile --target prod -t djw . && \
    docker tag djw ypeskov/djw:latest
}

if [[ $# -eq 0 ]]; then
    build_and_tag
elif [[ $1 == "push" ]]; then
    build_and_tag
    docker push ypeskov/djw:latest
else
    echo "Usage:"
    echo "$0            # Build and tag :latest"
    echo "$0 push       # Build, tag and push :latest to Docker Hub"
fi
