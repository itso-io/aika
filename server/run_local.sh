#!/bin/bash


export FLASK_ENV=development

$(gcloud beta emulators datastore env-init)
python src/main.py
