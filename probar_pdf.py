import argparse
import os
import sqlite3

from db.conexion import RUTA_DB
from models.entrevista import Entrevista
from models.interno import Interno
from models.solicitud import Solicitud


def obtener_solicitud(cursor, solicitud_id=None):
    if solicitud_id is not None:
        cursor.execute("SELECT * FROM solicitudes WHERE id = ?", (solicitud_id,))
    else:
        cursor.execute("SELECT * FROM solicitudes ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()


def cargar_solicitud_desde_fila(fila, cursor):
    solicitud = Solicitud()
    solicitud.id_solicitud = fila[0]
    solicitud.tipo = fila[2]
    solicitud.motivo = fila[3]
    solicitud.descripcion = fila[4]
    solicitud.urgencia = fila[5]
    solicitud.fecha_inicio = fila[6]
    solicitud.fecha_fin = fila[7]
    solicitud.hora_salida = fila[8]
    solicitud.hora_llegada = fila[9]
    solicitud.destino = fila[10]
    solicitud.provincia = fila[11]
    solicitud.direccion = fila[12]
    solicitud.cod_pos = fila[13]
    solicitud.nombre_cp = fila[14]
    solicitud.telf_cp = fila[15]
    solicitud.relacion_cp = fila[16]
    solicitud.direccion_cp = fila[17]
    solicitud.nombre_cs = fila[18]
    solicitud.telf_cs = fila[19]
    solicitud.relacion_cs = fila[20]
    solicitud.docs = fila[21]
    solicitud.compromisos = fila[22]
    solicitud.observaciones = fila[23]
    solicitud.conclusiones_profesional = fila[24]
    solicitud.id_profesional = fila[25]
    solicitud.estado = fila[26]

    cursor.execute("SELECT * FROM entrevistas WHERE id_solicitud = ?", (solicitud.id_solicitud,))
    entrevista_fila = cursor.fetchone()
    if entrevista_fila:
        solicitud.entrevista = Entrevista(
            id_entrevista=entrevista_fila[0],
            id_interno=entrevista_fila[1],
            fecha=entrevista_fila[3],
        )
        solicitud.entrevista.puntuacion = entrevista_fila[4]

    return solicitud


def cargar_interno_desde_rc(cursor, num_rc):
    cursor.execute("SELECT * FROM internos WHERE num_RC = ?", (num_rc,))
    interno_fila = cursor.fetchone()
    if not interno_fila:
        return None

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (interno_fila[1],))
    usuario_fila = cursor.fetchone()
    if not usuario_fila:
        return None

    return Interno(
        id_usuario=usuario_fila[0],
        nombre=usuario_fila[1],
        email=usuario_fila[2],
        contrasena=usuario_fila[3],
        rol=usuario_fila[4],
        num_RC=interno_fila[0],
        situacion_legal=interno_fila[2],
        delito=interno_fila[3],
        fecha_nac=interno_fila[5],
        condena=interno_fila[4],
        fecha_ingreso=interno_fila[6],
        modulo=interno_fila[7],
    )


def main():
    parser = argparse.ArgumentParser(description="Genera un PDF completo de solicitud sin iniciar la app.")
    parser.add_argument(
        "--solicitud-id",
        type=int,
        default=None,
        help="ID de solicitud a exportar. Si no se indica, usa la ultima solicitud.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Ruta del PDF de salida. Por defecto: Solicitud_<id>.pdf en el directorio actual.",
    )
    args = parser.parse_args()

    try:
        from utils.documentoPDF import DocumentoPDF
    except ModuleNotFoundError as exc:
        if exc.name == "reportlab":
            raise SystemExit(
                "Falta la dependencia 'reportlab'. Instala con: pip install reportlab"
            ) from exc
        raise

    if not os.path.exists(RUTA_DB):
        raise FileNotFoundError(f"No se encontro la base de datos: {RUTA_DB}")

    conn = sqlite3.connect(RUTA_DB)
    try:
        cursor = conn.cursor()
        solicitud_fila = obtener_solicitud(cursor, args.solicitud_id)
        if not solicitud_fila:
            raise ValueError("No se encontro ninguna solicitud para exportar.")

        solicitud = cargar_solicitud_desde_fila(solicitud_fila, cursor)
        interno = cargar_interno_desde_rc(cursor, solicitud_fila[1])
        if interno is None:
            raise ValueError(f"No se encontro el interno asociado a la solicitud {solicitud.id_solicitud}.")
    finally:
        conn.close()

    output = args.output or f"Solicitud_{solicitud.id_solicitud}.pdf"
    output = os.path.abspath(output)

    DocumentoPDF.generar_pdf_solicitud(solicitud, output, interno)
    print(f"PDF generado: {output}")


if __name__ == "__main__":
    main()
