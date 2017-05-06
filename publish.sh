#!/usr/bin/env bash

set -e

DOCKER_REGISTRY=686140181923.dkr.ecr.us-east-1.amazonaws.com

LATEST_COMMIT=`git rev-parse --short HEAD`
CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

DOCKER_TAG=${CURRENT_BRANCH//\//_}"-"$LATEST_COMMIT

# Tag it with DOCKER_TAG
docker tag -f html2pdf:latest $DOCKER_REGISTRY/html2pdf:$DOCKER_TAG

docker push $DOCKER_REGISTRY/html2pdf:$DOCKER_TAG
