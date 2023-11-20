import crearConexion from "../database/db.js";
import { enviarMensaje } from "./messageController.js";

const esperarConexion = async () => {
    while (true) {
        try {
            const db = await crearConexion();
            return db;
        } catch (error) {
            console.log('Reintentando conexión a la base de datos en 5 segundos...');
            await new Promise(resolve => setTimeout(resolve, 5000));
        }
    }
}

const db = await esperarConexion();

// Obtener la información de todos los perfiles
export const getAllProfiles = async (req, res) => {
    try {
        const [results] = await db.execute('SELECT * FROM Perfil');
        return res.json(results);
    } catch (error) {
        console.error(error);
        return res.json({ error: 'Error al obtener todos los perfiles' });
    }
}

// Obtener un perfil dado un id por parametro
export const getProfile = async (req, res) => {
    try {
        if (!req.headers.authorization) {
            return res.status(401).json({
                mensaje: 'No autorizado, token no existente'
            });
        }

        const id = req.params.id;
        const [results] = await db.execute('SELECT * FROM Perfil WHERE id = ?', [id]);
        if (results.length > 0) {
            return res.json(results[0]);
        } else {
            return res.status(404).json({ mensaje: 'No se encontró el perfil' });
        }
    } catch (error) {
        console.error(error);
        return res.json({ error: error.message });
    }
}

