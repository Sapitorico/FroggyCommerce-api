#!/bin/bash

SQL_SCRIPT="./schema/script.sql"

read -s -p "Ingrese la contraseña de MySQL: " MYSQL_PASSWORD
echo ""

check_file_existence() {
    if [ ! -f "$1" ]; then
        echo "Error: El archivo $1 no existe."
        exit 1
    fi
}

execute_sql_script() {
    mysql -u root -p"$MYSQL_PASSWORD" < "$1"
}

show_table_structure() {
    # Obtener la lista de tablas
    tables=$(mysql -u root -p"$MYSQL_PASSWORD" -e "USE ecommerce_db; SHOW TABLES;" | tail -n +2)

    # Mostrar la estructura de cada tabla
    for table in $tables; do
        echo "Estructura de la tabla $table:"
        mysql -u root -p"$MYSQL_PASSWORD" -e "USE ecommerce_db; DESCRIBE $table;"
        echo ""
    done
}

main() {
    check_file_existence "$SQL_SCRIPT"
    execute_sql_script "$SQL_SCRIPT"
    if [ $? -eq 0 ]; then
        echo "El script SQL se ha ejecutado correctamente."
        show_table_structure
    else
        echo "Error: No se pudo ejecutar el script SQL."
        exit 1
    fi
}

main

exit 0
