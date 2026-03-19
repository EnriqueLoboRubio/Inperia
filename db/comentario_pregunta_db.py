from datetime import datetime

from db.conexion import obtener_conexion


def crear_comentario_pre():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comentarios_pre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_respuesta INTEGER NOT NULL,
            id_profesional INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (id_respuesta) REFERENCES respuestas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_profesional) REFERENCES profesionales(id_usuario) ON DELETE RESTRICT
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_coment_pre_respuesta
        ON comentarios_pre(id_respuesta)
        """
    )

    conexion.commit()
    conexion.close()


def listar_comentarios_respuesta(id_respuesta):
    crear_comentario_pre()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT id, id_respuesta, id_profesional, comentario, fecha
            FROM comentarios_pre
            WHERE id_respuesta = ?
            ORDER BY fecha ASC, id ASC
            """,
            (id_respuesta,),
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def agregar_comentario_respuesta(id_respuesta, id_profesional, comentario, fecha=None):
    crear_comentario_pre()
    texto = str(comentario or "").strip()
    if not texto:
        return None
    fecha_txt = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO comentarios_pre (id_respuesta, id_profesional, comentario, fecha)
            VALUES (?, ?, ?, ?)
            """,
            (id_respuesta, id_profesional, texto, fecha_txt),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()


def eliminar_comentario_respuesta(id_comentario, id_profesional=None):
    crear_comentario_pre()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        if id_profesional is None:
            cursor.execute(
                "DELETE FROM comentarios_pre WHERE id = ?",
                (id_comentario,),
            )
        else:
            cursor.execute(
                """
                DELETE FROM comentarios_pre
                WHERE id = ? AND id_profesional = ?
                """,
                (id_comentario, id_profesional),
            )
        conexion.commit()
        return cursor.rowcount > 0
    finally:
        conexion.close()


def reemplazar_comentarios_respuesta(id_respuesta, comentarios):
    crear_comentario_pre()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM comentarios_pre
            WHERE id_respuesta = ?
            """,
            (id_respuesta,),
        )

        for comentario in list(comentarios or []):
            texto = str(comentario.get("comentario", "") or "").strip()
            if not texto:
                continue
            cursor.execute(
                """
                INSERT INTO comentarios_pre (id_respuesta, id_profesional, comentario, fecha)
                VALUES (?, ?, ?, ?)
                """,
                (
                    id_respuesta,
                    comentario.get("id_profesional"),
                    texto,
                    str(comentario.get("fecha", "") or "").strip(),
                ),
            )

        conexion.commit()
        return True
    finally:
        conexion.close()
