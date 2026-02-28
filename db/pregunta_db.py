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
            texto TEXT NOT NULL
        )
        """
    )
    conexion.commit()
    conexion.close()


def insertar_o_actualizar_pregunta(id_pregunta, titulo, texto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO preguntas (id, titulo, texto)
        VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            titulo = excluded.titulo,
            texto = excluded.texto
        """,
        (id_pregunta, titulo, texto),
    )
    conexion.commit()
    conexion.close()


def obtener_preguntas_como_diccionario():
    crear_pregunta()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, texto FROM preguntas ORDER BY id")
    filas = cursor.fetchall()
    conexion.close()

    if not filas:
        cargar_preguntas_desde_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, titulo, texto FROM preguntas ORDER BY id")
        filas = cursor.fetchall()
        conexion.close()

    if not filas:
        return {"1": {"titulo": "Error", "texto": "No hay preguntas en base de datos."}}

    preguntas = {}
    for fila in filas:
        preguntas[str(fila[0])] = {"titulo": fila[1], "texto": fila[2]}
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
        insertar_o_actualizar_pregunta(id_pregunta, titulo, texto)

    return True
