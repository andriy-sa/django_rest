#!/bin/bash

set -e
LOGFILE=/var/log/gunicorn/django_rest.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
# user/group to run as
USER=root
GROUP=sudo
PORT=8001 # Этот порт будет разным у каждого django-проекта
cd /home/elantix/venv/rest-django/django_rest/
source ../bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR

exec gunicorn -k eventlet django_rest.wsgi:application -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE \
  --bind 127.0.0.1:$PORT