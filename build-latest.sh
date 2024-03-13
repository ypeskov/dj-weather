#!/usr/bin/env bash

build_and_tag() {
    local tag="latest"
    local platform_option=""

    for arg in "$@"; do
        if [[ $arg == --platform=* ]]; then
            platform_option=$arg
        elif [[ $arg != "push" ]]; then
            tag=$arg
        fi
    done

    local build_command="docker build -f Dockerfiles/Dockerfile --target prod"
    if [[ -n $platform_option ]]; then
        build_command+=" $platform_option"
    fi
    build_command+=" -t djw ."

    eval $build_command
    docker tag djw ypeskov/djw:$tag
    echo "$tag" > version.txt
}

if [[ $# -eq 0 ]]; then
    build_and_tag
elif [[ $1 == "push" ]]; then
    build_and_tag "${@:2}"
    docker push ypeskov/djw:${2:-latest}

    echo "Updating docker-compose.yaml"
    sed -i '' "s|ypeskov/djw:[^[:space:]]*|ypeskov/djw:${2:-latest}|g" Dockerfiles/docker-compose.yaml
    echo "Updated docker-compose.yaml: $(grep -o "ypeskov/djw:[^[:space:]]*" Dockerfiles/docker-compose.yaml)"
    echo "Pushing to server"
    scp Dockerfiles/docker-compose.yaml root@135.181.38.18:djw/Dockerfiles/docker-compose.yaml
#    ssh root@135.181.38.18 "bash djw/run.sh"
    echo "Server updated. Please log in to and run run.sh to apply changes."

    echo "${2:-latest}" > version.txt
else
    echo "Usage:"
    echo "$0                                            # Build and tag :latest"
    echo "$0 push                                      # Build, tag and push :latest to Docker Hub"
    echo "$0 push <tag>                                # Build, tag as <tag> and push to Docker Hub"
    echo "$0 push [--platform=<platform>]              # Build for optional platform, tag as :latest, and push to Docker Hub"
    echo "$0 push <tag> [--platform=<platform>]        # Build for optional platform, tag as <tag>, and push to Docker Hub"
fi