// Crear el perfil de un usuario
export const createProfile = async (req, res) => {
    try {
        const { id, nombre, apellido, email } = req.body;
        const url_pagina = email;
        const apodo = `${nombre} ${apellido}`;
        const informacion_publica = 1;
        const direccion_correspondencia = "N/A";
        const biografia = "N/A";
        const organizacion = "N/A";
        const pais = "N/A";

        const values = [
            id,
            url_pagina,
            apodo,
            informacion_publica,
            direccion_correspondencia,
            biografia,
            organizacion,
            pais
        ];

        const [results] = await db.execute('INSERT INTO Perfil (id, url_pagina, apodo, informacion_publica, direccion_correspondencia, biografia, organizacion, pais) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values);
            
        if(results.affectedRows > 0){
            const tipo_log = "PROFILE";
            const metodo = "POST";
            const ruta = "/profiles"; 
            const modulo = "PROFILECONTROLLER.JS";
            const application = "PROFILES_API_REST";
            const usuario_autenticado = `USUARIO CON ID: ${id}`;
            const token = "NO TOKEN";
            const mensaje = "NUEVO PERFIL CREADO.";
            const fecha = obtenerFechaActual();

            const ip = obtenerIPv4(req); // Obtiene la dirección IP del cliente

            await enviarMensaje(tipo_log, metodo, ruta, modulo, application, fecha, ip, usuario_autenticado, token, mensaje);
            
            return res.status(200).json({
                mensaje: "Perfil creado exitosamente",
                detalles: "Filas afectadas: "+ results.affectedRows
            });
        }else{
            return res.status(500).json({
                mensaje: "Perfil no creado",
                detalles: "Ha ocurrido un error en la base de datos al crear el perfil"
            });
        }
    } catch (error) {
        return res.status(500).json({
            error: 'Ha ocurrido un error al crear el perfil',
            detalles: error.message
        });
    }
}

// Actualizar el perfil de un usuario
export const updateProfile = async (req, res) => {
    try {
        //Verificar si el token de bearer token es válido
        if (!req.headers.authorization) {
            return res.status(401).json({
                mensaje: 'No autorizado, token no existente'
            });
        }

        const token_auth = req.headers.authorization.split(' ')[1];

        const profile_id = parseInt(req.params.id);
        
        const {
            url_pagina,
            apodo, 
            informacion_publica, 
            direccion_correspondencia, 
            biografia, 
            organizacion, 
            pais
        } = req.body;
        
        const values = [];
        let updateQuery = `UPDATE Perfil SET `;
        
        if (url_pagina !== undefined && url_pagina !== '') {
            updateQuery += `url_pagina = ?, `;
            values.push(url_pagina);
        }
        
        if (apodo !== undefined && apodo !== '') {
            updateQuery += `apodo = ?, `;
            values.push(apodo);
        }
        
        if (informacion_publica !== undefined && informacion_publica !== '') {
            updateQuery += `informacion_publica = ?, `;
            values.push(informacion_publica);
        }
        
        if (direccion_correspondencia !== undefined && direccion_correspondencia !== '') {
            updateQuery += `direccion_correspondencia = ?, `;
            values.push(direccion_correspondencia);
        }
        
        if (biografia !== undefined && biografia !== '') {
            updateQuery += `biografia = ?, `;
            values.push(biografia);
        }
        
        if (organizacion !== undefined && organizacion !== '') {
            updateQuery += `organizacion = ?, `;
            values.push(organizacion);
        }
        
        if (pais !== undefined && pais !== '') {
            updateQuery += `pais = ?, `;
            values.push(pais);
        }
        
        // Quitar la última coma y espacio del string updateQuery
        updateQuery = updateQuery.slice(0, -2);
        
        // Agregar la condición WHERE
        updateQuery += ` WHERE id = ?`;
        values.push(profile_id);
        
        const [results] = await db.execute(updateQuery, values);
            
        if(results.affectedRows > 0){
            // Después de actualizar el perfil, envía el mensaje
            const tipo_log = "PROFILE";
            const metodo = "PUT";
            const ruta = "/profiles/:id"; 
            const modulo = "PROFILECONTROLLER.JS";
            const application = "PROFILES_API_REST";
            const usuario_autenticado = `USUARIO CON ID: ${profile_id}`;
            const token = token_auth;
            const mensaje = "PERFIL ACTUALIZADO.";
            const fecha = obtenerFechaActual();

            const ip = obtenerIPv4(req); // Obtiene la dirección IP del cliente

            await enviarMensaje(tipo_log, metodo, ruta, modulo, application, fecha, ip, usuario_autenticado, token, mensaje);
            
            return res.status(200).json({
                mensaje: "Perfil actualizado exitosamente",
                detalles: "Filas actualizadas: "+ results.affectedRows
            });
        }else{
            return res.status(401).json({
                mensaje: "Perfil no actualizado",
                detalles: "El perfil no ha sido encontrado"
            });
        }
    } catch (error) {
        return res.status(500).json({
            error: 'Ha ocurrido un error al actualizar el perfil',
            detalles: error.message
        });
    }
}

// Eliminar el perfil de un usuario por ID
export const deleteProfile = async (req, res) => {
    try {
        const { id } = req.params;

        const [results] = await db.execute('DELETE FROM Perfil WHERE id = ?', [id]);

        if (results.affectedRows > 0) {
            const tipo_log = "PROFILE";
            const metodo = "DELETE";
            const ruta = `/profiles/${id}`;
            const modulo = "PROFILECONTROLLER.JS";
            const application = "PROFILES_API_REST";
            const usuario_autenticado = `USUARIO CON ID: ${id}`;
            const token = "NO TOKEN";
            const mensaje = "PERFIL ELIMINADO.";
            const fecha = obtenerFechaActual();

            const ip = obtenerIPv4(req); // Obtiene la dirección IP del cliente

            await enviarMensaje(tipo_log, metodo, ruta, modulo, application, fecha, ip, usuario_autenticado, token, mensaje);

            return res.status(200).json({
                mensaje: "Perfil eliminado exitosamente",
                detalles: "Filas afectadas: " + results.affectedRows
            });
        } else {
            return res.status(404).json({
                mensaje: "Perfil no encontrado",
                detalles: "El perfil con el ID proporcionado no existe en la base de datos"
            });
        }
    } catch (error) {
        return res.status(500).json({
            error: 'Ha ocurrido un error al eliminar el perfil',
            detalles: error.message
        });
    }
}


function obtenerFechaActual(){
    const fechaActual = new Date();

    const año = fechaActual.getFullYear();
    const mes = String(fechaActual.getMonth() + 1).padStart(2, '0');
    const dia = String(fechaActual.getDate()).padStart(2, '0');

    const horas = String(fechaActual.getHours()).padStart(2, '0');
    const minutos = String(fechaActual.getMinutes()).padStart(2, '0');
    const segundos = String(fechaActual.getSeconds()).padStart(2, '0');
    const milisegundos = fechaActual.getMilliseconds();

    const fechaFormateada = `${año}-${mes}-${dia} ${horas}:${minutos}:${segundos}.${milisegundos}`;

    return fechaFormateada;
}

const obtenerIPv4 = (req) => {
    const rawIp = req.connection.remoteAddress;
    const ipv4 = rawIp.replace(/^::ffff:/, '');
    return ipv4;
};