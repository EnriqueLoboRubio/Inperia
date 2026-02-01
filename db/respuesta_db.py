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