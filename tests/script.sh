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

# Instalamos venv
sudo apt-get install -y python3-venv

# Creamos el entorno virtual
python3 -m venv venv

# Activamos el entorno virtual
source venv/bin/activate

# Instalamos pytest
pip install pytest

# Lista de carpetas donde se encuentran los archivos .py
carpetas=("testUsers" "testLogs" "testProfiles" "testGateway")

# Ejecuta los archivos .py en las carpetas especificadas
for carpeta in "${carpetas[@]}"; do
    if [ -d "$carpeta" ]; then
        echo "Ejecutando pruebas en $carpeta..."
        pytest "$carpeta"
    else
        echo "La carpeta $carpeta no existe."
    fi
done

# Desactivamos el entorno virtual
deactivate

# Eliminamos el entorno virtual
rm -rf venv
