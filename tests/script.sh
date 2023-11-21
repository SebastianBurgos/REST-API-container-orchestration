#!/bin/bash

# Verifica si Python está instalado
if ! command -v python3 &>/dev/null; then
    echo "Python no está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Verifica si pip está instalado
if ! command -v pip &>/dev/null; then
    echo "pip no está instalado. Instalando..."
    sudo apt-get install -y python3-pip
fi

# Verifica si pytest está instalado
if ! command -v pytest &>/dev/null; then
    echo "pytest no está instalado. Instalando..."
    sudo -H pip install -U pytest
fi

# Lista de carpetas donde se encuentran los archivos .py
carpetas=("testUsers" "testLogs" "testProfiles")

# Ejecuta los archivos .py en las carpetas especificadas
for carpeta in "${carpetas[@]}"; do
    if [ -d "$carpeta" ]; then
        echo "Ejecutando pruebas en $carpeta..."
        pytest "$carpeta"
    else
        echo "La carpeta $carpeta no existe."
    fi
done
