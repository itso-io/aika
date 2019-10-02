#!/bin/bash


export FLASK_ENV=development
export DATASTORE_EMULATOR_HOST=localhost:8277


python src/main.py
