#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready; do
  echo ${POSTGRES_USER}
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

echo "PostgreSQL is ready. Starting restore."

#psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "create extension if not exists postgis"

### RESTORE THE DATABASE
#To restore a databse follow the following steps.
#If no database restore, the database will be empty

### ADDITIONAL USERS CREATION
#To restore a database firts you have to create the users that own the objects.
# - Put, in the file init-users.sql, the necessary sql sentences to create the users.
# - Uncomment the followign two lines.

#echo "Creating the user vagrant."
#psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < /usr/local/app/init-users.sql

### RESTORE THE DATABASE
#Create a custom backup file and put it here.
#Uncomment the following line and change the filename to restore

#pg_restore -v -U ${POSTGRES_USER} -d ${POSTGRES_DB} /usr/local/app/disati.backup
#echo "Database restore completed."

echo "Database cluster created."
