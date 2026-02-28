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
        self._modo_lista_actual = None

        # Objetos iniciales
        self.profesional = self.cargar_profesional()             

        # ACTUALIZAR PANTALLA INICIO
        self.ventana_profesional.pantalla_bienvenida.set_profesional(self.profesional)
        self.actualizar_inicio_profesional()
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
        self.ventana_profesional.boton_nueva.clicked.connect(self.mostrar_lista_nuevas)
        self.ventana_profesional.boton_pendiente.clicked.connect(self.mostrar_lista_pendientes)
        self.ventana_profesional.boton_historial.clicked.connect(self.mostrar_lista_historial)

        self.ventana_profesional.pantalla_bienvenida.boton_nueva_solicitud.clicked.connect(
            self.mostrar_lista_nuevas
        )
        self.ventana_profesional.pantalla_bienvenida.boton_solicitudes_pendientes.clicked.connect(
            self.mostrar_lista_pendientes
        )
        self.ventana_profesional.pantalla_bienvenida.boton_historial_solicitudes.clicked.connect(
            self.mostrar_lista_historial
        )
        self.ventana_profesional.pantalla_lista_solicitud.asignar_solicitud.connect(
            self.asignar_solicitud_a_profesional
        )
        self.ventana_profesional.pantalla_lista_solicitud.filtro_superior_cambiado.connect(
            self.gestionar_filtro_superior_lista
        )

    def actualizar_inicio_profesional(self):
        """
        Actualiza la pantalla de bienvenida y menú lateral según
        solicitudes pendientes y completadas del profesional.
        """
        if not self.profesional:
            return

        num_pendientes = contar_solicitudes_por_evaluar_profesional(
            self.profesional.id_usuario
        )
        num_completadas = contar_solicitudes_por_profesional_y_estados(
            self.profesional.id_usuario,
            [
                Tipo_estado_solicitud.ACEPTADA.value,
                Tipo_estado_solicitud.RECHAZADA.value,
                Tipo_estado_solicitud.CANCELADA.value
            ]
        )
        num_historial = contar_solicitudes_por_profesional(self.profesional.id_usuario)

        self.ventana_profesional.actualizar_interfaz_inicio(
            num_pendientes,
            num_completadas,
            num_historial
        )
        self.ventana_profesional.pantalla_bienvenida.boton_historial_solicitudes.setVisible(
            num_historial > 0
        )

    def mostrar_lista_nuevas(self):
        self._modo_lista_actual = "nuevas"
        filas = listar_solicitudes_nuevas_sin_profesional()
        self._mostrar_lista_solicitudes(
            filas,
            top_activo="nuevas",
            combo_texto="Todos los estados",
            solo_sin_profesional=True
        )

    def mostrar_lista_pendientes(self):
        if not self.profesional:
            return

        self._modo_lista_actual = "pendientes"
        filas = listar_solicitudes_profesional(self.profesional.id_usuario)
        self._mostrar_lista_solicitudes(
            filas,
            top_activo="por_evaluar",
            combo_texto="Todos los estados",
            solo_sin_profesional=False
        )

    def mostrar_lista_historial(self):
        if not self.profesional:
            return

        self._modo_lista_actual = "historial"
        filas = listar_solicitudes_profesional(self.profesional.id_usuario)
        self._mostrar_lista_solicitudes(
            filas,
            top_activo=None,
            combo_texto="Todos los estados",
            solo_sin_profesional=False
        )

    def mostrar_lista_completadas(self):
        if not self.profesional:
            return

        self._modo_lista_actual = "completadas"
        filas = listar_solicitudes_profesional(self.profesional.id_usuario)
        self._mostrar_lista_solicitudes(
            filas,
            top_activo="completadas",
            combo_texto="Todos los estados",
            solo_sin_profesional=False
        )

    def gestionar_filtro_superior_lista(self, top_activo):
        if top_activo == "nuevas":
            self.mostrar_lista_nuevas()
        elif top_activo == "por_evaluar":
            self.mostrar_lista_pendientes()
        elif top_activo == "completadas":
            self.mostrar_lista_completadas()

    def asignar_solicitud_a_profesional(self, solicitud):
        if not self.profesional or not solicitud:
            return

        id_solicitud = getattr(solicitud, "id_solicitud", None)
        if id_solicitud is None:
            self.msg.mostrar_advertencia("Atencion", "No se pudo identificar la solicitud.")
            return

        ok = asignar_profesional_a_solicitud(id_solicitud, self.profesional.id_usuario)
        if not ok:
            self.msg.mostrar_advertencia("Atencion", "No se pudo asignar la solicitud.")
            return

        self.msg.mostrar_mensaje("Solicitud asignada", "Solicitud asignada correctamente")
        self.actualizar_inicio_profesional()
        self.recargar_lista_actual()

    def recargar_lista_actual(self):
        if self._modo_lista_actual == "nuevas":
            self.mostrar_lista_nuevas()
        elif self._modo_lista_actual == "pendientes":
            self.mostrar_lista_pendientes()
        elif self._modo_lista_actual == "completadas":
            self.mostrar_lista_completadas()
        elif self._modo_lista_actual == "historial":
            self.mostrar_lista_historial()

    def _mostrar_lista_solicitudes(self, filas_solicitud, top_activo, combo_texto, solo_sin_profesional):
        solicitudes = [self._construir_solicitud_desde_fila(fila) for fila in (filas_solicitud or [])]
        internos = self._cargar_internos_para_solicitudes(solicitudes)

        pantalla = self.ventana_profesional.pantalla_lista_solicitud
        pantalla.cargar_datos(solicitudes, internos)
        pantalla.aplicar_filtro_inicial(
            top_activo=top_activo,
            combo_texto=combo_texto,
            solo_sin_profesional=solo_sin_profesional,
            modo_historial=(self._modo_lista_actual == "historial")
        )
        self.ventana_profesional.stacked_widget.setCurrentWidget(pantalla)

    def _construir_solicitud_desde_fila(self, datos_solicitud):
        solicitud = Solicitud()

        solicitud.id_solicitud = datos_solicitud[0]
        solicitud.id_interno = datos_solicitud[1]
        solicitud.tipo = datos_solicitud[2]
        solicitud.motivo = datos_solicitud[3]
        solicitud.descripcion = datos_solicitud[4]
        solicitud.urgencia = datos_solicitud[5]
        solicitud.fecha_creacion = datos_solicitud[6]

        solicitud.fecha_inicio = datos_solicitud[7]
        solicitud.fecha_fin = datos_solicitud[8]
        solicitud.hora_salida = datos_solicitud[9]
        solicitud.hora_llegada = datos_solicitud[10]
        solicitud.destino = datos_solicitud[11]
        solicitud.provincia = datos_solicitud[12]
        solicitud.direccion = datos_solicitud[13]
        solicitud.cod_pos = datos_solicitud[14]

        solicitud.nombre_cp = datos_solicitud[15]
        solicitud.telf_cp = datos_solicitud[16]
        solicitud.relacion_cp = datos_solicitud[17]
        solicitud.direccion_cp = datos_solicitud[18]

        solicitud.nombre_cs = datos_solicitud[19]
        solicitud.telf_cs = datos_solicitud[20]
        solicitud.relacion_cs = datos_solicitud[21]

        solicitud.docs = datos_solicitud[22]
        solicitud.compromisos = datos_solicitud[23]
        solicitud.observaciones = datos_solicitud[24]
        solicitud.conclusiones_profesional = datos_solicitud[25]
        solicitud.id_profesional = datos_solicitud[26]
        solicitud.estado = datos_solicitud[27]
        solicitud.evaluacion_automatica = datos_solicitud[28] if len(datos_solicitud) > 28 else ""
        solicitud.entrevista = self.cargar_entrevista_solicitud(solicitud.id_solicitud)
        return solicitud

    def _cargar_internos_para_solicitudes(self, solicitudes):
        rcs = []
        for solicitud in solicitudes:
            num_rc = getattr(solicitud, "id_interno", None)
            if num_rc is not None:
                rcs.append(num_rc)

        datos_internos = encontrar_internos_por_num_rc(list(set(rcs)))
        internos = []
        for dato in datos_internos:
            interno = Interno(
                id_usuario=dato[1],
                nombre=dato[8],
                email=dato[9],
                contrasena=dato[10],
                rol=dato[11],
                num_RC=dato[0],
                situacion_legal=dato[2],
                delito=dato[3],
                fecha_nac=dato[5],
                condena=dato[4],
                fecha_ingreso=dato[6],
                modulo=dato[7]
            )
            internos.append(interno)
        return internos

    # Buscar entrevista de la solicitud
    def cargar_entrevista_solicitud(self, id_solicitud):
        datos_entrevista = encontrar_entrevista_por_solicitud(id_solicitud)
        if not datos_entrevista:
            return None

        entrevista = Entrevista(
            id_entrevista=datos_entrevista[0],
            id_interno=datos_entrevista[1],
            fecha=datos_entrevista[3]
        )
        entrevista.puntuacion = datos_entrevista[4]
        return entrevista

    def cerrar_sesion(self):
        confirmado = self.ventana_profesional.mostrar_confirmacion_logout()

        if confirmado:
            self.ventana_profesional.close()
            self.logout_signal.emit()

    



