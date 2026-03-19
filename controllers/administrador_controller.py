from PyQt5.QtCore import QObject, pyqtSignal

from controllers.administrador_datos_controller import AdministradorDatosController
from controllers.administrador_edicion_controller import AdministradorEdicionController
from controllers.administrador_internos_controller import AdministradorInternosController
from controllers.administrador_perfil_controller import AdministradorPerfilController
from controllers.administrador_usuarios_controller import AdministradorUsuariosController
from gui.administrador_inicio import VentanaAdministrador
from gui.mensajes import Mensajes


class AdministradorController(QObject):
    """
    Controlador principal para la gestion del rol administrador.
    """

    logout_signal = pyqtSignal()

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana_administrador = VentanaAdministrador()
        self.ventana_administrador.show()
        self.msg = Mensajes(self.ventana_administrador)

        self.usuarios = AdministradorUsuariosController(self)
        self.edicion = AdministradorEdicionController(self)
        self.datos = AdministradorDatosController(self)
        self.perfil = AdministradorPerfilController(self)
        self.internos = AdministradorInternosController(self)

        self._vista_origen_perfil_interno_admin = None
        self._titulo_origen_perfil_interno_admin = "Usuarios"
        self._vista_origen_perfil_profesional_admin = None
        self._titulo_origen_perfil_profesional_admin = "Usuarios"
        self._vista_origen_detalle_solicitud_admin = None
        self._titulo_origen_detalle_solicitud_admin = "Perfil interno"
        self._vista_origen_resumen_entrevista_admin = None
        self._titulo_origen_resumen_entrevista_admin = "Perfil interno"
        self._entrevista_actual_resumen_admin = None

        self._configurar_inicio()
        self._conectar_senales()

    def _configurar_inicio(self):
        self.ventana_administrador.establecer_usuario(self.usuario)
        self.ventana_administrador.establecer_titulo_pantalla("Inicio")

    def _conectar_senales(self):
        va = self.ventana_administrador

        va.boton_usuarios.clicked.connect(self.mostrar_lista_usuarios)
        va.boton_modelo.clicked.connect(self.mostrar_lista_modificar_prompts)
        va.boton_preguntas.clicked.connect(self.mostrar_lista_modificar_preguntas)
        va.boton_datos.clicked.connect(self.mostrar_pantalla_datos)
        va.pantalla_bienvenida.abrir_usuarios.connect(self.mostrar_lista_usuarios)
        va.pantalla_bienvenida.abrir_modelo.connect(self.mostrar_lista_modificar_prompts)
        va.pantalla_bienvenida.abrir_preguntas.connect(self.mostrar_lista_modificar_preguntas)
        va.pantalla_bienvenida.abrir_datos.connect(self.mostrar_pantalla_datos)

        va.pantalla_lista_usuarios.crear_usuario.connect(self.abrir_creacion_usuario)
        va.pantalla_lista_usuarios.editar_usuario.connect(self.abrir_edicion_usuario)
        va.pantalla_lista_usuarios.ver_perfil_interno.connect(self.mostrar_perfil_interno)
        va.pantalla_lista_usuarios.ver_perfil_profesional.connect(self.mostrar_perfil_profesional)
        va.pantalla_lista_usuarios.filtros_cambiados.connect(self.recargar_lista_usuarios)

        va.pantalla_lista_solicitudes_profesional.volver.connect(self.volver_desde_perfil_profesional)
        va.pantalla_lista_solicitudes_profesional.ver_perfil_interno.connect(self.mostrar_perfil_interno)
        va.pantalla_lista_solicitudes_profesional.ver_solicitud.connect(self.mostrar_solicitud_desde_lista_profesional)
        va.pantalla_lista_solicitudes_profesional.ver_entrevista.connect(
            self.mostrar_resumen_entrevista_desde_lista_profesional
        )

        va.pantalla_perfil_interno.volver.connect(self.volver_desde_perfil_interno)
        va.pantalla_perfil_interno.ver_solicitud.connect(self.mostrar_solicitud_desde_perfil_interno)
        va.pantalla_perfil_interno.ver_entrevista.connect(self.mostrar_entrevista_desde_perfil_interno)

        va.pantalla_detalle_solicitud.volver.connect(self.volver_desde_detalle_solicitud)
        va.pantalla_detalle_solicitud.ver_perfil_interno.connect(self.mostrar_perfil_interno)
        va.pantalla_detalle_solicitud.boton_ver_entrevista.clicked.connect(
            self.mostrar_resumen_entrevista_desde_detalle
        )

        va.pantalla_resumen_profesional_lectura.boton_atras.clicked.connect(
            self.volver_desde_resumen_entrevista
        )
        va.pantalla_resumen_profesional_lectura.grupo_botones_entrar.idClicked.connect(
            self.abrir_detalle_pregunta_desde_resumen
        )

        va.pantalla_lista_modificar_preguntas.grupo_botones_editar.idClicked.connect(
            self.mostrar_detalle_editar_pregunta
        )
        va.pantalla_lista_modificar_prompt.grupo_botones_editar.idClicked.connect(
            self.mostrar_detalle_editar_prompt
        )

        va.pantalla_datos.boton_exportar.clicked.connect(self.exportar_bd_csv)
        va.pantalla_datos.boton_importar.clicked.connect(self.importar_bd_csv)

        va.boton_usuario.clicked.connect(self.iniciar_perfil)
        va.boton_perfil.clicked.connect(self.iniciar_perfil)
        va.pantalla_perfil.guardar_cambios.connect(self.guardar_cambios_perfil)
        va.boton_cerrar_sesion.clicked.connect(self.cerrar_sesion)

    def mostrar_lista_usuarios(self):
        return self.usuarios.mostrar_lista_usuarios()

    def recargar_lista_usuarios(self):
        return self.usuarios.recargar_lista()

    def abrir_creacion_usuario(self):
        return self.usuarios.abrir_creacion_usuario()

    def abrir_edicion_usuario(self, usuario):
        return self.usuarios.abrir_edicion_usuario(usuario)

    def mostrar_perfil_interno(self, usuario):
        return self.internos.mostrar_perfil_interno(usuario)

    def mostrar_perfil_profesional(self, usuario):
        return self.usuarios.mostrar_perfil_profesional(usuario)

    def volver_desde_perfil_profesional(self):
        return self.usuarios.volver_desde_perfil_profesional()

    def volver_desde_perfil_interno(self):
        return self.internos.volver_desde_perfil_interno()

    def mostrar_solicitud_desde_perfil_interno(self, id_solicitud):
        return self.internos.mostrar_solicitud_desde_perfil_interno(id_solicitud)

    def mostrar_solicitud_desde_lista_profesional(self, solicitud):
        return self.internos.mostrar_solicitud_desde_perfil_interno(getattr(solicitud, "id_solicitud", None))

    def mostrar_entrevista_desde_perfil_interno(self, id_entrevista):
        return self.internos.mostrar_entrevista_desde_perfil_interno(id_entrevista)

    def volver_desde_detalle_solicitud(self):
        return self.internos.volver_desde_detalle_solicitud()

    def mostrar_resumen_entrevista_desde_detalle(self):
        return self.internos.mostrar_resumen_entrevista_desde_detalle()

    def mostrar_resumen_entrevista_desde_lista_profesional(self, solicitud):
        entrevista = getattr(solicitud, "entrevista", None)
        if entrevista is None:
            self.msg.mostrar_advertencia("Atención", "Esta solicitud no tiene entrevista.")
            return
        interno = self.internos._obtener_interno_de_solicitud(solicitud)
        nombre_interno = getattr(interno, "nombre", "") if interno is not None else ""
        return self.internos._abrir_resumen_entrevista(entrevista, nombre_interno)

    def volver_desde_resumen_entrevista(self):
        return self.internos.volver_desde_resumen_entrevista()

    def abrir_detalle_pregunta_desde_resumen(self, numero_pregunta):
        return self.internos.abrir_detalle_pregunta_desde_resumen(numero_pregunta)

    def mostrar_lista_modificar_preguntas(self):
        return self.edicion.mostrar_lista_modificar_preguntas()

    def mostrar_lista_modificar_prompts(self):
        return self.edicion.mostrar_lista_modificar_prompts()

    def mostrar_detalle_editar_pregunta(self, id_pregunta):
        return self.edicion.mostrar_detalle_editar_pregunta(id_pregunta)

    def mostrar_detalle_editar_prompt(self, id_pregunta):
        return self.edicion.mostrar_detalle_editar_prompt(id_pregunta)

    def mostrar_pantalla_datos(self):
        return self.datos.mostrar_pantalla_datos()

    def exportar_bd_csv(self):
        return self.datos.exportar_bd_csv()

    def importar_bd_csv(self):
        return self.datos.importar_bd_csv()

    def iniciar_perfil(self):
        return self.perfil.iniciar_perfil()

    def guardar_cambios_perfil(self):
        return self.perfil.guardar_cambios_perfil()

    def cerrar_sesion(self):
        confirmado = self.ventana_administrador.mostrar_confirmacion_logout()
        if confirmado:
            self.ventana_administrador.close()
            self.logout_signal.emit()
