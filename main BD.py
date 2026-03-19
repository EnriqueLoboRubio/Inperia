from db.usuario_db import *
from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *
from db.respuesta_db import *
from db.comentario_pregunta_db import *
from db.comentario_ia_entrevista_db import *
from db.profesional_db import *
from db.pregunta_db import *
from db.prompt_db import *
from db.inicio_preguntas import iniciar_preguntas_seed
from db.inicio_prompts import iniciar_prompts_seed
from db.conexion import obtener_conexion

from models.pregunta import Pregunta


def generar_usuarios():    
    agregar_usuario("Interno 1", "interno1@g.com", "1", "interno")
    agregar_usuario("Interno 2", "interno2@g.com", "2", "interno")
    agregar_usuario("Interno 3", "interno3@g.com", "3", "interno")
    agregar_usuario("Interno 4", "interno4@g.com", "4", "interno")
    agregar_usuario("Profesional 1", "prof1@g.com", "1", "profesional")
    agregar_usuario("Profesional 2", "prof2@g.com", "2", "profesional")
    agregar_usuario("Admin", "admin@g.com", "admin", "administrador")


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


def _crear_entrevista_con_respuestas(id_interno, id_solicitud, fecha, prefijo, puntuacion_ia=None, respuestas=None):
    respuestas = respuestas if respuestas is not None else _crear_respuestas_relleno(prefijo)
    id_entrevista = agregar_entrevista_y_respuestas(id_interno, id_solicitud, fecha, respuestas)
    if id_entrevista and puntuacion_ia is not None:
        actualizar_puntuacion_entrevista(id_entrevista, puntuacion_ia)
    return id_entrevista


