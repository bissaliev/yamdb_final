#!/bin/bash
python3 manage.py migrate
python3 manage.py load_data
python3 manage.py collectstatic
exec gunicorn --bind 0:8000 api_yamdb.wsgi