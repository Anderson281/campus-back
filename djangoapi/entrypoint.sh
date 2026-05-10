#!/bin/sh

# Si algún comando falla, el script se detiene
echo "entrypoint.sh"
set -e

echo "Esperando a la base de datos: $POSTGRES_DB en host postgis..."

# 1. Espera hasta que la base de datos acepte conexiones
until python -c "
import psycopg
import sys
try:
    conn = psycopg.connect(
        dbname='$POSTGRES_DB',
        user='$POSTGRES_USER',
        password='$POSTGRES_PASSWORD',
        host='postgis',
        connect_timeout=3
    )
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
"; do
  echo "Postgres (o la DB $POSTGRES_DB) no está lista aún... esperando 2 segundos"
  sleep 2
done

echo "¡Base de datos lista!"

# 2. Comprobar si el esquema 'codelist' existe
echo "Comprobando si la tabla 'auth_user' ya existe..."
AUTH_USER_TABLE_EXISTS=$(python -c "
import psycopg
import sys
try:
    conn = psycopg.connect(
        dbname='$POSTGRES_DB',
        user='$POSTGRES_USER',
        password='$POSTGRES_PASSWORD',
        host='postgis'
    )
    with conn.cursor() as cur:
        # Buscamos el esquema en el catálogo de Postgres
        cur.execute(\"SELECT 1 FROM information_schema.tables WHERE table_name = 'auth_user'\")
        exists = cur.fetchone() is not None
        # Imprimimos True o False para que el shell lo capture
        print(exists)
    conn.close()
except Exception as e:
    print(f'Error comprobando esquema: {e}', file=sys.stderr)
    sys.exit(1)
")

# 3. Ejecutar initdb.sh solo si el esquema NO existe
if [ "$AUTH_USER_TABLE_EXISTS" = "False" ]; then
    echo "El la tabla 'auth_user' no existe. Ejecutando inicialización (initdb.sh)..."
    ./initdb.sh
else
    echo "La tabla 'auth_user' ya existe. Saltando inicialización de la base de datos."
fi

# Ejecutamos el comando final
exec "$@"