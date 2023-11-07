import mysql from "mysql2"

const conexion = mysql.createConnection({
    host: process.env.MYSQL_SERVICE,
    user: process.env.MYSQL_USER,        
    password: process.env.MYSQL_PASSWORD, 
    database: process.env.MYSQL_DATABASE 
})

conexion.connect( (error)=> {
    if(error){
        console.log('El error de conexión es: '+error)
        return
    }
    console.log('¡Conectado a la base de datos MySQL!')
})

export default conexion;