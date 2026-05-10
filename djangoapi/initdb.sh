#/bin/sh
## This script is used to initialize the database for a Django application.
echo 'Initializing database'
python manage.py migrate
## Create a superuser if the environment variables are set
echo 'Creating superuser'
echo ${DJANGO_SUPERUSER_USERNAME}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}
echo 'Created'
## Create the database tables from the application models
python manage.py makemigrations
python manage.py migrate










