#!/bin/bash
#
# Sets environment variables, installs npm packages, builds Vue.js app, uupdates
# zappa, migrate models and collects statict files.
set -o allexport \
  && source .env \
  && set +o allexport \
  && npm install --prefix web-app/ \
  && npm run build --prefix web-app/ \
  && zappa update \
  && zappa manage --all 'migrate risk_model_api' \
  && zappa manage --all 'collectstatic --noinput'