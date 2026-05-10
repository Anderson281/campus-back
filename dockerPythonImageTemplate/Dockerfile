# pull official base image
FROM python:3.12-alpine

# ARG USER_ID sets the USER_ID variable in the Dockerfile, 
#    reading the value from the USER_ID arg variable.
# This arg variable is set in the djangoapi->build->args section 
#    of the docker-compose.yml file
#    The username is set in the .env.dev file
ARG USER_ID
ARG GROUP_ID
ARG USERNAME

# Crear grupo y usuario con los mismos UID y GID que el host
RUN addgroup -g $GROUP_ID $USERNAME && \
    adduser -D -u $USER_ID -G $USERNAME $USERNAME

# set work directory
# WORKDIR /usr/src/app

WORKDIR /home/$USERNAME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2, and geodjango dependencies
RUN apk update && apk add postgresql-dev g++ gcc musl-dev libpq-dev wget pango gdal-dev geos-dev proj-dev gcc musl-dev \
     libffi-dev python3-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     libc-dev linux-headers 

# install dependencies
RUN pip install --upgrade pip

# Set the user to copy the files to the container,
# so the owner of the files is the user and not root
# and the user in the host match with the user in the container
USER $USERNAME
COPY . .
# Set the user root to install the dependencies. Otherwise the
# the python dependencies are not found latter in the container
USER root
RUN pip3 install -r requirements.txt
# Set the user again to be the defaut user in the container
USER $USERNAME

