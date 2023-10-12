#!/bin/sh

# Inicia message_service.py en segundo plano
python message_service.py &

# Inicia api_message.py en primer plano
python api_message.py
