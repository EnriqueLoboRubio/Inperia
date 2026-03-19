import json
import os

from db.conexion import obtener_conexion


def crear_pregunta():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            texto TEXT NOT NULL,
            cantidad_niveles INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    cursor.execute("PRAGMA table_info(preguntas)")
    columnas = {fila[1] for fila in cursor.fetchall()}
    if "cantidad_niveles" not in columnas:
        cursor.execute(
            """
            ALTER TABLE preguntas
            ADD COLUMN cantidad_niveles INTEGER NOT NULL DEFAULT 0
            """
        )
    conexion.commit()
    conexion.close()


def insertar_o_actualizar_pregunta(id_pregunta, titulo, texto, cantidad_niveles=0):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO preguntas (id, titulo, texto, cantidad_niveles)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            titulo = excluded.titulo,
            texto = excluded.texto,
            cantidad_niveles = excluded.cantidad_niveles
        """,
        (id_pregunta, titulo, texto, int(cantidad_niveles or 0)),
    )
    conexion.commit()
    conexion.close()


def actualizar_cantidad_niveles_pregunta(id_pregunta, cantidad_niveles):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE preguntas
        SET cantidad_niveles = ?
        WHERE id = ?
        """,
        (int(cantidad_niveles or 0), int(id_pregunta)),
    )
    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()
    return actualizado


def obtener_preguntas_como_diccionario():
    crear_pregunta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, texto, cantidad_niveles FROM preguntas ORDER BY id")
    filas = cursor.fetchall()
    conexion.close()

    necesita_recarga = any(int(fila[3] or 0) <= 0 for fila in filas)
    if filas and necesita_recarga:
        cargar_preguntas_desde_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, titulo, texto, cantidad_niveles FROM preguntas ORDER BY id")
        filas = cursor.fetchall()
        conexion.close()

    if not filas:
        cargar_preguntas_desde_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, titulo, texto, cantidad_niveles FROM preguntas ORDER BY id")
        filas = cursor.fetchall()
        conexion.close()

    if not filas:
        return {"1": {"titulo": "Error", "texto": "No hay preguntas en base de datos.", "cantidad_niveles": 0}}

    preguntas = {}
    for fila in filas:
        preguntas[str(fila[0])] = {
            "titulo": fila[1],
            "texto": fila[2],
            "cantidad_niveles": int(fila[3] or 0),
        }
    return preguntas


def cargar_preguntas_desde_json(ruta_json=None):
    if ruta_json is None:
        ruta_base = os.path.dirname(os.path.dirname(__file__))
        ruta_json = os.path.join(ruta_base, "data", "preguntas.json")

    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error cargando preguntas.json: {e}")
        return False

    for clave, contenido in data.items():
        try:
            id_pregunta = int(clave)
        except ValueError:
            continue

        titulo = str(contenido.get("titulo", f"Pregunta {id_pregunta}"))
        texto = str(contenido.get("texto", ""))
        cantidad_niveles = int(contenido.get("cantidad_niveles", 0) or 0)
        insertar_o_actualizar_pregunta(id_pregunta, titulo, texto, cantidad_niveles)

    return True
