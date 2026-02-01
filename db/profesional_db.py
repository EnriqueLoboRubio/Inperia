from db.conexion import obtener_conexion

# -------------------------------- PROFESIONAL ------------------------------- #

# Función para crear la tabla de profesionales
def crear_profesional():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE profesionales (
            id_usuario INTEGER PRIMARY KEY,
            especialidad TEXT CHECK(especialidad IN (
                'psicologo','educador_social','jurista','trabajador_social'
            )),
            num_colegiado TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    conexion.commit()
    conexion.close()