### File description

## Dockerfile
File that configures an image to use Pyhton.

- Download the image 3.12-alpine
- Install the necesary Linux libraries to support psycopg2, and gdal, required by Django, and geodjango
- Copy the code in this folder into the image in /usr/src/app
- Upgrade pip and install the Python requirements in requirements.txt
- Give execution permission to the file initdb.sh, to be able to execute it

## requirements.txt

- Python packages to be installed into the image. It contains all necessary  packages to develop with Python and Django

## initdb.sh

- Python script to create the initial Django tables and the Django superuser. 
It needs the DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD environment variables. They must be set
in the .env.dev or in the .env.prod files in the Docker Compose project.