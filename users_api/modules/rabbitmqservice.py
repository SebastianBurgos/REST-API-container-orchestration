import time
import os
import pika
import json

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

channel_logs = gestormensajes.channel()
# Declarar una cola para logs
channel_logs.queue_declare(queue='logs', durable=True)

channel_profiles = gestormensajes.channel()
# Declarar una cola para perfiles
channel_profiles.queue_declare(queue='profiles', durable=True)

# Función para enviar mensajes a la cola de perfiles
def enviar_mensaje_profiles(usuario_json):
    # Serializar el objeto JSON a cadena antes de enviarlo
    mensaje = json.dumps(usuario_json)
    channel_profiles.basic_publish(exchange='', routing_key='profiles', body=mensaje)
    print(f"Mensaje enviado a la cola de profiles: ID: {usuario_json['id']}\nMensaje: {usuario_json}")

# Función original para enviar mensajes a la cola de logs
def enviar_mensaje_logs(tipo_log, metodo, ruta, modulo, app, fecha, ip, usuario_autenticado, token, mensaje):
    bodymessage = tipo_log+"#"+metodo+"#"+ruta+"#"+modulo+"#"+app+"#"+fecha+"#"+ip+"#"+usuario_autenticado+"#"+token+"#"+mensaje
    channel_logs.basic_publish(exchange='', routing_key='logs', body=bodymessage)
    print(f"Mensaje enviado a la cola de logs: ID: {ip}\nMensaje: {mensaje}")
