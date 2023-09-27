import pika
import os
import time
import datetime

print("Iniciando servicio consumidor de mensajes...")

def callback(ch, method, properties, body):
    message_info = body.decode('utf-8').split('#')
    print(f"FROM SERVICE: {message_info[0]}")
    print(f"ACCION: {message_info[1]}")
    print(f"METODO-HTTP: {message_info[2]}")
    print(f"RUTA: {message_info[3]}")
    print(f"IP: {message_info[4]}")
    print(f"FECHA: {message_info[5]}")

    # Obtener la ruta actual del script
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Construir la ruta de la carpeta "logs"
    logs_folder = os.path.join(current_path, "logs")

    # Verificar si la carpeta "logs" existe, si no, crearla
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Construir el nombre del archivo de log con la ruta de la carpeta
    log_filename = os.path.join(logs_folder, datetime.datetime.now().strftime("log_%Y-%m-%d.txt"))

    with open(log_filename, 'a') as log_file:
        log_file.write(f"FROM SERVICE: {message_info[0]}\n")
        log_file.write(f"ACCION: {message_info[1]}\n")
        log_file.write(f"METODO-HTTP: {message_info[2]}\n")
        log_file.write(f"RUTA: {message_info[3]}\n")
        log_file.write(f"IP: {message_info[4]}\n")
        log_file.write(f"FECHA: {message_info[5]}\n\n")


while True:
    try:
        print("Conectando a RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_SERVICE"), heartbeat=600))
        channel = connection.channel()

        channel.queue_declare(queue='autenticaciones')

        channel.basic_consume(queue='autenticaciones', on_message_callback=callback, auto_ack=True)

        print('Esperando mensajes...')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        print("Reintentando conexión a RabbitMQ en 5 segundos...")
        time.sleep(5)
