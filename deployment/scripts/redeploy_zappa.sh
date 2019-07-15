#!/bin/bash
#
# Redeploys zappa from the working environment container.

redeployzappa() {
    docker run -ti -e AWS_PROFILE=zappa -v "$(pwd):/var/task" \
    -v ~/.aws/:/root/.aws --rm britecore-zappa /bin/bash -c \
    "source deployment/scripts/setup.sh \
      && $SHELL"
}
redeployzappa