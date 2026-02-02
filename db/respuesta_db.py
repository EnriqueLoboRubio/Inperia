import sqlite3
from db.conexion import obtener_conexion

# -------------------------------- RESPUESTA ------------------------------- #

# Función para crear la tabla de respuestas
def crear_respuesta():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entrevista INTEGER NOT NULL,
            id_pregunta INTEGER NOT NULL,
            texto_respuesta TEXT,            
            puntuacion_ia REAL,
            FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id) ON DELETE CASCADE
        )
    ''')

    conexion.commit()
    conexion.close()

#Función para agregar nueva respuesta
def agregar_respuesta(id_entrevista, id_pregunta, texto_respuesta, puntacion_ia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute('''
            INSERT INTO respuestas (id_entrevista, id_pregunta, texto_respuesta, puntacion_ia)
            VALUES (?,?,?,?)
        ''', (id_entrevista, id_pregunta, texto_respuesta, puntacion_ia))
    except sqlite3.IntegrityError:
        print("ERror: No se ha podido crear la respuesta")
        return False

    conexion.commit()
    conexion.close()
    return True
    
    