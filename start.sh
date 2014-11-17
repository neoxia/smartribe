#!/bin/bash

export DJANGO_SETTINGS_MODULE="smartribe.settings_demo"
python3 manage.py migrate && \
gunicorn -w 2 -b 0.0.0.0:7777 smartribe.wsgi:application
