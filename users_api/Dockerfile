#PRODUCTOR O API
FROM python:3.9-alpine

WORKDIR /app

COPY . .

#Instala curl
RUN apk update && apk add curl

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
