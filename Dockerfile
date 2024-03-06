FROM ubuntu:22.04

# Actualiza el sistema y instala Python y MySQL
RUN apt update && \
    apt install -y python3 python3-pip python3-venv mysql-server

# Directorio de trabajo
WORKDIR /e_commerce

# Copia el contenido actual al directorio de trabajo
COPY . /e_commerce

# Instala virtualenv
RUN python3 -m venv sapoenv

# Activa el entorno virtual
SHELL ["/bin/bash", "-c"]
RUN source sapoenv/bin/activate && \
    pip install -r requirements.txt

# Inicializa el servicio MySQL
RUN service mysql start

