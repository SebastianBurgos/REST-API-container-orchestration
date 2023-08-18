# CREAR CONTENEDOR CON DATABASE
docker run -d -p 8080:3306 --name mysql-db -e MYSQL_ROOT_PASSWORD=1234 --mount type=bind,src="$(pwd)"/mysql-api,dst=/var/lib/mysql mysql

# ENTRAR AL CONTENEDOR
docker exec -it mysql-db mysql -p