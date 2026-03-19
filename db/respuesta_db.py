import sqlite3
from db.conexion import obtener_conexion

# -------------------------------- RESPUESTA ------------------------------- #

_DDL_RESPUESTAS = """
    CREATE TABLE IF NOT EXISTS respuestas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevista INTEGER NOT NULL,
        id_pregunta INTEGER NOT NULL,
        texto_respuesta TEXT,
        ruta_audio TEXT,
        nivel_ia INTEGER,
        analisis_ia TEXT,
        nivel_profesional INTEGER,
        FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id) ON DELETE CASCADE,
        FOREIGN KEY (id_pregunta) REFERENCES preguntas(id) ON DELETE RESTRICT
    )
"""



def crear_respuesta():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(_DDL_RESPUESTAS)
    cursor.execute("PRAGMA table_info(respuestas)")
    columnas = {fila[1] for fila in cursor.fetchall()}
    if "analisis_ia" not in columnas:
        cursor.execute(
            """
            ALTER TABLE respuestas
            ADD COLUMN analisis_ia TEXT
            """
        )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_resp_entrevista_pregunta
        ON respuestas(id_entrevista, id_pregunta)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_resp_entrevista
        ON respuestas(id_entrevista)
        """
    )

    conexion.commit()
    conexion.close()


def agregar_respuesta(id_entrevista, id_pregunta, texto_respuesta, ruta_audio, *args):
    crear_respuesta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO respuestas (id_entrevista, id_pregunta, texto_respuesta, ruta_audio)
            VALUES (?,?,?,?)
            """,
            (id_entrevista, id_pregunta, texto_respuesta, ruta_audio),
        )
    except sqlite3.IntegrityError:
        print("ERror: No se ha podido crear la respuesta")
        return False

    conexion.commit()
    conexion.close()
    return True


def actualizar_puntuacion_respuesta(id_entrevista, id_pregunta, *args):
    """
    Compatibilidad:
    - Nuevo: actualizar_puntuacion_respuesta(id_entrevista, id_pregunta, nivel_ia)
    - Antiguo: actualizar_puntuacion_respuesta(id_entrevista, id_pregunta, _, nivel_ia)
    """
    if len(args) == 1:
        nivel_ia = args[0]
    elif len(args) >= 2:
        nivel_ia = args[1]
    else:
        print("Error al actualizar: falta nivel_ia")
        return False

    crear_respuesta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE respuestas
            SET nivel_ia = ?
            WHERE id_entrevista = ? AND id_pregunta = ?
            """,
            (nivel_ia, id_entrevista, id_pregunta),
        )

        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
    finally:
        conexion.close()


def actualizar_analisis_ia_respuesta(id_entrevista, id_pregunta, nivel_ia, analisis_ia):
    crear_respuesta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE respuestas
            SET nivel_ia = ?, analisis_ia = ?
            WHERE id_entrevista = ? AND id_pregunta = ?
            """,
            (nivel_ia, str(analisis_ia or "").strip(), id_entrevista, id_pregunta),
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar analisis IA de respuesta: {e}")
        return False
    finally:
        conexion.close()


def actualizar_nivel_profesional_respuesta(id_entrevista, id_pregunta, nivel_profesional):
    crear_respuesta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE respuestas
            SET nivel_profesional = ?
            WHERE id_entrevista = ? AND id_pregunta = ?
            """,
            (nivel_profesional, id_entrevista, id_pregunta),
        )
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar nivel profesional: {e}")
        return False
    finally:
        conexion.close()


def obtener_respuestas_por_entrevista(id_entrevista):
    """
    Recupera todas las respuestas asociadas a una entrevista.
    Devuelve una lista de diccionarios con los datos.
    """
    crear_respuesta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT id, id_pregunta, texto_respuesta, ruta_audio, nivel_ia, analisis_ia, nivel_profesional
            FROM respuestas
            WHERE id_entrevista = ?
            """,
            (id_entrevista,),
        )

        filas = cursor.fetchall()
        lista_respuestas = []

        for fila in filas:
            datos = {
                "id_respuesta": fila[0],
                "id_pregunta": fila[1],
                "texto_respuesta": fila[2],
                "ruta_audio": fila[3],
                "nivel_ia": fila[4],
                "analisis_ia": fila[5],
                "nivel_profesional": fila[6],
            }
            lista_respuestas.append(datos)

        return lista_respuestas

    except Exception as e:
        print(f"Error al obtener respuestas: {e}")
        return []
    finally:
        conexion.close()


def borrar_respuestas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS respuestas")
    conexion.commit()
    conexion.close()

