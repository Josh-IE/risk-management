#!/bin/bash
#
# Deploys zappa from the working environment container.

runimage() {
  docker run -ti -e AWS_PROFILE=zappa -v "$(pwd):/var/task" \
    -v ~/.aws/:/root/.aws --rm britecore-zappa /bin/bash -c \
    "source deployment/scripts/setup.sh \
      && zappa manage --all 'configure_web_app' \
      && $SHELL"
}
source ./deployment/scripts/build_docker_image.sh
runimage