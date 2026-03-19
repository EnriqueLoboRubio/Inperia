from db.comentario_entrevista_mensajes_db import listar_comentarios_entrevista
from db.comentario_ia_entrevista_db import obtener_comentario_ia
from db.comentario_pregunta_db import listar_comentarios_respuesta
from db.entrevista_db import (
    encontrar_entrevista_por_id,
    encontrar_entrevista_por_solicitud,
    listar_ultimas_entrevistas_por_interno,
)
from db.interno_db import encontrar_interno_por_id, encontrar_internos_por_num_rc
from db.respuesta_db import obtener_respuestas_por_entrevista
from db.solicitud_db import encontrar_solicitud_por_id, listar_solicitudes_por_interno
from gui.ventana_detalle_pregunta_profesional import VentanaDetallePreguntaProfesional
from models.entrevista import Entrevista
from models.interno import Interno
from models.pregunta import Pregunta
from models.solicitud import Solicitud


class AdministradorInternosController:
    """
    Navegacion en modo lectura del perfil de un interno desde el panel de administrador.
    """

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar_perfil_interno(self, usuario):
        interno = self._cargar_interno_desde_usuario(usuario)
        if interno is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se encontró la información del interno.")
            return

        self.controlador._vista_origen_perfil_interno_admin = (
            self.controlador.ventana_administrador.stacked_widget.currentWidget()
        )
        self.controlador._titulo_origen_perfil_interno_admin = (
            self.controlador.ventana_administrador.titulo_pantalla.text()
        )

        entrevistas = listar_ultimas_entrevistas_por_interno(interno.num_RC, limite=5)
        solicitudes = listar_solicitudes_por_interno(interno.num_RC)
        pantalla = self.controlador.ventana_administrador.pantalla_perfil_interno
        pantalla.cargar_perfil(interno=interno, entrevistas=entrevistas, solicitudes=solicitudes)
        self.controlador.ventana_administrador.mostrar_pantalla_perfil_interno()

    def volver_desde_perfil_interno(self):
        self._restaurar_vista(
            self.controlador._vista_origen_perfil_interno_admin,
            self.controlador._titulo_origen_perfil_interno_admin,
            fallback=self.controlador.ventana_administrador.pantalla_lista_usuarios,
            fallback_titulo="Usuarios",
        )

    def mostrar_solicitud_desde_perfil_interno(self, id_solicitud):
        fila = encontrar_solicitud_por_id(id_solicitud)
        if not fila:
            self.controlador.msg.mostrar_advertencia("Atención", "No se pudo cargar la solicitud seleccionada.")
            return

        solicitud = self._construir_solicitud_desde_fila(fila)
        interno = self._obtener_interno_de_solicitud(solicitud)
        if interno is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se encontró la información del interno.")
            return

        self.controlador._vista_origen_detalle_solicitud_admin = (
            self.controlador.ventana_administrador.stacked_widget.currentWidget()
        )
        self.controlador._titulo_origen_detalle_solicitud_admin = (
            self.controlador.ventana_administrador.titulo_pantalla.text()
        )

        pantalla = self.controlador.ventana_administrador.pantalla_detalle_solicitud
        pantalla.cargar_datos(solicitud, interno)
        pantalla.set_modo_solo_lectura(True)
        self.controlador.ventana_administrador.mostrar_pantalla_detalle_solicitud()

    def volver_desde_detalle_solicitud(self):
        self._restaurar_vista(
            self.controlador._vista_origen_detalle_solicitud_admin,
            self.controlador._titulo_origen_detalle_solicitud_admin,
            fallback=self.controlador.ventana_administrador.pantalla_lista_usuarios,
            fallback_titulo="Usuarios",
        )

    def mostrar_entrevista_desde_perfil_interno(self, id_entrevista):
        entrevista = self.cargar_entrevista_por_id(id_entrevista)
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se pudo cargar la entrevista.")
            return

        nombre_interno = self.controlador.ventana_administrador.pantalla_perfil_interno.lbl_nombre.text()
        self._abrir_resumen_entrevista(entrevista, nombre_interno)

    def mostrar_resumen_entrevista_desde_detalle(self):
        pantalla = self.controlador.ventana_administrador.pantalla_detalle_solicitud
        solicitud = getattr(pantalla, "_solicitud", None)
        if solicitud is None or getattr(solicitud, "entrevista", None) is None:
            self.controlador.msg.mostrar_advertencia("Atención", "Esta solicitud no tiene entrevista.")
            return

        interno = getattr(pantalla, "_interno", None)
        nombre_interno = getattr(interno, "nombre", "") if interno is not None else ""
        self._abrir_resumen_entrevista(solicitud.entrevista, nombre_interno)

    def volver_desde_resumen_entrevista(self):
        self._restaurar_vista(
            self.controlador._vista_origen_resumen_entrevista_admin,
            self.controlador._titulo_origen_resumen_entrevista_admin,
            fallback=self.controlador.ventana_administrador.pantalla_lista_usuarios,
            fallback_titulo="Usuarios",
        )

    def abrir_detalle_pregunta_desde_resumen(self, numero_pregunta):
        entrevista = self.controlador._entrevista_actual_resumen_admin
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay entrevista cargada.")
            return

        pregunta = None
        for respuesta in list(getattr(entrevista, "respuestas", []) or []):
            try:
                if int(getattr(respuesta, "id_pregunta", -1)) == int(numero_pregunta):
                    pregunta = respuesta
                    break
            except (TypeError, ValueError):
                continue

        if pregunta is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se encontró la pregunta seleccionada.")
            return

        ventana = VentanaDetallePreguntaProfesional(
            pregunta=pregunta,
            numero=int(numero_pregunta),
            id_entrevista=getattr(entrevista, "id_entrevista", None),
            id_profesional=None,
            solo_lectura=True,
            parent=self.controlador.ventana_administrador,
        )
        ventana.exec_()

    def _abrir_resumen_entrevista(self, entrevista, nombre_interno=""):
        self.controlador._vista_origen_resumen_entrevista_admin = (
            self.controlador.ventana_administrador.stacked_widget.currentWidget()
        )
        self.controlador._titulo_origen_resumen_entrevista_admin = (
            self.controlador.ventana_administrador.titulo_pantalla.text()
        )
        self.controlador._entrevista_actual_resumen_admin = entrevista

        pantalla = self.controlador.ventana_administrador.pantalla_resumen_profesional_lectura
        pantalla.cargar_datos_respuestas(entrevista, nombre_interno=nombre_interno)
        pantalla.boton_anadir_comentario.setEnabled(False)
        pantalla.boton_anadir_comentario.setToolTip(
            "Desactivado: el administrador solo puede consultar la entrevista."
        )
        self.controlador.ventana_administrador.mostrar_pantalla_resumen_entrevista()

    def _cargar_interno_desde_usuario(self, usuario):
        id_usuario = None
        if isinstance(usuario, dict):
            id_usuario = usuario.get("id_usuario")
        else:
            id_usuario = getattr(usuario, "id_usuario", None)

        if id_usuario is None:
            return None

        fila = encontrar_interno_por_id(id_usuario)
        if not fila:
            return None
        return self._construir_interno_desde_fila(fila, usuario)

    @staticmethod
    def _construir_interno_desde_fila(fila, usuario=None):
        nombre = getattr(usuario, "nombre", None)
        email = getattr(usuario, "email", None)
        contrasena = getattr(usuario, "contrasena", "")
        if isinstance(usuario, dict):
            nombre = usuario.get("nombre")
            email = usuario.get("email")
            contrasena = usuario.get("contrasena", "")

        return Interno(
            id_usuario=fila[1],
            nombre=nombre or "-",
            email=email or "-",
            contrasena=contrasena or "",
            rol="interno",
            num_RC=fila[0],
            situacion_legal=fila[2],
            delito=fila[3],
            fecha_nac=fila[5],
            condena=fila[4],
            fecha_ingreso=fila[6],
            modulo=fila[7],
            lugar_nacimiento=fila[8] if len(fila) > 8 else "",
            nombre_contacto_emergencia=fila[9] if len(fila) > 9 else "",
            relacion_contacto_emergencia=fila[10] if len(fila) > 10 else "",
            numero_contacto_emergencia=fila[11] if len(fila) > 11 else "",
        )

    def _construir_solicitud_desde_fila(self, fila):
        solicitud = Solicitud()
        solicitud.id_solicitud = fila[0]
        solicitud.id_interno = fila[1]
        solicitud.tipo = fila[2]
        solicitud.motivo = fila[3]
        solicitud.descripcion = fila[4]
        solicitud.urgencia = fila[5]
        solicitud.fecha_creacion = fila[6]
        solicitud.fecha_inicio = fila[7]
        solicitud.fecha_fin = fila[8]
        solicitud.hora_salida = fila[9]
        solicitud.hora_llegada = fila[10]
        solicitud.destino = fila[11]
        solicitud.provincia = fila[12]
        solicitud.direccion = fila[13]
        solicitud.cod_pos = fila[14]
        solicitud.nombre_cp = fila[15]
        solicitud.telf_cp = fila[16]
        solicitud.relacion_cp = fila[17]
        solicitud.direccion_cp = fila[18]
        solicitud.nombre_cs = fila[19]
        solicitud.telf_cs = fila[20]
        solicitud.relacion_cs = fila[21]
        solicitud.docs = fila[22]
        solicitud.compromisos = fila[23]
        solicitud.observaciones = fila[24]
        solicitud.conclusiones_profesional = fila[25]
        solicitud.id_profesional = fila[26]
        solicitud.estado = fila[27]
        solicitud.entrevista = self.cargar_entrevista_solicitud(solicitud.id_solicitud)
        return solicitud

    def _obtener_interno_de_solicitud(self, solicitud):
        pantalla_perfil = self.controlador.ventana_administrador.pantalla_perfil_interno
        interno_actual = getattr(pantalla_perfil, "_interno_actual", None)
        if interno_actual is not None and int(getattr(interno_actual, "num_RC", 0) or 0) == int(
            getattr(solicitud, "id_interno", 0) or 0
        ):
            return interno_actual

        filas = encontrar_internos_por_num_rc([getattr(solicitud, "id_interno", None)])
        fila = filas[0] if filas else None
        if not fila:
            return None
        return Interno(
            id_usuario=fila[1],
            nombre=fila[8],
            email=fila[9],
            contrasena=fila[10],
            rol=fila[11],
            num_RC=fila[0],
            situacion_legal=fila[2],
            delito=fila[3],
            fecha_nac=fila[5],
            condena=fila[4],
            fecha_ingreso=fila[6],
            modulo=fila[7],
            lugar_nacimiento=fila[12] if len(fila) > 12 else "",
            nombre_contacto_emergencia=fila[13] if len(fila) > 13 else "",
            relacion_contacto_emergencia=fila[14] if len(fila) > 14 else "",
            numero_contacto_emergencia=fila[15] if len(fila) > 15 else "",
        )

    def cargar_internos_para_solicitudes(self, solicitudes):
        ids_internos = []
        for solicitud in solicitudes or []:
            id_interno = getattr(solicitud, "id_interno", None)
            if id_interno is not None:
                ids_internos.append(id_interno)

        filas = encontrar_internos_por_num_rc(list(set(ids_internos)))
        internos = []
        for fila in filas:
            internos.append(
                Interno(
                    id_usuario=fila[1],
                    nombre=fila[8],
                    email=fila[9],
                    contrasena=fila[10],
                    rol=fila[11],
                    num_RC=fila[0],
                    situacion_legal=fila[2],
                    delito=fila[3],
                    fecha_nac=fila[5],
                    condena=fila[4],
                    fecha_ingreso=fila[6],
                    modulo=fila[7],
                    lugar_nacimiento=fila[12] if len(fila) > 12 else "",
                    nombre_contacto_emergencia=fila[13] if len(fila) > 13 else "",
                    relacion_contacto_emergencia=fila[14] if len(fila) > 14 else "",
                    numero_contacto_emergencia=fila[15] if len(fila) > 15 else "",
                )
            )
        return internos

    def cargar_entrevista_solicitud(self, id_solicitud):
        fila = encontrar_entrevista_por_solicitud(id_solicitud)
        if not fila:
            return None
        return self._construir_entrevista_desde_fila(fila)

    def cargar_entrevista_por_id(self, id_entrevista):
        fila = encontrar_entrevista_por_id(id_entrevista)
        if not fila:
            return None
        return self._construir_entrevista_desde_fila(fila)

    def _construir_entrevista_desde_fila(self, fila):
        entrevista = Entrevista(
            id_entrevista=fila[0],
            id_interno=fila[1],
            fecha=fila[3],
        )
        entrevista.puntuacion_ia = fila[4]
        entrevista.puntuacion_profesional = fila[5] if len(fila) > 5 else -1
        entrevista.estado_evaluacion_ia = fila[6] if len(fila) > 6 else "sin evaluación"
        self._cargar_respuestas_entrevista(entrevista)
        return entrevista

    def _cargar_respuestas_entrevista(self, entrevista):
        entrevista.respuestas = []
        entrevista.comentarios = self._cargar_comentarios_entrevista(entrevista.id_entrevista)
        entrevista.comentario_ia_general = self._cargar_comentario_ia_entrevista(entrevista.id_entrevista)
        for dato in obtener_respuestas_por_entrevista(entrevista.id_entrevista):
            pregunta = Pregunta(
                id_pregunta=dato.get("id_pregunta"),
                respuesta=dato.get("texto_respuesta", ""),
            )
            pregunta.id_respuesta = dato.get("id_respuesta")
            pregunta.set_archivo_audio(dato.get("ruta_audio"))
            pregunta.nivel_ia = dato.get("nivel_ia", -1)
            pregunta.nivel_profesional = dato.get("nivel_profesional", -1)
            pregunta.valoracion_ia = str(dato.get("analisis_ia", "") or "").strip()
            pregunta.comentarios = self._cargar_comentarios_respuesta(pregunta.id_respuesta)
            entrevista.add_respuestas(pregunta)

    @staticmethod
    def _cargar_comentarios_respuesta(id_respuesta):
        if not id_respuesta:
            return []
        return [
            {
                "id": fila[0],
                "id_respuesta": fila[1],
                "id_profesional": fila[2],
                "comentario": fila[3],
                "fecha": fila[4],
            }
            for fila in listar_comentarios_respuesta(id_respuesta)
        ]

    @staticmethod
    def _cargar_comentarios_entrevista(id_entrevista):
        if not id_entrevista:
            return []
        return [
            {
                "id": fila[0],
                "id_entrevista": fila[1],
                "id_profesional": fila[2],
                "comentario": fila[3],
                "fecha": fila[4],
            }
            for fila in listar_comentarios_entrevista(id_entrevista)
        ]

    @staticmethod
    def _cargar_comentario_ia_entrevista(id_entrevista):
        if not id_entrevista:
            return None
        fila = obtener_comentario_ia(id_entrevista)
        if not fila:
            return None
        texto = str(fila[2] or "").strip()
        if not texto:
            return None
        return {
            "id": fila[0],
            "id_entrevista": fila[1],
            "id_profesional": None,
            "comentario": texto,
            "fecha": fila[3],
            "es_ia": True,
        }

    def _restaurar_vista(self, widget, titulo, fallback, fallback_titulo):
        ventana = self.controlador.ventana_administrador
        if widget is not None:
            ventana.stacked_widget.setCurrentWidget(widget)
            ventana.establecer_titulo_pantalla(titulo)
            return
        ventana.stacked_widget.setCurrentWidget(fallback)
        ventana.establecer_titulo_pantalla(fallback_titulo)
