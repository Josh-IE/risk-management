#!/bin/bash
#
# Runs the docker container and mounts the project and aws credentials folder.
manageimage() {
  docker run -ti -e AWS_PROFILE=zappa -v "$(pwd):/var/task" \
    -v ~/.aws/:/root/.aws --rm britecore-zappa /bin/bash -c \
    "source ve/bin/activate \
      && set -o allexport \
      && source .env \
      && set +o allexport \
      && $SHELL"
}
manageimage