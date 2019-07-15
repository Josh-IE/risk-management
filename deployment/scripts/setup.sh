#!/bin/bash
#
# Creates and activates a virtual environment, installs production requirements,
# updates runs zappa deploy, updates environment files, runs post deploy.
python -m venv ve
source ve/bin/activate
pip install -r requirements/production.txt

# prevents TemplateDoesNotExist exception, during zappa's post deploy test.
mkdir -p web-app/dist && touch web-app/dist/index.html

MSG=$(zappa deploy) \
  && URL=${MSG##* } \
  && API_SUFFIX=/api/v1/ \
  && API_URL=$URL$API_SUFFIX \
  && sed -Ei "s/^(API_URL=*).*/\1${API_URL//\//\\/}/" .env \
  && source deployment/scripts/post_deploy.sh \
  && echo Your deployment is live!: $URL