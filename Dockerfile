FROM ubuntu:22.04

# Actualiza el sistema y instala Python y MySQL
RUN apt update && \
    DEBIAN_FRONTEND="noninteractive" apt install -y python3 python3-pip python3-venv mysql-server

# Directorio de trabajo
WORKDIR /e_commerce

# Copia el contenido actual al directorio de trabajo
COPY . /e_commerce

# Instala virtualenv
RUN python3 -m venv sapovenv

# Activa el entorno virtual
SHELL ["/bin/bash", "-c"]
RUN source sapovenv/bin/activate && \
    pip install -r requirements.txt

# Inicializa el servicio MySQL y ejecuta el script SQL
RUN source .env && \
    MYSQL_DB=${MYSQL_DB} && \
    MYSQL_HOST=${MYSQL_HOST} && \
    MYSQL_USER=${MYSQL_USER} && \
    MYSQL_PASSWORD=${MYSQL_PASSWORD} && \
    service mysql start && \
    # Ejecuta el script SQL para crear la base de datos y las tablas
    mysql -u root -e "source schema/schema.sql;" && \
    # Crea un usuario MySQL para el ecommerce y asigna una contraseña
    mysql -u root -e "CREATE USER '${MYSQL_USER}'@'${MYSQL_HOST}' IDENTIFIED BY '${MYSQL_PASSWORD}';" && \
    # Otorga todos los permisos al usuario para todas las bases de datos
    mysql -u root -e "GRANT ALL PRIVILEGES ON ${MYSQL_DB}.* TO '${MYSQL_USER}'@'${MYSQL_HOST}' WITH GRANT OPTION;" && \
    # Hace que los cambios surtan efecto inmediatamente
    mysql -u root -e "FLUSH PRIVILEGES;" && \
    service mysql stop

# Ejecuta el archivo main.py dentro del entorno virtual sapovenv
CMD ["/bin/bash", "-c", "service mysql start && source sapovenv/bin/activate && python3 main.py"]