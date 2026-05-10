FROM postgis/postgis:16-3.4

WORKDIR /usr/local/app


#It is a sql file to create the vagrant user
#to be able to restore de backup withot errors
#as the vagrant user is the owner of the objects
COPY ./init-users.sql .

# The bacup to restore
COPY ./disati.backup .

# Copy the init-db.sh script into the container
# Everythin in that folder (/docker-entrypoint-initdb.d)
# is going to be executed,
# to init the database.
# If the database has already initialized, anything is going 
# to be executed
COPY ./init-db.sh /docker-entrypoint-initdb.d/init-db.sh

# Grant execution permissions for the init-db.sh script
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh
