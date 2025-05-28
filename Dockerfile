FROM python:3.8.18
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .  

RUN pip install -r requirements.txt  

ADD ./web .  

EXPOSE 8080
CMD ["python", "app.py", "runserver"]

FROM mariadb:latest

# Copia el archivo Juegos.sql al contenedor en el directorio de inicialización
COPY Juegos.sql /docker-entrypoint-initdb.d/

# Opcional: Si necesitas permisos especiales, puedes ajustar esto:
RUN chown mysql:mysql /docker-entrypoint-initdb.d/Juegos.sql
