from db.conexion import obtener_conexion


_CACHE_PONDERACIONES_RIESGO = None


def crear_tabla_ponderaciones_riesgo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ponderaciones_riesgo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pregunta INTEGER NOT NULL,
            nivel INTEGER NOT NULL,
            valor REAL NOT NULL,
            UNIQUE (id_pregunta, nivel)
        )
        """
    )
    conexion.commit()
    conexion.close()


def listar_ponderaciones_riesgo():
    crear_tabla_ponderaciones_riesgo()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT id_pregunta, nivel, valor
        FROM ponderaciones_riesgo
        ORDER BY id_pregunta ASC, nivel ASC
        """
    )
    filas = cursor.fetchall()
    conexion.close()
    return filas


def obtener_ponderaciones_riesgo_como_diccionario(force_refresh=False):
    global _CACHE_PONDERACIONES_RIESGO

    if _CACHE_PONDERACIONES_RIESGO is not None and not force_refresh:
        return _CACHE_PONDERACIONES_RIESGO

    filas = listar_ponderaciones_riesgo()
    ponderaciones = {}
    for id_pregunta, nivel, valor in filas:
        clave_pregunta = int(id_pregunta)
        if clave_pregunta not in ponderaciones:
            ponderaciones[clave_pregunta] = {}
        ponderaciones[clave_pregunta][int(nivel)] = float(valor)

    _CACHE_PONDERACIONES_RIESGO = ponderaciones
    return _CACHE_PONDERACIONES_RIESGO


def precargar_ponderaciones_riesgo():
    return obtener_ponderaciones_riesgo_como_diccionario(force_refresh=True)


def invalidar_cache_ponderaciones_riesgo():
    global _CACHE_PONDERACIONES_RIESGO
    _CACHE_PONDERACIONES_RIESGO = None
