import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.pantalla_perfil_interno_profesional import PantallaPerfilInternoProfesional
from models.interno import Interno


def _solicitud_fila(
    id_solicitud,
    id_interno,
    tipo,
    motivo,
    fecha_creacion,
    estado,
    id_profesional,
):
    # Estructura compatible con la tabla solicitudes (28 columnas).
    return (
        id_solicitud,          # 0 id
        id_interno,            # 1 id_interno
        tipo,                  # 2 tipo
        motivo,                # 3 motivo
        "Descripcion demo",    # 4 descripcion
        "importante",          # 5 urgencia
        fecha_creacion,        # 6 fecha_creacion
        fecha_creacion,        # 7 fecha_inicio
        fecha_creacion,        # 8 fecha_fin
        "09:00",               # 9 hora_salida
        "18:00",               # 10 hora_llegada
        "Huelva",              # 11 destino
        "Huelva",              # 12 provincia
        "Calle Demo 10",       # 13 direccion
        "21001",               # 14 cod_pos
        "Contacto 1",          # 15 nombre_cp
        "600000001",           # 16 telf_cp
        "madre",               # 17 relacion_cp
        "Calle Demo 10",       # 18 direccion_cp
        "Contacto 2",          # 19 nombre_cs
        "600000002",           # 20 telf_cs
        "padre",               # 21 relacion_cs
        7,                     # 22 docs
        63,                    # 23 compromiso
        "Observaciones demo",  # 24 observaciones
        "",                    # 25 conclusiones_profesional
        id_profesional,        # 26 id_profesional
        estado,                # 27 estado
    )


def main():
    app = QApplication(sys.argv)

    ventana = QMainWindow()
    ventana.setWindowTitle("Test - Perfil Interno (Profesional)")
    ventana.resize(1300, 820)

    pantalla = PantallaPerfilInternoProfesional()

    interno = Interno(
        id_usuario=2,
        nombre="Interno Demo",
        email="interno.demo@inperia.local",
        contrasena="x",
        rol="interno",
        num_RC=2021,
        situacion_legal="condenado",
        delito="Robo con violencia",
        fecha_nac="1989-02-19",
        condena=8,
        fecha_ingreso="2021-08-15",
        modulo="8",
        lugar_nacimiento="Ciudad de Mexico",
        nombre_contacto_emergencia="Carmen Rodriguez",
        relacion_contacto_emergencia="madre",
        numero_contacto_emergencia="+00 123 45 67 89",
    )

    entrevistas = [
        (1, 11, "2026-07-15", 8.4, "educativo"),
        (2, 12, "2026-06-01", 7.1, "familiar"),
    ]

    solicitudes = [
        _solicitud_fila(11, 2021, "familiar", "Acompañamiento medico a familiar", "2026-07-15", "pendiente", 5),
        _solicitud_fila(12, 2021, "educativo", "Examen final de capacitacion", "2026-07-01", "aceptada", 5),
        _solicitud_fila(13, 2021, "juridico", "Asistencia a diligencia judicial", "2026-05-10", "rechazada", 5),
    ]

    pantalla.cargar_perfil(interno, entrevistas, solicitudes)
    pantalla.volver.connect(lambda: print("Volver pulsado"))

    ventana.setCentralWidget(pantalla)
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
