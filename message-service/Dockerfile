#CONSUMIDOR
FROM python:3.9-alpine

WORKDIR /service

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# Copia el script de inicio
COPY start.sh /service/start.sh

# Establece permisos de ejecución para el script
RUN chmod +x /service/start.sh

# Ejecuta el script de inicio
CMD ["./start.sh"]
