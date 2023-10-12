import os
from datetime import datetime

# Obtener los dates filtrados del directorio logs
strdates = []

initialdate = datetime.strptime("2023-09-01", "%Y-%m-%d").date()
finaldate = datetime.strptime("2023-09-30", "%Y-%m-%d").date()
# Listar los archivos del directorio logs que su nombre este en el rango de fechas dadas
for strdate in os.listdir('logs'):
    formatedstrdate = strdate.split("_")[1].split(".")[0]
    currentdate = datetime.strptime(formatedstrdate, "%Y-%m-%d").date()
    if initialdate <= currentdate <= finaldate:
        strdates.append(str(currentdate))

logs = []

for datefiltrado in strdates:
            with open("logs/log_"+datefiltrado+".log", "r") as log_file:
                log = log_file.read()
                logs.append(log)

tipologfiltrar = "INFO"
strlogs = ""

for log in logs:
    strlogs += log

print(strlogs)
    