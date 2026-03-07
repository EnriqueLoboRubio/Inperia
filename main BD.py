from db.usuario_db import *
from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *
from db.respuesta_db import *
from db.comentario_pregunta_db import *
from db.comentario_entrevista_db import *
from db.profesional_db import *
from db.pregunta_db import *
from db.conexion import obtener_conexion

from models.pregunta import Pregunta


def generar_usuarios():    
    agregar_usuario("Interno 1", "interno1@g.com", "1", "interno")
    agregar_usuario("Interno 2", "interno2@g.com", "2", "interno")
    agregar_usuario("Interno 3", "interno3@g.com", "3", "interno")
    agregar_usuario("Interno 4", "interno4@g.com", "4", "interno")
    agregar_usuario("Profesional 1", "prof1@g.com", "1", "profesional")
    agregar_usuario("Profesional 2", "prof2@g.com", "2", "profesional")


def generar_internos():
    u1 = encontrar_usuario_por_email("interno1@g.com")
    u2 = encontrar_usuario_por_email("interno2@g.com")
    u3 = encontrar_usuario_por_email("interno3@g.com")
    u4 = encontrar_usuario_por_email("interno4@g.com")

    agregar_interno(
        1, u1[0], "condenado", "Hurto", 3, "1991-04-12", "2024-01-10", "Mod A",
        lugar_nacimiento="Huelva",
        nombre_contacto_emergencia="Maria Torres",
        relacion_contacto_emergencia="madre",
        numero_contacto_emergencia="600111001",
    )
    agregar_interno(
        2, u2[0], "condenado", "Robo", 5, "1989-09-22", "2023-11-15", "Mod B",
        lugar_nacimiento="Sevilla",
        nombre_contacto_emergencia="Luis Gomez",
        relacion_contacto_emergencia="padre",
        numero_contacto_emergencia="600111002",
    )
    agregar_interno(
        3, u3[0], "provisional", "Estafa", 2, "1993-02-03", "2025-01-20", "Mod C",
        lugar_nacimiento="Cadiz",
        nombre_contacto_emergencia="Clara Ruiz",
        relacion_contacto_emergencia="hermana",
        numero_contacto_emergencia="600111003",
    )
    agregar_interno(
        4, u4[0], "condenado", "Lesiones", 4, "1987-12-30", "2022-07-01", "Mod D",
        lugar_nacimiento="Cordoba",
        nombre_contacto_emergencia="Pedro Martin",
        relacion_contacto_emergencia="tio",
        numero_contacto_emergencia="600111004",
    )


def generar_profesionales():
    prof1 = encontrar_usuario_por_email("prof1@g.com")
    prof2 = encontrar_usuario_por_email("prof2@g.com")

    id_prof1 = None
    id_prof2 = None

    if prof1:
        agregar_profesional(prof1[0], "COL-0001")
        id_prof1 = prof1[0]
    if prof2:
        agregar_profesional(prof2[0], "COL-0002")
        id_prof2 = prof2[0]

    return id_prof1, id_prof2


def _crear_solicitud_completa(id_interno, estado, fecha_base, id_profesional=None, conclusiones_profesional=""):
    return agregar_solicitud(
        id_interno=id_interno,
        tipo="familiar",
        motivo=f"Solicitud {estado} interno {id_interno}",
        descripcion="Salida temporal por motivo familiar con toda la documentacion.",
        urgencia="importante",
        fecha_creacion=fecha_base,
        fecha_inicio=fecha_base,
        fecha_fin=fecha_base,
        hora_salida="09:00",
        hora_llegada="18:00",
        destino="Huelva",
        provincia="Huelva",
        direccion="Calle Principal 10",
        cod_pos="21001",
        nombre_cp="Ana Contacto",
        telf_cp="600123123",
        relacion_cp="madre",
        direccion_cp="Calle Principal 10",
        nombre_cs="Juan Contacto",
        telf_cs="600456456",
        relacion_cs="padre",
        docs=7,
        compromiso=63,
        observaciones=f"Observaciones para estado {estado}",
        estado=estado,
        id_profesional=id_profesional,
        conclusiones_profesional=conclusiones_profesional,
    )


def _crear_respuestas_relleno(prefijo):
    preguntas = []
    for i in range(1, 11):
        p = Pregunta(i, f"{prefijo}: respuesta de la pregunta {i}")
        p.archivo_audio = None
        preguntas.append(p)
    return preguntas


def _crear_entrevista_con_respuestas(id_interno, id_solicitud, fecha, prefijo, puntuacion_global=None):
    respuestas = _crear_respuestas_relleno(prefijo)
    id_entrevista = agregar_entrevista_y_respuestas(id_interno, id_solicitud, fecha, respuestas)
    if id_entrevista and puntuacion_global is not None:
        actualizar_puntuacion_entrevista(id_entrevista, puntuacion_global)
    return id_entrevista


