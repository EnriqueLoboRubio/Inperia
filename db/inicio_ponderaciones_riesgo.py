from db.conexion import obtener_conexion
from db.riesgo_ponderacion_db import (
    crear_tabla_ponderaciones_riesgo,
    invalidar_cache_ponderaciones_riesgo,
)


PONDERACIONES_RIESGO_SEMILLA = [
    (1, 0, 1.5435),
    (1, 1, 3.0870),
    (1, 2, 4.6305),
    (1, 3, 6.1740),
    (2, 0, 0.3338),
    (2, 1, 0.6676),
    (2, 2, 1.0014),
    (3, 0, 0.2507),
    (3, 1, 0.5014),
    (4, 0, 0.2364),
    (4, 1, 0.4728),
    (5, 0, 1.1522),
    (5, 1, 2.3044),
    (5, 2, 3.4566),
    (5, 3, 4.6088),
    (6, 0, 0.3071),
    (6, 1, 0.6142),
    (7, 0, 0.3979),
    (7, 1, 0.7958),
    (8, 0, 0.3523),
    (8, 1, 0.7046),
    (9, 0, 0.3271),
    (9, 1, 0.6542),
    (10, 0, 0.3656),
    (10, 1, 0.7312),
]


def iniciar_ponderaciones_riesgo_seed(force=False):
    crear_tabla_ponderaciones_riesgo()

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM ponderaciones_riesgo")
    total = cursor.fetchone()[0]

    if total > 0 and not force:
        conexion.close()
        return 0

    cursor.executemany(
        """
        INSERT INTO ponderaciones_riesgo (id_pregunta, nivel, valor)
        VALUES (?, ?, ?)
        ON CONFLICT(id_pregunta, nivel) DO UPDATE SET
            valor = excluded.valor
        """,
        PONDERACIONES_RIESGO_SEMILLA,
    )

    conexion.commit()
    conexion.close()
    invalidar_cache_ponderaciones_riesgo()
    return len(PONDERACIONES_RIESGO_SEMILLA)
