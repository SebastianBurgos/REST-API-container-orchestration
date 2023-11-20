import amqp from 'amqplib';
import { crearConexion } from '../database/db.js';

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

async function procesarMensaje(msg) {
    try {
        const mensaje = msg.content.toString();
        const datosPerfil = JSON.parse(mensaje);

        const {
            id,
            nombre,
            apellido,
            email
        } = datosPerfil;

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

        if (results.affectedRows > 0) {
            console.log('Perfil creado exitosamente en la base de datos');
        } else {
            console.error('Error al crear el perfil en la base de datos');
        }

    } catch (error) {
        console.error('Error al procesar el mensaje:', error);
    }
}

let isListening = false; // Bandera para controlar si está escuchando

async function connectToRabbitMQ() {
    try {
        const connection = await amqp.connect(`amqp://${process.env.RABBITMQ_SERVICE}`);
        const channel = await connection.createChannel();

        const queue = 'profiles';
        await channel.assertQueue(queue, { durable: true });

        channel.consume(queue, (msg) => {
            if (msg !== null) {
                procesarMensaje(msg);
                channel.ack(msg);
            }
        });

        console.log('Esperando mensajes para creación automática de perfil...');
        isListening = true; // Establecer la bandera a true para indicar que está escuchando

    } catch (error) {
        if (error.code === 'ECONNREFUSED' || error.name === 'AMQPConnectionError') {
            console.error('Error de conexión a RabbitMQ:', error.message);
        } else {
            console.error('Error no manejado:', error);
        }
    }
}

export async function consumeMessages() {
    await connectToRabbitMQ(); // Conexión inicial

    while (isListening) {
        // Se queda escuchando mientras la conexión sea exitosa
        await new Promise(resolve => setTimeout(resolve, 1000)); // Otra operación o simplemente esperar
    }
}

