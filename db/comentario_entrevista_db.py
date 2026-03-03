from db.conexion import obtener_conexion

# -------------------------------- COMENTARIO ------------------------------- #

# Función para crear la tabla de comentarios
def crear_comentario_ent():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE comentarios_ent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entrevista INTEGER NOT NULL,
            id_profesional INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            fecha TEXT,
            FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id),
            FOREIGN KEY (id_profesional) REFERENCES usuarios(id)
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coment_ent_entrevista
        ON comentarios_ent(id_entrevista)
    ''')

    conexion.commit()
    conexion.close()
