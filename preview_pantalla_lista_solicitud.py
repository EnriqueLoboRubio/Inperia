import sys

from PyQt5.QtWidgets import QApplication

from gui.pantalla_lista_solicitud import PantallaListaSolicitud
from models.interno import Interno
from models.solicitud import Solicitud
from models.entrevista import Entrevista
from utils.enums import Tipo_rol


def crear_interno(id_usuario, nombre, num_rc):
    return Interno(
        id_usuario=id_usuario,
        nombre=nombre,
        email=f"{nombre.lower().replace(' ', '.')}@demo.com",
        contrasena="demo",
        rol=Tipo_rol.INTERNO.value,
        num_RC=num_rc,
        situacion_legal="Condenado",
        delito="N/A",
        fecha_nac="01/01/1990",
        condena="N/A",
        fecha_ingreso="01/01/2024",
        modulo="A1",
    )


def crear_solicitud(id_solicitud, id_interno, estado, fecha, con_entrevista, id_profesional=None):
    s = Solicitud()
    s.id_solicitud = id_solicitud
    s.id_interno = id_interno
    s.estado = estado
    s.fecha_creacion = fecha
    s.id_profesional = id_profesional
    s.conclusiones_profesional = (
        "El resultado obtenido es del 30%, se aprecia riesgo normal y buen ajuste en permisos anteriores."
    )
    if con_entrevista:
        s.entrevista = Entrevista(
            id_entrevista=1000 + id_solicitud,
            id_interno=id_interno,
            fecha="15/07/2025",
        )
    return s


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pantalla = PantallaListaSolicitud()
    pantalla.setWindowTitle("Preview - pantalla_lista_solicitud")
    pantalla.resize(1200, 700)

    internos = [
        crear_interno(1, "Maria Lopez Lopez", "2021-0234"),
        crear_interno(2, "Carlos Ruiz Martin", "2022-0101"),
        crear_interno(3, "Ana Perez Gomez", "2020-3344"),
    ]

    solicitudes = [
        crear_solicitud(1, "2021-0234", "pendiente", "15/07/2025", True, id_profesional=9),
        crear_solicitud(2, "2022-0101", "iniciada", "20/02/2026", False, id_profesional=None),
        crear_solicitud(3, "2020-3344", "aceptada", "03/01/2026", True, id_profesional=7),
    ]

    pantalla.cargar_datos(solicitudes, internos)

    pantalla.ver_perfil_interno.connect(lambda s: print(f"[perfil] Solicitud #{s.id_solicitud}"))
    pantalla.ver_entrevista.connect(lambda s: print(f"[entrevista] Solicitud #{s.id_solicitud}"))
    pantalla.ver_solicitud.connect(lambda s: print(f"[solicitud] Solicitud #{s.id_solicitud}"))
    pantalla.asignar_solicitud.connect(lambda s: print(f"[asignar] Solicitud #{s.id_solicitud}"))

    pantalla.show()
    sys.exit(app.exec_())
