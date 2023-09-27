import time
import os
import pika

nombre_servicio = os.environ.get("SERVICE_NAME")

def esperar_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get("RABBITMQ_SERVICE"), heartbeat=600)
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Reintentando conexión a RabbitMQ en 5 segundos...")
            time.sleep(5)

gestormensajes = esperar_rabbitmq()

channel = gestormensajes.channel()
# Declarar una cola
channel.queue_declare(queue='autenticaciones')

# Declaramos la función para envio de mensajes
def enviar_mensaje(mensaje, metodo, ruta, username, fecha):
    bodymensaje = nombre_servicio+"#"+mensaje+"#"+metodo+"#"+ruta+"#"+username+"#"+fecha
    channel.basic_publish(exchange='', routing_key='autenticaciones', body=bodymensaje)
    print(f"Mensaje enviado: Usuario: {username}\nMensaje: {mensaje}")