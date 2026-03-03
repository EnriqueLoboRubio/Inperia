from db.conexion import obtener_conexion
from db.fecha_utils import normalizar_fecha

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
            comentario_ia TEXT,
            fecha_ia TEXT,
            comentario_profesional TEXT,       
            fecha_profesional TEXT,       
            FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_profesional) REFERENCES profesionales(id_usuario) ON DELETE RESTRICT,
            UNIQUE (id_entrevista, id_profesional)
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coment_ent_entrevista
        ON comentarios_ent(id_entrevista)
    ''')

    conexion.commit()
    conexion.close()


def _asegurar_fila_comentario_ent(cursor, id_entrevista, id_profesional):
    cursor.execute(
        """
        INSERT OR IGNORE INTO comentarios_ent (id_entrevista, id_profesional)
        VALUES (?, ?)
        """,
        (id_entrevista, id_profesional),
    )


def agregar_comentario_ia(id_entrevista, id_profesional, comentario_ia, fecha_ia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        fecha_norm = normalizar_fecha(fecha_ia)
        _asegurar_fila_comentario_ent(cursor, id_entrevista, id_profesional)
        cursor.execute(
            """
            UPDATE comentarios_ent
            SET comentario_ia = ?, fecha_ia = ?
            WHERE id_entrevista = ? AND id_profesional = ?
            """,
            (comentario_ia, fecha_norm, id_entrevista, id_profesional),
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al guardar comentario IA de entrevista: {e}")
        return False
    finally:
        conexion.close()


def agregar_comentario_profesional(id_entrevista, id_profesional, comentario_profesional, fecha_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        fecha_norm = normalizar_fecha(fecha_profesional)
        _asegurar_fila_comentario_ent(cursor, id_entrevista, id_profesional)
        cursor.execute(
            """
            UPDATE comentarios_ent
            SET comentario_profesional = ?, fecha_profesional = ?
            WHERE id_entrevista = ? AND id_profesional = ?
            """,
            (comentario_profesional, fecha_norm, id_entrevista, id_profesional),
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al guardar comentario profesional de entrevista: {e}")
        return False
    finally:
        conexion.close()
