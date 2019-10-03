#!/bin/bash
set -e

python scripts/deploy_set_variables.py
gcloud app deploy --project aika-dev src/app.yaml src/index.yaml
git checkout src/app.yaml
