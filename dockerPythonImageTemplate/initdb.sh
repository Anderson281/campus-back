#/bin/sh

#create the initial Django tables
python manage.py makemigrations
python manage.py migrate
#create the Django superuser
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}







