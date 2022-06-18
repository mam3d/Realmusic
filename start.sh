#!/bin/bash
service cron start
/etc/init.d/nginx start
python manage.py crontab add
python manage.py migrate 
python manage.py collectstatic --noinput 
gunicorn config.wsgi:application -w 2 -b 0.0.0.0:8000