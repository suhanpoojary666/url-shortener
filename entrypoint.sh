#!/bin/sh

python manage.py migrate

exec "$@"

#this shell script makes the migrations for docker container before running