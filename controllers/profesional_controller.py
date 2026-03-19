from PyQt5.QtCore import QObject, pyqtSignal

from db.profesional_db import agregar_profesional, encontrar_profesional_por_id

from controllers.profesional_entrevistas_controller import ProfesionalEntrevistasController
from controllers.profesional_internos_controller import ProfesionalInternosController
from controllers.profesional_navegacion_controller import ProfesionalNavegacionController
from controllers.profesional_perfil_controller import ProfesionalPerfilController
from controllers.profesional_solicitudes_controller import ProfesionalSolicitudesController

from gui.mensajes import Mensajes
from gui.profesional_inicio import VentanaProfesional
from models.profesional import Profesional


class ProfesionalController(QObject):
    """
    Controlador principal para la gestión de la aplicación por parte de un profesional.
    """
    logout_signal = pyqtSignal()

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana_profesional = VentanaProfesional()
        self.ventana_profesional.show()
        self.msg = Mensajes(self.ventana_profesional)

        # Atributos de estado
        self._modo_lista_actual = None
        self._vista_origen_perfil_interno = "solicitudes"
        self._vista_origen_detalle_solicitud = None
        self._titulo_origen_detalle_solicitud = "Solicitudes"
        self._detalle_solicitud_solo_lectura = False
        self._vista_origen_resumen_entrevista = None
        self._titulo_origen_resumen_entrevista = "Solicitudes"
        self._resumen_entrevista_solo_lectura = False
        self._nombre_interno_resumen = ""
        self._recargar_lista_al_salir_detalle = False
        self._entrevista_actual_resumen = None
        self._hilo_analisis_ia = None
        self._analisis_ia_trabajo_activo = None
        self._ventana_detalle_analisis = None
        self._analisis_ia_global_activo = False
        self._preguntas_ia_bloqueadas = set()
        self._cola_analisis_ia = []
        self._progreso_analisis_completo_actual = 0
        self._progreso_analisis_completo_total = 0

        self.profesional = self.cargar_profesional()

        # Controladores
        self.navegacion = ProfesionalNavegacionController(self)
        self.perfil = ProfesionalPerfilController(self)
        self.internos = ProfesionalInternosController(self)
        self.entrevistas = ProfesionalEntrevistasController(self)
        self.solicitudes = ProfesionalSolicitudesController(self)

        self.ventana_profesional.pantalla_bienvenida.set_profesional(self.profesional)
        self.actualizar_inicio_profesional()
        self.conectar_senales()

    def cargar_profesional(self):
        datos_profesional = encontrar_profesional_por_id(self.usuario.id_usuario)
        if not datos_profesional:
            agregar_profesional(self.usuario.id_usuario, f"AUTO-{self.usuario.id_usuario:04d}")
            datos_profesional = encontrar_profesional_por_id(self.usuario.id_usuario)
        if not datos_profesional:
            return None
        return Profesional(
            id_usuario=self.usuario.id_usuario,
            nombre=self.usuario.nombre,
            email=self.usuario.email,
            contrasena=self.usuario.contrasena,
            num_profesional=datos_profesional[0],
        )

    def conectar_senales(self):
        vp = self.ventana_profesional

        # Botones de la barra lateral
        vp.boton_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        vp.boton_nueva.clicked.connect(self.mostrar_lista_nuevas)
        vp.boton_pendiente.clicked.connect(self.mostrar_lista_pendientes)
        vp.boton_historial.clicked.connect(self.mostrar_lista_historial)
        vp.boton_internos.clicked.connect(self.mostrar_lista_internos_asignados)

        # Botones de la pantalla de bienvenida
        vp.pantalla_bienvenida.boton_nueva_solicitud.clicked.connect(self.mostrar_lista_nuevas)
        vp.pantalla_bienvenida.boton_solicitudes_pendientes.clicked.connect(self.mostrar_lista_pendientes)
        vp.pantalla_bienvenida.boton_historial_solicitudes.clicked.connect(self.mostrar_lista_historial)

        # Botones de la pantalla de lista de solicitudes
        vp.pantalla_lista_solicitud.asignar_solicitud.connect(self.asignar_solicitud_a_profesional)
        vp.pantalla_lista_solicitud.filtro_superior_cambiado.connect(self.gestionar_filtro_superior_lista)
        vp.pantalla_lista_solicitud.ver_perfil_interno.connect(self.mostrar_perfil_interno)
        vp.pantalla_lista_solicitud.ver_solicitud.connect(self.mostrar_detalle_solicitud)
        vp.pantalla_lista_solicitud.ver_entrevista.connect(self.mostrar_resumen_entrevista_desde_lista)

        # Botones de la pantalla de perfil interno y lista de internos
        vp.pantalla_perfil_interno.volver.connect(self.volver_desde_perfil_interno)
        vp.pantalla_perfil_interno.ver_entrevista.connect(self.mostrar_entrevista_desde_perfil_interno)
        vp.pantalla_perfil_interno.ver_solicitud.connect(self.mostrar_solicitud_desde_perfil_interno)
        vp.pantalla_lista_internos.ver_perfil_interno.connect(self.mostrar_perfil_interno_desde_internos)
        vp.pantalla_lista_internos.ver_ultima_entrevista.connect(self.mostrar_ultima_entrevista_desde_internos)

        # Botones de la pantalla de detalle de solicitud
        vp.pantalla_detalle_solicitud.volver.connect(self.volver_desde_detalle_solicitud)
        vp.pantalla_detalle_solicitud.ver_perfil_interno.connect(self.mostrar_perfil_interno_desde_detalle)
        vp.pantalla_detalle_solicitud.boton_finalizar.clicked.connect(self.finalizar_solicitud_desde_detalle)
        vp.pantalla_detalle_solicitud.boton_descargar_solicitud.clicked.connect(self.descargar_solicitud_desde_detalle)
        vp.pantalla_detalle_solicitud.boton_ver_entrevista.clicked.connect(self.mostrar_resumen_entrevista_desde_detalle)

        # Botones de la pantalla de resumen de entrevista
        vp.pantalla_resumen_profesional.boton_atras.clicked.connect(self.volver_desde_resumen_entrevista)
        vp.pantalla_resumen_profesional.boton_anadir_comentario.clicked.connect(self.abrir_ventana_comentarios_entrevista)
        vp.pantalla_resumen_profesional.boton_analizar_entrevista.clicked.connect(self.analizar_entrevista_completa)
        vp.pantalla_resumen_profesional.guardar_evaluacion_profesional.connect(self.guardar_evaluacion_profesional_actual)
        vp.pantalla_resumen_profesional.grupo_botones_ia.idClicked.connect(self.analizar_pregunta_desde_resumen)
        vp.pantalla_resumen_profesional.grupo_botones_entrar.idClicked.connect(self.abrir_detalle_pregunta_desde_resumen)
        vp.pantalla_resumen_profesional_lectura.boton_atras.clicked.connect(self.volver_desde_resumen_entrevista)
        vp.pantalla_resumen_profesional_lectura.boton_anadir_comentario.clicked.connect(self.abrir_ventana_comentarios_entrevista)
        vp.pantalla_resumen_profesional_lectura.grupo_botones_entrar.idClicked.connect(self.abrir_detalle_pregunta_desde_resumen)

        # Botones de la pantalla de perfil
        vp.boton_usuario.clicked.connect(self.iniciar_perfil)
        vp.boton_perfil.clicked.connect(self.iniciar_perfil)
        vp.pantalla_perfil.guardar_cambios.connect(self.guardar_cambios_perfil)

    def actualizar_inicio_profesional(self):
        return self.navegacion.actualizar_inicio_profesional()

    def mostrar_lista_nuevas(self):
        return self.solicitudes.mostrar_lista_nuevas()

    def mostrar_lista_pendientes(self):
        return self.solicitudes.mostrar_lista_pendientes()

    def mostrar_lista_historial(self):
        return self.solicitudes.mostrar_lista_historial()

    def mostrar_lista_completadas(self):
        return self.solicitudes.mostrar_lista_completadas()

    def gestionar_filtro_superior_lista(self, top_activo):
        return self.solicitudes.gestionar_filtro_superior_lista(top_activo)

    def asignar_solicitud_a_profesional(self, solicitud):
        return self.solicitudes.asignar_solicitud_a_profesional(solicitud)

    def recargar_lista_actual(self):
        return self.solicitudes.recargar_lista_actual()

    def volver_desde_perfil_interno(self):
        return self.internos.volver_desde_perfil_interno()

    def mostrar_perfil_interno(self, interno):
        return self.internos.mostrar_perfil_interno(interno)

    def mostrar_perfil_interno_desde_detalle(self, interno):
        return self.internos.mostrar_perfil_interno_desde_detalle(interno)

    def mostrar_perfil_interno_desde_internos(self, interno):
        return self.internos.mostrar_perfil_interno_desde_internos(interno)

    def mostrar_ultima_entrevista_desde_internos(self, dato_interno):
        return self.entrevistas.mostrar_ultima_entrevista_desde_internos(dato_interno)

    def mostrar_entrevista_desde_perfil_interno(self, id_entrevista):
        return self.entrevistas.mostrar_entrevista_desde_perfil_interno(id_entrevista)

    def mostrar_solicitud_desde_perfil_interno(self, id_solicitud):
        return self.solicitudes.mostrar_solicitud_desde_perfil_interno(id_solicitud)

    def mostrar_detalle_solicitud(self, solicitud):
        return self.solicitudes.mostrar_detalle_solicitud(solicitud)

    def finalizar_solicitud_desde_detalle(self):
        return self.solicitudes.finalizar_solicitud_desde_detalle()

    def descargar_solicitud_desde_detalle(self):
        return self.solicitudes.descargar_solicitud_desde_detalle()

    def volver_desde_detalle_solicitud(self):
        return self.solicitudes.volver_desde_detalle_solicitud()

    def mostrar_resumen_entrevista_desde_lista(self, solicitud):
        return self.entrevistas.mostrar_resumen_entrevista_desde_lista(solicitud)

    def mostrar_resumen_entrevista_desde_detalle(self):
        return self.entrevistas.mostrar_resumen_entrevista_desde_detalle()

    def abrir_ventana_comentarios_entrevista(self):
        return self.entrevistas.abrir_ventana_comentarios_entrevista()

    def abrir_detalle_pregunta_desde_resumen(self, numero_pregunta):
        return self.entrevistas.abrir_detalle_pregunta_desde_resumen(numero_pregunta)

    def volver_desde_resumen_entrevista(self):
        return self.entrevistas.volver_desde_resumen_entrevista()

    def analizar_pregunta_desde_resumen(self, numero_pregunta):
        return self.entrevistas.analizar_pregunta_desde_resumen(numero_pregunta)

    def analizar_entrevista_completa(self):
        return self.entrevistas.analizar_entrevista_completa()

    def guardar_evaluacion_profesional_actual(self):
        return self.entrevistas.guardar_evaluacion_profesional_actual()

    def mostrar_lista_internos_asignados(self):
        return self.internos.mostrar_lista_internos_asignados()

    def cargar_entrevista_solicitud(self, id_solicitud):
        return self.entrevistas.cargar_entrevista_solicitud(id_solicitud)

    def cerrar_sesion(self):
        return self.navegacion.cerrar_sesion()

    def iniciar_perfil(self):
        return self.perfil.iniciar_perfil()

    def guardar_cambios_perfil(self):
        return self.perfil.guardar_cambios_perfil()
