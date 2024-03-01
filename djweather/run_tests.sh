#!/usr/bin/env bash

#source ../.env
#export DB_USER
#export DB_PASSWORD

pytest -s --cov=./ --cov-report=term-missing
#pytest -s -v
