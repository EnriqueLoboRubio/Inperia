import json
from pathlib import Path

from db.conexion import obtener_conexion
from db.pregunta_db import crear_pregunta


RUTA_PREGUNTAS_JSON = Path(__file__).resolve().parent.parent / "data" / "preguntas.json"


def _cargar_preguntas_desde_json(ruta_json=RUTA_PREGUNTAS_JSON):
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    preguntas = []
    for clave, contenido in data.items():
        if not str(clave).isdigit():
            continue
        id_pregunta = int(clave)
        titulo = str(contenido.get("titulo", f"Pregunta {id_pregunta}"))
        texto = str(contenido.get("texto", ""))
        cantidad_niveles = int(contenido.get("cantidad_niveles", 0) or 0)
        preguntas.append((id_pregunta, titulo, texto, cantidad_niveles))
    return preguntas


def iniciar_preguntas_seed(force=False):
    """
    Data seeding idempotente para preguntas.
    Solo inserta si la tabla esta vacia (salvo force=True).
    """
    crear_pregunta()

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM preguntas")
    total = cursor.fetchone()[0]

    if total > 0 and not force:
        conexion.close()
        return 0

    preguntas = _cargar_preguntas_desde_json()

    cursor.executemany(
        """
        INSERT INTO preguntas (id, titulo, texto, cantidad_niveles)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            titulo = excluded.titulo,
            texto = excluded.texto,
            cantidad_niveles = excluded.cantidad_niveles
        """,
        preguntas,
    )

    conexion.commit()
    conexion.close()
    return len(preguntas)
