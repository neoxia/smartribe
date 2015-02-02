#!/bin/bash
export DJANGO_SETTINGS_MODULE="smartribe.settings_demo"
python3 manage.py migrate && \
supervisord -c /srv/smartribe/supervisor/supervisor.conf -n
