#CONSUMIDOR
FROM python:3.9-alpine

# Define el directorio de trabajo
WORKDIR /app

# Copia todo el directorio actual
COPY . .

# Instala curl para poder hacer peticiones a la API
RUN apk update && apk add curl

# Instala las dependencias
RUN pip install -r requirements.txt

CMD ["python", "api_logs.py"]
