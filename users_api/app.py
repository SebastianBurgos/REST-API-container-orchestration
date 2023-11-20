from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print("El servicio de API REST se ha iniciado exitosamente.")

if __name__ == '__main__':
    from modules.routes import *
    app.run(host='0.0.0.0', port=5000)
