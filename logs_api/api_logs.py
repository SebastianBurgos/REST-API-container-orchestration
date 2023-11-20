from flask import Flask
from flask_cors import CORS

import multiprocessing

app = Flask(__name__)
CORS(app)

def start_api():
    app.run(host='0.0.0.0', port=5005)

if __name__ == '__main__':
    print("El servicio de API REST de LOGS se ha iniciado exitosamente en el puerto 5005.")
    from modules.routes import *
    from message_service import start_message_service

    p1 = multiprocessing.Process(target=start_message_service)
    p2 = multiprocessing.Process(target=start_api)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
