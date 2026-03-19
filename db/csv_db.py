import csv
import os

from db.conexion import RUTA_DB
from db.conexion import obtener_conexion


EXCLUDED_TABLES = {"sqlite_sequence"}


def listar_tablas_exportables():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        return [
            fila[0]
            for fila in cursor.fetchall()
            if fila and fila[0] not in EXCLUDED_TABLES
        ]
    finally:
        conexion.close()


def _obtener_columnas(cursor, tabla):
    cursor.execute(f"PRAGMA table_info({tabla})")
    return [fila[1] for fila in cursor.fetchall()]


def _mapa_dependencias(cursor, tablas):
    dependencias = {tabla: set() for tabla in tablas}
    for tabla in tablas:
        cursor.execute(f"PRAGMA foreign_key_list({tabla})")
        for fila in cursor.fetchall():
            tabla_referenciada = fila[2]
            if tabla_referenciada in dependencias:
                dependencias[tabla].add(tabla_referenciada)
    return dependencias


def orden_topologico(tablas, dependencias):
    pendientes = {tabla: set(refs) for tabla, refs in dependencias.items()}
    resultado = []
    libres = sorted([tabla for tabla in tablas if not pendientes.get(tabla)])

    while libres:
        actual = libres.pop(0)
        resultado.append(actual)
        for tabla in tablas:
            refs = pendientes.get(tabla)
            if actual in refs:
                refs.remove(actual)
                if not refs and tabla not in resultado and tabla not in libres:
                    libres.append(tabla)
                    libres.sort()

    restantes = [tabla for tabla in tablas if tabla not in resultado]
    return resultado + sorted(restantes)


def obtener_tablas_en_orden_importacion():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        tablas = listar_tablas_exportables()
        dependencias = _mapa_dependencias(cursor, tablas)
        return orden_topologico(tablas, dependencias)
    finally:
        conexion.close()


def exportar_base_datos_a_csv(carpeta_destino):
    if not carpeta_destino:
        raise ValueError("Debe indicar una carpeta de destino.")

    os.makedirs(carpeta_destino, exist_ok=True)
    conexion = obtener_conexion()
    resumen = []
    try:
        cursor = conexion.cursor()
        tablas = listar_tablas_exportables()
        for tabla in tablas:
            columnas = _obtener_columnas(cursor, tabla)
            ruta_csv = os.path.join(carpeta_destino, f"{tabla}.csv")
            cursor.execute(f"SELECT * FROM {tabla}")
            filas = cursor.fetchall()

            with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerow(columnas)
                escritor.writerows(filas)

            resumen.append(
                {
                    "tabla": tabla,
                    "filas": len(filas),
                    "ruta": ruta_csv,
                }
            )
        return resumen
    finally:
        conexion.close()


def importar_base_datos_desde_csv(carpeta_origen):
    if not carpeta_origen or not os.path.isdir(carpeta_origen):
        raise ValueError("La carpeta de importación no es válida.")

    conexion = obtener_conexion()
    resumen = []
    try:
        cursor = conexion.cursor()
        tablas = obtener_tablas_en_orden_importacion()

        datos_por_tabla = {}
        for tabla in tablas:
            ruta_csv = os.path.join(carpeta_origen, f"{tabla}.csv")
            if not os.path.exists(ruta_csv):
                continue

            with open(ruta_csv, "r", newline="", encoding="utf-8-sig") as archivo_csv:
                lector = csv.reader(archivo_csv)
                try:
                    cabecera = next(lector)
                except StopIteration:
                    cabecera = []
                    filas = []
                else:
                    filas = [fila for fila in lector]

            columnas_reales = _obtener_columnas(cursor, tabla)
            if cabecera != columnas_reales:
                raise ValueError(
                    f"El CSV de la tabla '{tabla}' no coincide con la estructura actual."
                )

            datos_por_tabla[tabla] = {
                "columnas": cabecera,
                "filas": filas,
                "ruta": ruta_csv,
            }

        if not datos_por_tabla:
            raise ValueError("No se ha encontrado ningún CSV válido para importar.")

        conexion.execute("PRAGMA foreign_keys = OFF")
        conexion.execute("BEGIN")

        for tabla in reversed(tablas):
            if tabla in datos_por_tabla:
                cursor.execute(f"DELETE FROM {tabla}")

        for tabla in tablas:
            if tabla not in datos_por_tabla:
                continue

            info = datos_por_tabla[tabla]
            columnas = info["columnas"]
            filas = info["filas"]
            if filas:
                placeholders = ", ".join(["?"] * len(columnas))
                columnas_sql = ", ".join(columnas)
                cursor.executemany(
                    f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({placeholders})",
                    filas,
                )

            resumen.append(
                {
                    "tabla": tabla,
                    "filas": len(filas),
                    "ruta": info["ruta"],
                }
            )

        conexion.commit()
        return resumen
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.close()


def obtener_resumen_csv():
    return {
        "ruta_db": RUTA_DB,
        "tablas": listar_tablas_exportables(),
    }
