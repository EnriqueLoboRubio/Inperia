from db.conexion import obtener_conexion
from db.fecha_utils import normalizar_fecha


NOMBRE_TABLA = "comentarios_ia_ent"


def crear_tabla_comentarios_ia_entrevista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {NOMBRE_TABLA} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_entrevista INTEGER NOT NULL UNIQUE,
                comentario_ia TEXT,
                fecha_ia TEXT,
                FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id) ON DELETE CASCADE
            )
            """
        )
        cursor.execute(
            f"""
            CREATE INDEX IF NOT EXISTS idx_coment_ia_ent_entrevista
            ON {NOMBRE_TABLA}(id_entrevista)
            """
        )

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'comentarios_ent'"
        )
        tabla_antigua = cursor.fetchone()
        if tabla_antigua:
            cursor.execute(
                f"""
                INSERT OR IGNORE INTO {NOMBRE_TABLA} (id_entrevista, comentario_ia, fecha_ia)
                SELECT id_entrevista, comentario_ia, fecha_ia
                FROM comentarios_ent
                WHERE TRIM(COALESCE(comentario_ia, '')) <> ''
                """
            )

        conexion.commit()
    finally:
        conexion.close()


def _asegurar_fila(cursor, id_entrevista):
    cursor.execute(
        f"""
        INSERT OR IGNORE INTO {NOMBRE_TABLA} (id_entrevista)
        VALUES (?)
        """,
        (id_entrevista,),
    )


def agregar_comentario_ia(id_entrevista, comentario_ia, fecha_ia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        crear_tabla_comentarios_ia_entrevista()
        fecha_norm = normalizar_fecha(fecha_ia)
        _asegurar_fila(cursor, id_entrevista)
        cursor.execute(
            f"""
            UPDATE {NOMBRE_TABLA}
            SET comentario_ia = ?, fecha_ia = ?
            WHERE id_entrevista = ?
            """,
            (comentario_ia, fecha_norm, id_entrevista),
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al guardar comentario IA de entrevista: {e}")
        return False
    finally:
        conexion.close()


def obtener_comentario_ia(id_entrevista):
    crear_tabla_comentarios_ia_entrevista()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"""
            SELECT id, id_entrevista, comentario_ia, fecha_ia
            FROM {NOMBRE_TABLA}
            WHERE id_entrevista = ?
            """,
            (id_entrevista,),
        )
        return cursor.fetchone()
    finally:
        conexion.close()
