#!/bin/bash

DB_USER="$MYSQL_USER"
DB_PASSWORD="$MYSQL_PASSWORD"

SQL_SCRIPT="./schema/script.sql"

mysql -u "$DB_USER" -p "$DB_PASSWORD" < "$SQL_SCRIPT"