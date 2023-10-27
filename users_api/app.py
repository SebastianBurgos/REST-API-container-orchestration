from flask import Flask

app = Flask(__name__)

print("El servicio de API REST se ha iniciado exitosamente.")

if __name__ == '__main__':
    from modules.routes import *
    app.run(host='0.0.0.0', port=5000)
