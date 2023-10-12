import os
from api_message import app
from datetime import datetime
from flask import request, jsonify

# tipo_log+"#"+metodo+"#"+ruta+"#"+modulo+"#"+fecha+"#"+ip+"#"+usuario_autenticado+"#"+token+"#"+mensaje
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        # Obtener los parámetros de paginación de la URL (opcional)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        initial_date = request.args.get('initial_date', '2020-01-01')
        final_date = request.args.get('final_date', formatted_date)
        tipo_log = request.args.get('tipo_log', 'INFO')

        # Obtener los dates filtrados del directorio logs
        datesfiltrados = []

        initialdate = datetime.strptime(initial_date, "%Y-%m-%d").date()
        finaldate = datetime.strptime(final_date, "%Y-%m-%d").date()

        # Por si el usuario ingresa un ragno incorrecto de fechas
        if initialdate > finaldate:
            return jsonify({"error":"El rango de fechas es incorrecto"}), 404

        # Listar los archivos del directorio logs que su nombre este en el rango de fechas dadas
        for strdate in os.listdir('logs'):
            formatedstrdate = strdate.split("_")[1].split(".")[0]
            currentdate = datetime.strptime(formatedstrdate, "%Y-%m-%d").date()
            print(str(currentdate) + "contra" + str(initialdate) + " " + str(finaldate))
            if initialdate <= currentdate <= finaldate:
                datesfiltrados.append(str(currentdate))
        
        # Obtener los logs filtrados del directorio logs
        # ... (código anterior) ...

        # Obtener los logs filtrados del directorio logs
        logs = []

        for datefiltrado in datesfiltrados:
            with open("logs/log_"+datefiltrado+".log", "r") as log_file:
                log_content = log_file.read()
                log_entries = log_content.strip().split("\n\n")

                for entry in log_entries:
                    log_data = {}
                    lines = entry.strip().split("\n")
                    for line in lines:
                        key, value = line.split(": ", 1)
                        log_data[key] = value

                    logs.append(log_data)

        # Retornar la lista de logs en formato JSON junto con información de paginación
        response = {
            "page": page,
            "per_page": per_page,
            "initial_date": initial_date,
            "final_date": final_date,
            "tipo_log": tipo_log,
            "logs": logs,
        }
        
        if any(logs):
            return jsonify(response), 200
        else:
            return jsonify({"error":"Error al obtener los logs"}), 404

    except Exception as err:
        print("Exception:", err)
        return jsonify({"error": "Error al obtener los logs"}), 500