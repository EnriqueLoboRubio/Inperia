from datetime import datetime

from db.conexion import obtener_conexion


def crear_tabla_comentarios_entrevista_mensajes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comentarios_entrevista_mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entrevista INTEGER NOT NULL,
            id_profesional INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_profesional) REFERENCES profesionales(id_usuario) ON DELETE RESTRICT
        )
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_coment_mensajes_entrevista
        ON comentarios_entrevista_mensajes(id_entrevista)
        """
    )
    conexion.commit()
    conexion.close()


def listar_comentarios_entrevista(id_entrevista):
    crear_tabla_comentarios_entrevista_mensajes()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT id, id_entrevista, id_profesional, comentario, fecha_creacion
            FROM comentarios_entrevista_mensajes
            WHERE id_entrevista = ?
            ORDER BY fecha_creacion ASC, id ASC
            """,
            (id_entrevista,),
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def agregar_comentario_entrevista(id_entrevista, id_profesional, comentario, fecha_creacion=None):
    crear_tabla_comentarios_entrevista_mensajes()
    texto = str(comentario or "").strip()
    if not texto:
        return None

    fecha = fecha_creacion or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO comentarios_entrevista_mensajes
            (id_entrevista, id_profesional, comentario, fecha_creacion)
            VALUES (?, ?, ?, ?)
            """,
            (id_entrevista, id_profesional, texto, fecha),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()


def eliminar_comentario_entrevista(id_comentario, id_profesional=None):
    crear_tabla_comentarios_entrevista_mensajes()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        if id_profesional is None:
            cursor.execute(
                "DELETE FROM comentarios_entrevista_mensajes WHERE id = ?",
                (id_comentario,),
            )
        else:
            cursor.execute(
                """
                DELETE FROM comentarios_entrevista_mensajes
                WHERE id = ? AND id_profesional = ?
                """,
                (id_comentario, id_profesional),
            )
        conexion.commit()
        return cursor.rowcount > 0
    finally:
        conexion.close()


def reemplazar_comentarios_entrevista(id_entrevista, comentarios):
    crear_tabla_comentarios_entrevista_mensajes()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM comentarios_entrevista_mensajes
            WHERE id_entrevista = ?
            """,
            (id_entrevista,),
        )

        for comentario in list(comentarios or []):
            texto = str(comentario.get("comentario", "") or "").strip()
            if not texto:
                continue
            cursor.execute(
                """
                INSERT INTO comentarios_entrevista_mensajes
                (id_entrevista, id_profesional, comentario, fecha_creacion)
                VALUES (?, ?, ?, ?)
                """,
                (
                    id_entrevista,
                    comentario.get("id_profesional"),
                    texto,
                    str(comentario.get("fecha", "") or comentario.get("fecha_creacion", "") or "").strip(),
                ),
            )

        conexion.commit()
        return True
    finally:
        conexion.close()