def _anadir_comentarios_preguntas(id_entrevista, id_profesional, fecha, prefijo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT id, id_pregunta
        FROM respuestas
        WHERE id_entrevista = ?
        ORDER BY id_pregunta
        LIMIT 3
        """,
        (id_entrevista,),
    )
    filas = cursor.fetchall()

    for id_respuesta, id_pregunta in filas:
        cursor.execute(
            """
            INSERT INTO comentarios_pre (id_respuesta, id_profesional, comentario, fecha)
            VALUES (?, ?, ?, ?)
            """,
            (id_respuesta, id_profesional, f"{prefijo} - comentario pregunta {id_pregunta}", fecha),
        )

    conexion.commit()
    conexion.close()


def generar_escenarios():
    prof1_id, prof2_id = generar_profesionales()

    # Interno 1: sin nada pendiente.
    # No se crean solicitudes para interno 1.

    # Interno 2: primero caso antiguo (aceptada), luego el mas reciente (pendiente).
    sol_i2_acep = _crear_solicitud_completa(
        2, "aceptada", "2025-02-10", id_profesional=prof1_id,
        conclusiones_profesional="Aprobada tras evaluacion completa del caso.",
    )
    ent_i2_acep = _crear_entrevista_con_respuestas(
        2, sol_i2_acep, "2025-02-11", "Interno 2 aceptada", puntuacion_global=944.0
    )
    agregar_comentario_ia(ent_i2_acep, prof1_id, "IA: riesgo bajo y buena coherencia narrativa.", "2025-02-12")
    agregar_comentario_profesional(ent_i2_acep, prof1_id, "Profesional: apto para permiso solicitado.", "2025-02-12")
    _anadir_comentarios_preguntas(ent_i2_acep, prof1_id, "2025-02-12", "Interno 2 aceptada")

    sol_i2_pend = _crear_solicitud_completa(2, "pendiente", "2026-03-01")
    _crear_entrevista_con_respuestas(
        2, sol_i2_pend, "2026-03-01", "Interno 2 pendiente", puntuacion_global=918.0
    )

    # Interno 3: primero caso antiguo (rechazada), luego el mas reciente (pendiente).
    sol_i3_rech = _crear_solicitud_completa(
        3, "rechazada", "2026-02-05", id_profesional=prof1_id,
        conclusiones_profesional="Rechazada por inconsistencias en la justificacion.",
    )
    ent_i3_rech = _crear_entrevista_con_respuestas(
        3, sol_i3_rech, "2026-02-06", "Interno 3 rechazada", puntuacion_global=989.0
    )
    agregar_comentario_ia(ent_i3_rech, prof1_id, "IA: detecta contradicciones relevantes en respuestas.", "2026-02-07")
    agregar_comentario_profesional(ent_i3_rech, prof1_id, "Profesional: no procede autorizacion.", "2026-02-07")
    _anadir_comentarios_preguntas(ent_i3_rech, prof1_id, "2026-02-07", "Interno 3 rechazada")

    sol_i3_pend = _crear_solicitud_completa(3, "pendiente", "2026-03-02", id_profesional=prof2_id)
    _crear_entrevista_con_respuestas(
        3, sol_i3_pend, "2026-03-02", "Interno 3 pendiente", puntuacion_global=930.0
    )

    # Interno 4: solicitud completa sin entrevista y sin profesional asignado.
    _crear_solicitud_completa(
        4, "iniciada", "2026-01-20", id_profesional=None,
        conclusiones_profesional="",
    )


def reiniciar_base_de_datos():
    print("Borrando tablas antiguas...")
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS comentarios_pre")
    cursor.execute("DROP TABLE IF EXISTS comentarios_ent")
    conexion.commit()
    conexion.close()

    borrar_respuestas()
    borrar_entrevistas()
    borrar_solicitudes()
    eliminar_profesional()
    borrar_internos()
    borrar_usuarios()
    print("Tablas borradas con exito.")

    print("Creando nuevas tablas...")
    crear_usuario()
    crear_interno()
    crear_profesional()
    crear_respuesta()
    crear_comentario_pre()
    crear_comentario_ent()
    crear_solicitud()
    crear_entrevista()
    crear_pregunta()
    print("Base de datos reconstruida completamente.")


def imprimir_resumen_bd():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    print("\n===== RESUMEN BD =====")
    for tabla in ["usuarios", "internos", "profesionales", "solicitudes", "entrevistas", "respuestas", "comentarios_ent", "comentarios_pre"]:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        total = cursor.fetchone()[0]
        print(f"{tabla}: {total}")

    print("\nSolicitudes por interno y estado:")
    cursor.execute(
        """
        SELECT id_interno, estado, COUNT(*)
        FROM solicitudes
        GROUP BY id_interno, estado
        ORDER BY id_interno, estado
        """
    )
    for fila in cursor.fetchall():
        print(f"  interno {fila[0]} -> {fila[1]}: {fila[2]}")

    print("\nUsuarios creados:")
    cursor.execute("SELECT id, nombre, email, rol FROM usuarios ORDER BY id")
    for fila in cursor.fetchall():
        print(f"  id={fila[0]} | {fila[1]} | {fila[2]} | rol={fila[3]}")

    conexion.close()


def reiniciar_y_generar():
    reiniciar_base_de_datos()
    cargar_preguntas_desde_json()
    generar_usuarios()
    generar_internos()
    generar_escenarios()
    imprimir_resumen_bd()


if __name__ == "__main__":
    reiniciar_y_generar()
