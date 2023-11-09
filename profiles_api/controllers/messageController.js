import { connect } from 'amqplib';
import dotenv from 'dotenv';

dotenv.config();

async function esperarRabbitMQ() {
    while (true) {
        try {
            const connection = await connect(`amqp://${process.env.RABBITMQ_SERVICE}`);
            return connection;
        } catch (error) {
            console.log('Reintentando conexión a RabbitMQ en 5 segundos...');
            await new Promise((resolve) => setTimeout(resolve, 5000));
        }
    }
}

const gestorMensajes = await esperarRabbitMQ();

const channel = await gestorMensajes.createChannel();
await channel.assertQueue('logs', { durable: true });

async function enviarMensaje(tipoLog, metodo, ruta, modulo, app, fecha, ip, usuarioAutenticado, token, mensaje) {
    const bodyMensaje = `${tipoLog}#${metodo}#${ruta}#${modulo}#${app}#${fecha}#${ip}#${usuarioAutenticado}#${token}#${mensaje}`;
    channel.sendToQueue('logs', Buffer.from(bodyMensaje));
    console.log(`Mensaje enviado: ID: ${ip}\nMensaje: ${mensaje}`);
}

export { enviarMensaje };
