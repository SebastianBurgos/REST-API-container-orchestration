#CONSUMIDOR
FROM python:3.9-alpine

WORKDIR /service

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "message_service.py"]
