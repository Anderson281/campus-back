mkdir pgadmin4
mkdir pgadmin4/data
mkdir pgadmin4/servers
touch pgadmin4/servers/servers.json
mkdir pgadmin4_prod
mkdir pgadmin4_prod/data
mkdir pgadmin4_prod/servers
touch pgadmin4_prod/servers/servers.json
sudo chown -R 5050:5050 pgadmin4
sudo chown -R 5050:5050 pgadmin4_prod
