#!/bin/bash

SQL_SCRIPT="./schema/script.sql"

# Check if MYSQL_PASSWORD environment variable is defined
if [ -z "$MYSQL_PASSWORD" ]; then
    echo "Error: MYSQL_PASSWORD environment variable is not defined."
    exit 1
fi

check_file_existence() {
    if [ ! -f "$1" ]; then
        echo "Error: File $1 does not exist."
        exit 1
    fi
}

execute_sql_script() {
    mysql -u root -p"$MYSQL_PASSWORD" < "$1"
}

show_table_structure() {
    # Get list of tables
    tables=$(mysql -u root -p"$MYSQL_PASSWORD" -e "USE ${MYSQL_DB}; SHOW TABLES;" | tail -n +2)

    # Show structure of each table
    for table in $tables; do
        echo "Table structure for $table:"
        mysql -u root -p"$MYSQL_PASSWORD" -e "USE ${MYSQL_DB}; DESCRIBE $table;"
        echo ""
    done
}

main() {
    check_file_existence "$SQL_SCRIPT"
    execute_sql_script "$SQL_SCRIPT"
    if [ $? -eq 0 ]; then
        echo "SQL script executed successfully."
        show_table_structure
    else
        echo "Error: Failed to execute SQL script."
        exit 1
    fi
}

main

exit 0
