#!/usr/bin/env bash

set -e

LATEST_COMMIT=`git rev-parse --short HEAD`
CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

DOCKER_TAG=${CURRENT_BRANCH//\//_}"-"$LATEST_COMMIT

# Tag it with DOCKER_TAG
docker tag html2pdf:latest $DOCKER_REGISTRY/html2pdf:$DOCKER_TAG

docker push $DOCKER_REGISTRY/html2pdf:$DOCKER_TAG
