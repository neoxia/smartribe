#!/bin/bash

source /srv/demo/venv/bin/activate
gunicorn -w 3 smartribe.wsgi:application