def _anadir_comentarios_preguntas(id_entrevista, id_profesional, fecha, prefijo, limite=3):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        SELECT id, id_pregunta
        FROM respuestas
        WHERE id_entrevista = ?
        ORDER BY id_pregunta
    """
    if limite is not None:
        query += f" LIMIT {int(limite)}"
    cursor.execute(query, (id_entrevista,))
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


def _actualizar_niveles_respuestas(id_entrevista, niveles_ia, niveles_prof):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        for id_pregunta in range(1, 11):
            nivel_ia = niveles_ia[id_pregunta - 1]
            nivel_prof = niveles_prof[id_pregunta - 1]
            cursor.execute(
                """
                UPDATE respuestas
                SET nivel_ia = ?, nivel_profesional = ?
                WHERE id_entrevista = ? AND id_pregunta = ?
                """,
                (nivel_ia, nivel_prof, id_entrevista, id_pregunta),
            )
        conexion.commit()
    finally:
        conexion.close()


def _respuestas_realistas_interno1_rechazada():
    textos = [
        "Llevo tiempo sin conflictos y quiero salir para ver a mi hijo, pero no he podido traer todos los justificantes originales.",
        "Me comprometo a volver a las 18:00, aunque reconozco que otras veces llegué con retraso por problemas de transporte.",
        "El domicilio de destino es el de mi primo en Huelva, pero no tengo contrato de alquiler ni autorización firmada del propietario.",
        "Mi contacto principal es mi hermana, pero actualmente está fuera de España y no puede acompañarme durante el permiso.",
        "No tengo cita médica oficial para ese día; quería aprovechar para resolver asuntos personales y familiares.",
        "La documentación laboral está en trámite, todavía no me han entregado el certificado final de la empresa.",
        "Durante la entrevista me he puesto nervioso y no recordé fechas exactas de permisos anteriores.",
        "Admito que en un permiso anterior consumí alcohol, aunque no cometí ninguna infracción grave según mi versión.",
        "Estoy dispuesto a cumplir condiciones estrictas, pero no puedo asegurar contacto telefónico continuo durante toda la salida.",
        "Mi objetivo es retomar la relación familiar, pero entiendo que faltan garantías y pruebas suficientes para autorizar la salida.",
    ]
    respuestas = []
    for i, texto in enumerate(textos, start=1):
        p = Pregunta(i, texto)
        p.archivo_audio = None
        respuestas.append(p)
    return respuestas


def generar_escenarios():
    prof1_id, prof2_id = generar_profesionales()

    # Interno 1: solicitud rechazada completa, asignada al profesional 1, con entrevista y comentarios.
    sol_i1_rech = _crear_solicitud_completa(
        1, "rechazada", "2026-02-18", id_profesional=prof1_id,
        conclusiones_profesional=(
            "Solicitud rechazada por inconsistencias relevantes entre declaración y documentos aportados, "
            "falta de acreditación del destino y ausencia de garantías de control durante la salida."
        ),
    )
    ent_i1_rech = _crear_entrevista_con_respuestas(
        1,
        sol_i1_rech,
        "2026-02-19",
        "Interno 1 rechazada",
        puntuacion_ia=987.4,
        respuestas=_respuestas_realistas_interno1_rechazada(),
    )
    # Niveles de IA y profesional para las 10 preguntas.
    _actualizar_niveles_respuestas(
        ent_i1_rech,
        niveles_ia=[3, 2, 1, 1, 3, 1, 1, 1, 1, 1],
        niveles_prof=[2, 2, 1, 1, 2, 1, 1, 1, 1, 1],
    )
    agregar_comentario_ia(
        ent_i1_rech,
        "IA: patrón de riesgo alto por contradicciones, soporte documental insuficiente y baja fiabilidad en compromisos operativos.",
        "2026-02-20",
    )
    _anadir_comentarios_preguntas(
        ent_i1_rech,
        prof1_id,
        "2026-02-20",
        "Interno 1 rechazada",
        limite=10,
    )

    # Interno 2: primero caso antiguo (aceptada), luego el mas reciente (pendiente).
    sol_i2_acep = _crear_solicitud_completa(
        2, "aceptada", "2025-02-10", id_profesional=prof1_id,
        conclusiones_profesional="Aprobada tras evaluacion completa del caso.",
    )
    ent_i2_acep = _crear_entrevista_con_respuestas(
        2, sol_i2_acep, "2025-02-11", "Interno 2 aceptada", puntuacion_ia=944.0
    )
    agregar_comentario_ia(ent_i2_acep, "IA: riesgo bajo y buena coherencia narrativa.", "2025-02-12")
    _anadir_comentarios_preguntas(ent_i2_acep, prof1_id, "2025-02-12", "Interno 2 aceptada")

    sol_i2_pend = _crear_solicitud_completa(2, "pendiente", "2026-03-01")
    _crear_entrevista_con_respuestas(
        2, sol_i2_pend, "2026-03-01", "Interno 2 pendiente", puntuacion_ia=918.0
    )

    # Interno 3: primero caso antiguo (rechazada), luego el mas reciente (pendiente).
    sol_i3_rech = _crear_solicitud_completa(
        3, "rechazada", "2026-02-05", id_profesional=prof1_id,
        conclusiones_profesional="Rechazada por inconsistencias en la justificacion.",
    )
    ent_i3_rech = _crear_entrevista_con_respuestas(
        3, sol_i3_rech, "2026-02-06", "Interno 3 rechazada", puntuacion_ia=989.0
    )
    agregar_comentario_ia(ent_i3_rech, "IA: detecta contradicciones relevantes en respuestas.", "2026-02-07")
    _anadir_comentarios_preguntas(ent_i3_rech, prof1_id, "2026-02-07", "Interno 3 rechazada")

    sol_i3_pend = _crear_solicitud_completa(3, "pendiente", "2026-03-02", id_profesional=prof2_id)
    _crear_entrevista_con_respuestas(
        3, sol_i3_pend, "2026-03-02", "Interno 3 pendiente", puntuacion_ia=930.0
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
    cursor.execute("DROP TABLE IF EXISTS prompts")
    cursor.execute("DROP TABLE IF EXISTS comentarios_ent")
    cursor.execute("DROP TABLE IF EXISTS comentarios_ia_ent")
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
    crear_tabla_comentarios_ia_entrevista()
    crear_solicitud()
    crear_entrevista()
    crear_pregunta()
    crear_prompt()
    print("Base de datos reconstruida completamente.")


def imprimir_resumen_bd():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    print("\n===== RESUMEN BD =====")
    for tabla in ["usuarios", "internos", "profesionales", "solicitudes", "entrevistas", "respuestas", "comentarios_ia_ent", "comentarios_pre", "prompts"]:
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
    iniciar_preguntas_seed(force=True)
    iniciar_prompts_seed(force=True)
    generar_usuarios()
    generar_profesionales()
    generar_internos()
    generar_escenarios()
    imprimir_resumen_bd()


if __name__ == "__main__":
    reiniciar_y_generar()


