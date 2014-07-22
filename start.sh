#!/bin/bash

/usr/bin/python3 /srv/smartribe/manage.py migrate && \
/usr/local/bin/gunicorn -w 2 -b 0.0.0.0:7777 smartribe.wsgi:application
