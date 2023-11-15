import mysql from "mysql2/promise";

const crearConexion = async () => {
    try {
        const conexion = await mysql.createConnection({
            host: process.env.MYSQL_SERVICE,
            user: process.env.MYSQL_USER,        
            password: process.env.MYSQL_PASSWORD, 
            database: process.env.MYSQL_DATABASE 
        });

        console.log('¡Conectado a la base de datos MySQL!');
        return conexion;
    } catch (error) {
        console.error('El error de conexión es:', error);
        throw error; // Re-lanzar el error para que sea manejado en el código que importe esta función
    }
}

export default crearConexion;