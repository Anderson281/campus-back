# Docker Django API template

It is a Docker template to start Django + DRF + GeoDjango APIs.
It cams with a working example in the buildings app.

# Help

- Clone the repo:

```ruby
    git clone https://github.com/joamona/django-api-template.git
```

- Change to the project folder:
```ruby
    cd django-api-template
```

- Create the pgadmin folders:
```ruby
    Windows: pgadmin_create_folders_windows.bat
    Linux: ./pgadmin_create_folders_linux.sh
```

- Change the ports of the services in the file .env
- Change the secret key, username, database name, etc. in the file .env.dev

- Create the images, containers and start the services:
```ruby
    docker compose up
```
- First time you will get a connection error from the service djangoapi. This is because PostgreSQL is stil
creating the database. Once the PostgreSQL service is OK. Cancel and start the services again.

```ruby
    control + c (cancel)
    docker compose up
```

Everithing should be fine now.

- Check the services:

    - pgadmin: http://localhost:5050
    - geoserver: http://localhost:8080 (Not started by default. You must uncomment the service in docker-compose.yml)
    - Django API: http://localhost:8000/core/hello_world/

# Initialize de database
A superuser must be created and the database must be migrated in order to create de database tables.
This work is done in the script ./initdb.sh. To execute this script:

    - Get into the container *-djangoapi-1 and type:

```ruby
    ./initdb.sh
```

# Start developping
To avoid to install Pyhton and its dependencies in your computer, you can 
use the interpreter in the container. You can achieve this with Visual Studio Code (VS).

- Start the services: docker compose up.
- Open VS.
- Press Ctrl + Shift + p.
- Paste the following: Dev Containers: Attach to Running Container.
- Select the container *-djangoapi-1.
- A new VS code window is started.
- Select the interpreter: Ctrl + Shift + p, and type python select interpreter, and select the interpreter in the container. There are two interpreters. Select the one in 
/usr/local/bib/python. This one is the one that has all the pythoin mackages installed: Django, GeoDjango, etc. In this way VS will help you to code.
- Now, you can modify the source files, and create new Django apps from the VS connected to the container.
- To create a new app, in the terminal, in the VS connected to the container, type: 

    python manage.py startapp mynewapp

# Debugging

RemoteDebug has been configured in the VS project and in settings.py. To stop the execution in a line:

- Put a breackpoint.
- Set, in djangoapi/settings.py, the REMOTE_DEBUG to true.
- Open the Debug window of VS and click Play over the DjangoAPI configuration.
- Ready to debug.

# Installed apps

The project cams with three app:

- core: It has the myLib package, who contains the geoModelSerializer. It is a base class to manage models with geometries. Ii uses geodjango.
- codelist: It is empty. It us thougt to contain all the models who represents codelists of possible values for other models.
- buildings: It contains a model, serializer, and modelViewSet as example of DFR and  geoModelSerializer example. 



