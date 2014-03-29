#!/bin/bash
pip install django-registration django-mathfilters
python manage.py syncdb
python manage.py loaddata dump.json