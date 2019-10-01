#!/bin/bash

export FLASK_SECRET_KEY=test_secret
export OAUTHLIB_INSECURE_TRANSPORT=1

$(gcloud beta emulators datastore env-init)
python src/main.py
