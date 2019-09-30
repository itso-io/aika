#!/bin/bash

gcloud beta emulators datastore start &&
$(gcloud beta emulators datastore env-init) &&

python src/main.py
