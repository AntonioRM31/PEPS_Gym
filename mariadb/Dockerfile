FROM mariadb:latest

# Copia el archivo Juegos.sql al contenedor en el directorio de inicialización
COPY Juegos.sql /docker-entrypoint-initdb.d/

# Opcional: Si necesitas permisos especiales, puedes ajustar esto:
RUN chown mysql:mysql /docker-entrypoint-initdb.d/Juegos.sql
