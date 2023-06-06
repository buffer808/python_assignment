#! /bin/sh

RUN_DEBUGGER=$1

cd /app/financial

if [ "$RUN_DEBUGGER" = "True" ]; then
    python -m debugpy --listen 0.0.0.0:9009 --wait-for-client manage.py & 
    python manage.py runserver 0.0.0.0:5000
else
    # python manage.py runserver 0.0.0.0:8000
    gunicorn financial.wsgi:application --bind=0.0.0.0:5000
fi;
