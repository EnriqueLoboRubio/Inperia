from db.conexion import obtener_conexion

# -------------------------------- COMENTARIO ------------------------------- #

# Función para crear la tabla de comentarios
def crear_comentario_pre():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE comentarios_pre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_respuesta INTEGER NOT NULL,
            id_profesional INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (id_respuesta) REFERENCES respuestas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_profesional) REFERENCES profesionales(id_usuario) ON DELETE RESTRICT
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coment_pre_respuesta
        ON comentarios_pre(id_respuesta)
    ''')

    conexion.commit()
    conexion.close()
