# Función para filtrar los datos de respuesta por un rango de fechas
from datetime import datetime
import os

def get_data_filtered_by_date(initial_date, final_date):
    data_filtered = []
    initialdate = datetime.strptime(initial_date, "%Y-%m-%d").date()
    finaldate = datetime.strptime(final_date, "%Y-%m-%d").date()

    # Por si el usuario ingresa un ragno incorrecto de fechas
    if initialdate > finaldate:
        raise Exception("Fecha inicial mayor a fecha final")

    # Listar los archivos del directorio logs que su nombre este en el rango de fechas dadas
    for strdate in os.listdir('logs'):
        formatedstrdate = strdate.split("_")[1].split(".")[0]
        currentdate = datetime.strptime(formatedstrdate, "%Y-%m-%d").date()
        if initialdate <= currentdate <= finaldate:
            data_filtered.append(str(currentdate))
    
    return data_filtered

# Función para filtrar los logs por un rango de fechas
def get_logs_filtered_by_date(data_filtered_by_date_range):
    logs = []
    for date_filtered in data_filtered_by_date_range:
            with open("logs/log_"+date_filtered+".log", "r") as log_file:
                log_content = log_file.read()
                log_entries = log_content.strip().split("\n\n")

                for entry in log_entries:
                    log_data = {}
                    lines = entry.strip().split("\n")
                    for line in lines:
                        key, value = line.split(": ", 1)
                        log_data[key] = value

                    logs.append(log_data)
    return logs

# Función para filtrar los logs por tipo de log
def get_logs_filtered_by_type(logs_filtered_by_date_range, log_type):
    logs_filtered_by_type = []

    for log in logs_filtered_by_date_range:
        if log["TIPO DE LOG"] == log_type:
            logs_filtered_by_type.append(log)
    
    return logs_filtered_by_type