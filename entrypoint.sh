#!/bin/bash
set -euo pipefail

CONFIG='/var/www/watcher/CONFIG'

if [ ! -f "$CONFIG" ]
then
    DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    ENV_DJANGO_SECRET_KEY="DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}"
    echo $ENV_DJANGO_SECRET_KEY >> "$CONFIG"
    sleep 10
    export $(cat "$CONFIG" | xargs)
    cd /var/www/watcher/watcher
    python manage.py migrate
    python manage.py createsuperuser2 --username=admin --email=admin@wexample.com --password=watcheradmin
    python manage.py createappgroups
    python manage.py addsuperusertoadmgroup
    exec "$@"
else
    export $(cat "$CONFIG" | xargs)
    exec "$@"
fi