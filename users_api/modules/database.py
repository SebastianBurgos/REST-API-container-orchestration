import time
import mysql.connector
import os
#from modules.fakerservice import insert_fake_data

# Configuración de la base de datos
def esperar_db():
    while True:
        try:
            db = mysql.connector.connect(
                host=os.environ.get("SERVICE"),
                user=os.environ.get("USER"),
                password=os.environ.get("PASSWORD"),
                database=os.environ.get("DATABASE"),
            )

            # Generamos datos falsos para la base de datos
            #insert_fake_data(db)

            return db
        except mysql.connector.Error as err:
            print("Error:", err)
            print("Reintentando conexión a la base de datos en 5 segundos...")
            time.sleep(5)

db = esperar_db()