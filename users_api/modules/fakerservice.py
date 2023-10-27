import mysql.connector
from modules.insertions import data

# Insertar datos falsos en la base de datos
def insert_fake_data(db):
    try:
        cursor = db.cursor()
        print("Insertando datos falsos en la base de datos...")
        cursor.executemany("""INSERT INTO Usuario (nombre, apellido, email, clave, fecha_nacimiento) 
                            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(clave)s, %(fecha_nacimiento)s)""", data)
        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error:", err)