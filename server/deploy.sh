#!/bin/bash

python scripts/deploy_set_variables.py
gcloud app deploy src/app.yaml
git checkout src/app.yaml
