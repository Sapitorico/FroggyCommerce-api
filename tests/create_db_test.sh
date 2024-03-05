#!/bin/bash

# Cargar variables de entorno desde el archivo .env
if [[ -f .env ]]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: El archivo .env no encontrado."
    exit 1
fi

# Obtener el usuario y la contraseña de las variables de entorno
mysql_user=$MYSQL_USER
mysql_password=$MYSQL_PASSWORD

if [ -z "$mysql_user" ] || [ -z "$mysql_password" ]; then
    echo "Error: Las variables de entorno MYSQL_USER y/o MYSQL_PASSWORD no están configuradas."
    exit 1
fi

# Ejecutar el comando MySQL con el usuario y la contraseña proporcionados
mysql -u"$mysql_user" -p"$mysql_password" < tests/script.sql