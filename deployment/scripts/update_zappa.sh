#!/bin/bash
#
# Runs the docker container, mounts the project and aws credentials folder
# and updates vue build and zappa.
updatezappa() {
  docker run -ti -e AWS_PROFILE=zappa -v "$(pwd):/var/task" \
    -v ~/.aws/:/root/.aws --rm britecore-zappa /bin/bash -c \
    "source ve/bin/activate \
      && pip install -r requirements/production.txt \
      && source deployment/scripts/post_deploy.sh \
      && $SHELL"
}
updatezappa