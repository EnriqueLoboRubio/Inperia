from db.conexion import obtener_conexion

# -------------------------------- COMENTARIO ------------------------------- #

# Función para crear la tabla de comentarios
def crear_comentario():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_respuesta INTEGER NOT NULL,
            id_profesional INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (id_respuesta) REFERENCES respuestas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_profesional) REFERENCES usuarios(id)
        )
    ''')

    conexion.commit()
    conexion.close()