from api_logs import app
from datetime import datetime
from modules.rabbitmqservice import enviar_mensaje
from flask import request, jsonify
from modules.util import get_data_filtered_by_date, get_logs_filtered_by_date, get_logs_filtered_by_type

# Metodo REST para obtener los logs
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
        log_type = request.args.get('log_type')

        # Obtener los dates de las fechas filtrados del directorio logs por rango de fecha
        data_filtered_by_date_range = get_data_filtered_by_date(initial_date, final_date)
                
        # Obtener los logs filtrados del directorio logs
        logs_filtered_by_date = get_logs_filtered_by_date(data_filtered_by_date_range)

        # Obtener los logs filtrados por tipo de log
        if log_type != None:
            logs = get_logs_filtered_by_type(logs_filtered_by_date, log_type)
        else:
            logs = logs_filtered_by_date

        # Aplicar paginación
        start = (page - 1) * per_page
        end = start + per_page
        paginated_logs = logs[start:end]

        # Retornar la lista de logs en formato JSON junto con información de paginación
        response = {
            "page": page,
            "per_page": per_page,
            "initial_date": initial_date,
            "final_date": final_date,
            "log_type": log_type,
            "logs": paginated_logs,
        }
        
        if any(paginated_logs):
            return jsonify(response), 200
        else:
            return jsonify({"message":"No se han encontrado logs con los parametros brindados"}), 404

    except Exception as err:
        print("Exception:", str(err))
        return jsonify({"error": "Error al obtener los logs de aplicación, razón: "+str(err)}), 500
    
# Metodo REST para obtener los logs de una aplicación específica
@app.route('/logs/<application>', methods=['GET'])
def get_app_logs(application):
    try:
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        # Obtener los parámetros de paginación de la URL (opcional)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        initial_date = request.args.get('initial_date', '2020-01-01')
        final_date = request.args.get('final_date', formatted_date)
        log_type = request.args.get('log_type')

        # Obtener los dates filtrados del directorio logs filtradas por rango de fecha
        data_filtered_by_date_range = get_data_filtered_by_date(initial_date, final_date)
                
        # Obtener los logs filtrados del directorio logs
        logs_filtered_by_date = get_logs_filtered_by_date(data_filtered_by_date_range)

        # Obtener los logs filtrados por tipo de log
        if log_type != None:
            logs = get_logs_filtered_by_type(logs_filtered_by_date, log_type)
        else:
            logs = logs_filtered_by_date

        # Filtrar los logs por la aplicación específica
        logs_by_application = [log for log in logs if log['APLICACION'] == application]

        # Ordenar los logs por fecha de creación
        logs_by_application.sort(key=lambda x: x['FECHA'])

        # Aplicar paginación
        start = (page - 1) * per_page
        end = start + per_page
        paginated_logs = logs_by_application[start:end]

        # Retornar la lista de logs en formato JSON junto con información de paginación
        response = {
            "page": page,
            "per_page": per_page,
            "initial_date": initial_date,
            "final_date": final_date,
            "log_type": log_type,
            "logs": paginated_logs,
        }
        
        if any(paginated_logs):
            return jsonify(response), 200
        else:
            return jsonify({"message":"No se han encontrado logs con los parametros brindados"}), 404

    except Exception as err:
        print("Exception:", str(err))
        return jsonify({"error": "Error al obtener los logs de aplicación, razón: "+str(err)}), 500
    
# Metodo REST para crear un LOG
@app.route('/logs', methods=['POST'])  
def register_log():
    try:
        # Obtener datos del cuerpo de la solicitud JSON
        data = request.get_json()

        # Verificar si todos los campos requeridos están presentes en los datos
        required_fields = ['TIPO-LOG',
                            'METODO-HTTP',
                            'RUTA',
                            'MODULO',
                            'APLICACION',
                            'FECHA',
                            'IP',
                            'ACCION']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"El campo '{field}' es requerido"}), 400

        tipo_log = data.get('TIPO-LOG')
        metodo_log = data.get('METODO-HTTP')
        ruta_log = data.get('RUTA')
        modulo_log = data.get('MODULO')
        aplicacion_log = data.get('APLICACION')
        fecha_log = data.get('FECHA')
        ip_log = data.get('IP')
        usuario_log = data.get('USUARIO-AUTENTICADO', 'GUEST')
        token_log = data.get('TOKEN', 'NO TOKEN')
        acccion_log = data.get('ACCION')

        # Crear el log
        enviar_mensaje(tipo_log,
                        metodo_log,
                        ruta_log, 
                        modulo_log, 
                        aplicacion_log, 
                        fecha_log, 
                        ip_log, 
                        usuario_log, 
                        token_log, 
                        acccion_log)
    
        return jsonify({"message": "Log registrado exitosamente"}), 201

    except Exception as err:
        print("Error: ", err)
        return jsonify({"error": "Error al registrar el log"}), 500