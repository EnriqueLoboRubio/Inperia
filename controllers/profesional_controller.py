import os, shutil
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog
from datetime import date

from controllers.solicitud_controller import SolicitudController
from controllers.progreso_controller import ProgresoController

from gui.profesional_inicio import VentanaProfesional
from gui.ventana_detalle_edit_pregunta_interno import VentanaDetallePreguntaEdit
from gui.ventana_detalle_pregunta_interno import VentanaDetallePregunta

from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *
from db.profesional_db import *

from models.profesional import Profesional
from models.interno import Interno
from models.solicitud import Solicitud
from models.entrevista import Entrevista
from models.pregunta import Pregunta

from utils.enums import Tipo_estado_solicitud

from gui.mensajes import Mensajes

class ProfesionalController(QObject):

    #Señales
    logout_signal = pyqtSignal()

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana_profesional = VentanaProfesional()
        self.ventana_profesional.show()
        self.msg = Mensajes(self.ventana_profesional)

        # Objetos iniciales
        self.profesional = self.cargar_profesional()             

        # ACTUALIZAR PANTALLA INICIO
        self.ventana_profesional.pantalla_bienvenida.set_profesional(self.profesional)
        self.conectar_senales()

    # -------- CARGAR DATOS --------

    # Buscar profesional por id de usuario y cargar datos
    def cargar_profesional(self):
        datos_profesional = encontrar_profesional_por_id(self.usuario.id_usuario)
        if datos_profesional:
            profesional = Profesional(
                id_usuario=self.usuario.id_usuario,
                nombre=self.usuario.nombre,
                email=self.usuario.email,
                contrasena=self.usuario.contrasena,
                num_profesional=datos_profesional[0],
            )
            return profesional
        else:
            return None

    def conectar_senales(self):
        self.ventana_profesional.boton_cerrar_sesion.clicked.connect(
            self.cerrar_sesion
        )

    def cerrar_sesion(self):
        confirmado = self.ventana_profesional.mostrar_confirmacion_logout()

        if confirmado:
            self.ventana_profesional.close()
            self.logout_signal.emit()

    



