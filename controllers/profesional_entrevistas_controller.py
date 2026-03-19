from unicodedata import normalize

from db.comentario_entrevista_mensajes_db import (
    crear_tabla_comentarios_entrevista_mensajes,
    listar_comentarios_entrevista,
    reemplazar_comentarios_entrevista,
)
from db.comentario_ia_entrevista_db import obtener_comentario_ia
from db.comentario_pregunta_db import listar_comentarios_respuesta, reemplazar_comentarios_respuesta
from db.entrevista_db import (
    encontrar_entrevista_por_id,
    encontrar_entrevista_por_solicitud,
    actualizar_puntuacion_profesional_entrevista,
)
from db.respuesta_db import (
    actualizar_nivel_profesional_respuesta,
    obtener_respuestas_por_entrevista,
)
from gui.ventana_comentarios_entrevista_profesional import VentanaComentariosEntrevistaProfesional
from gui.ventana_detalle_pregunta_profesional import VentanaDetallePreguntaProfesional
from ia.analisis_service import HiloAnalisisIA
from models.entrevista import Entrevista
from models.pregunta import Pregunta
from utils.enums import Tipo_estado_solicitud
from utils.ecuacion_riesgo import calcular_puntuacion_total_profesional


class ProfesionalEntrevistasController:
    """
    Controlador para la gestion de entrevistas.
    """

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar_resumen_entrevista_desde_lista(self, solicitud):
        if solicitud is None:
            return

        entrevista = getattr(solicitud, "entrevista", None)
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "Esta solicitud no tiene entrevista.")
            return

        interno = self.controlador.internos._obtener_interno_de_solicitud(solicitud)
        nombre_interno = getattr(interno, "nombre", "") if interno is not None else ""

        self.controlador._vista_origen_resumen_entrevista = self.controlador.ventana_profesional.stacked_widget.currentWidget()
        self.controlador._titulo_origen_resumen_entrevista = self.controlador.ventana_profesional.titulo_pantalla.text()
        self._abrir_resumen_entrevista(
            entrevista,
            nombre_interno,
            solo_lectura=(
                self.controlador._detalle_solicitud_solo_lectura
                or self._resumen_debe_ser_solo_lectura(solicitud)
            ),
        )

    def mostrar_resumen_entrevista_desde_detalle(self):
        pantalla = self.controlador.ventana_profesional.pantalla_detalle_solicitud
        solicitud = getattr(pantalla, "_solicitud", None)
        interno = getattr(pantalla, "_interno", None)
        if solicitud is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay solicitud cargada.")
            return

        entrevista = getattr(solicitud, "entrevista", None)
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "Esta solicitud no tiene entrevista.")
            return

        nombre_interno = getattr(interno, "nombre", "") if interno is not None else ""
        self.controlador._vista_origen_resumen_entrevista = self.controlador.ventana_profesional.stacked_widget.currentWidget()
        self.controlador._titulo_origen_resumen_entrevista = self.controlador.ventana_profesional.titulo_pantalla.text()
        self._abrir_resumen_entrevista(
            entrevista,
            nombre_interno,
            solo_lectura=self._resumen_debe_ser_solo_lectura(solicitud),
        )

    def mostrar_ultima_entrevista_desde_internos(self, dato_interno):
        if not dato_interno:
            return

        entrevista_id = dato_interno.get("id_ultima_entrevista")
        if not entrevista_id:
            self.controlador.msg.mostrar_advertencia("Atención", "Este interno no tiene entrevistas.")
            return

        entrevista = self.cargar_entrevista_por_id(entrevista_id)
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se pudo cargar la última entrevista.")
            return

        interno = dato_interno.get("interno")
        nombre_interno = getattr(interno, "nombre", "") if interno is not None else ""
        self.controlador._vista_origen_resumen_entrevista = (
            self.controlador.ventana_profesional.stacked_widget.currentWidget()
        )
        self.controlador._titulo_origen_resumen_entrevista = (
            self.controlador.ventana_profesional.titulo_pantalla.text()
        )
        self._abrir_resumen_entrevista(entrevista, nombre_interno, solo_lectura=True)

    def mostrar_entrevista_desde_perfil_interno(self, id_entrevista):
        if not id_entrevista:
            self.controlador.msg.mostrar_advertencia("AtenciÃ³n", "No se encontrÃ³ la entrevista seleccionada.")
            return

        entrevista = self.cargar_entrevista_por_id(id_entrevista)
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("AtenciÃ³n", "No se pudo cargar la entrevista.")
            return

        pantalla_perfil = self.controlador.ventana_profesional.pantalla_perfil_interno
        nombre_interno = pantalla_perfil.lbl_nombre.text() if hasattr(pantalla_perfil, "lbl_nombre") else ""
        self.controlador._vista_origen_resumen_entrevista = (
            self.controlador.ventana_profesional.stacked_widget.currentWidget()
        )
        self.controlador._titulo_origen_resumen_entrevista = (
            self.controlador.ventana_profesional.titulo_pantalla.text()
        )
        self._abrir_resumen_entrevista(entrevista, nombre_interno, solo_lectura=True)

    def _abrir_resumen_entrevista(self, entrevista, nombre_interno="", solo_lectura=False):
        self.controlador._entrevista_actual_resumen = entrevista
        self.controlador._resumen_entrevista_solo_lectura = solo_lectura
        self.controlador._nombre_interno_resumen = nombre_interno or ""
        self._cargar_respuestas_entrevista(entrevista)
        if solo_lectura:
            pantalla_resumen = self.controlador.ventana_profesional.pantalla_resumen_profesional_lectura
        else:
            pantalla_resumen = self.controlador.ventana_profesional.pantalla_resumen_profesional
        pantalla_resumen.cargar_datos_respuestas(entrevista, nombre_interno=nombre_interno)
        self._aplicar_bloqueos_ia_en_resumen()
        self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(pantalla_resumen)
        self.controlador.ventana_profesional.establecer_titulo_pantalla("Resumen de entrevista")

    def abrir_ventana_comentarios_entrevista(self):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None or not getattr(entrevista, "id_entrevista", None):
            self.controlador.msg.mostrar_advertencia("Atención", "No hay entrevista cargada.")
            return

        id_prof = getattr(self.controlador.profesional, "id_usuario", None)
        if id_prof is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay profesional activo.")
            return

        crear_tabla_comentarios_entrevista_mensajes()
        ventana = VentanaComentariosEntrevistaProfesional(
            entrevista=entrevista,
            id_profesional=id_prof,
            solo_lectura=self.controlador._resumen_entrevista_solo_lectura,
            parent=self.controlador.ventana_profesional,
        )
        ventana.exec_()
        self._sincronizar_entrevista_actual()

    def abrir_detalle_pregunta_desde_resumen(self, numero_pregunta):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay entrevista cargada.")
            return

        respuestas = list(getattr(entrevista, "respuestas", []) or [])
        pregunta = None
        for respuesta in respuestas:
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
            id_profesional=getattr(self.controlador.profesional, "id_usuario", None),
            solo_lectura=self.controlador._resumen_entrevista_solo_lectura,
            analisis_bloqueado=self._pregunta_ia_bloqueada(numero_pregunta),
            parent=self.controlador.ventana_profesional,
        )
        if self._pregunta_ia_bloqueada(numero_pregunta):
            en_cola = self._pregunta_ia_en_cola(numero_pregunta)
            ventana.set_estado_analisis(
                "En cola..." if en_cola else "Analizando...",
                en_progreso=not en_cola,
                bloqueado=True,
            )
        self.controlador._ventana_detalle_analisis = ventana
        if not self.controlador._resumen_entrevista_solo_lectura:
            ventana.boton_analizar.clicked.connect(
                lambda: self._analizar_pregunta_desde_detalle(ventana, int(numero_pregunta))
            )
            ventana.nivel_profesional_actualizado.connect(self._on_nivel_profesional_actualizado)
        ventana.exec_()
        if self.controlador._ventana_detalle_analisis is ventana:
            self.controlador._ventana_detalle_analisis = None
        self._sincronizar_pregunta_entrevista(entrevista, pregunta)
        if self.controlador._hilo_analisis_ia is not None and self.controlador._hilo_analisis_ia.isRunning():
            return
        self._refrescar_resumen_entrevista_actual()

    def analizar_pregunta_desde_resumen(self, numero_pregunta):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay entrevista cargada.")
            return

        pregunta = self._buscar_pregunta_entrevista(entrevista, numero_pregunta)
        if pregunta is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se encontró la pregunta seleccionada.")
            return

        self._iniciar_analisis_ia([pregunta], analizar_todas=False)

    def analizar_entrevista_completa(self):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay entrevista cargada.")
            return

        preguntas = list(getattr(entrevista, "respuestas", []) or [])
        if not preguntas:
            self.controlador.msg.mostrar_advertencia("Atención", "La entrevista no tiene respuestas.")
            return

        self._iniciar_analisis_ia(preguntas, analizar_todas=True)

    def volver_desde_resumen_entrevista(self):
        self._sincronizar_entrevista_actual()
        if self.controlador._vista_origen_resumen_entrevista is not None:
            self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(
                self.controlador._vista_origen_resumen_entrevista
            )
            self.controlador.ventana_profesional.establecer_titulo_pantalla(
                self.controlador._titulo_origen_resumen_entrevista
            )
            return
        self.controlador.recargar_lista_actual()

    def _refrescar_resumen_entrevista_actual(self):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None:
            return
        if self.controlador._resumen_entrevista_solo_lectura:
            pantalla_resumen = self.controlador.ventana_profesional.pantalla_resumen_profesional_lectura
        else:
            pantalla_resumen = self.controlador.ventana_profesional.pantalla_resumen_profesional
        pantalla_resumen.refrescar_desde_modelo(entrevista)
        pantalla_resumen.set_estado_global_entrevista(
            getattr(entrevista, "estado_evaluacion_ia", "sin evaluacion")
        )
        self._aplicar_bloqueos_ia_en_resumen()

    @staticmethod
    def _normalizar_clave(texto):
        base = normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode("ascii")
        return " ".join(base.strip().lower().split())

    def _tiene_evaluacion_ia(self, solicitud):
        entrevista = getattr(solicitud, "entrevista", None)
        if entrevista is None:
            return False
        estado = self._normalizar_clave(getattr(entrevista, "estado_evaluacion_ia", ""))
        return estado == "evaluada"

    def _resumen_debe_ser_solo_lectura(self, solicitud):
        if solicitud is None:
            return True

        id_prof_solicitud = getattr(solicitud, "id_profesional", None)
        if id_prof_solicitud is None:
            return True

        estado = str(getattr(solicitud, "estado", "") or "").strip().lower()
        estados_finales = {
            Tipo_estado_solicitud.ACEPTADA.value,
            Tipo_estado_solicitud.RECHAZADA.value,
            Tipo_estado_solicitud.CANCELADA.value,
        }
        return estado in estados_finales

    def cargar_entrevista_solicitud(self, id_solicitud):
        datos_entrevista = encontrar_entrevista_por_solicitud(id_solicitud)
        if not datos_entrevista:
            return None

        return self._construir_entrevista_desde_fila(datos_entrevista)

    def cargar_entrevista_por_id(self, id_entrevista):
        datos_entrevista = encontrar_entrevista_por_id(id_entrevista)
        if not datos_entrevista:
            return None

        return self._construir_entrevista_desde_fila(datos_entrevista)

    def _construir_entrevista_desde_fila(self, datos_entrevista):
        entrevista = Entrevista(
            id_entrevista=datos_entrevista[0],
            id_interno=datos_entrevista[1],
            fecha=datos_entrevista[3],
        )
        entrevista.puntuacion_ia = datos_entrevista[4]
        entrevista.puntuacion_profesional = datos_entrevista[5] if len(datos_entrevista) > 5 else -1
        entrevista.estado_evaluacion_ia = datos_entrevista[6] if len(datos_entrevista) > 6 else "sin evaluacion"
        self._cargar_respuestas_entrevista(entrevista)
        return entrevista

    def _cargar_respuestas_entrevista(self, entrevista):
        if entrevista is None:
            return

        entrevista.respuestas = []
        entrevista.comentarios = self._cargar_comentarios_entrevista_modelo(entrevista.id_entrevista)
        entrevista.comentario_ia_general = self._cargar_comentario_ia_entrevista_modelo(
            entrevista.id_entrevista
        )
        datos_respuestas = obtener_respuestas_por_entrevista(entrevista.id_entrevista)
        for dato in datos_respuestas:
            nueva_pregunta = Pregunta(
                id_pregunta=dato.get("id_pregunta"),
                respuesta=dato.get("texto_respuesta", ""),
            )
            nueva_pregunta.id_respuesta = dato.get("id_respuesta")
            nueva_pregunta.set_archivo_audio(dato.get("ruta_audio"))
            nueva_pregunta.nivel_ia = dato.get("nivel_ia", -1)
            nueva_pregunta.nivel_profesional = dato.get("nivel_profesional", -1)
            nueva_pregunta.valoracion_ia = str(dato.get("analisis_ia", "") or "").strip()
            nueva_pregunta.comentarios = self._cargar_comentarios_respuesta_modelo(nueva_pregunta.id_respuesta)
            entrevista.add_respuestas(nueva_pregunta)

    @staticmethod
    def _cargar_comentarios_respuesta_modelo(id_respuesta):
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
    def _cargar_comentarios_entrevista_modelo(id_entrevista):
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
    def _cargar_comentario_ia_entrevista_modelo(id_entrevista):
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

    def _sincronizar_pregunta_entrevista(self, entrevista, pregunta):
        if entrevista is None or pregunta is None:
            return
        if getattr(pregunta, "id_respuesta", None):
            reemplazar_comentarios_respuesta(pregunta.id_respuesta, getattr(pregunta, "comentarios", []))

    def _sincronizar_entrevista_actual(self):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None or not getattr(entrevista, "id_entrevista", None):
            return

        for pregunta in list(getattr(entrevista, "respuestas", []) or []):
            self._sincronizar_pregunta_entrevista(entrevista, pregunta)

        reemplazar_comentarios_entrevista(
            entrevista.id_entrevista,
            getattr(entrevista, "comentarios", []),
        )

    def guardar_evaluacion_profesional_actual(self):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None or not getattr(entrevista, "id_entrevista", None):
            self.controlador.msg.mostrar_advertencia("Atencion", "No hay entrevista cargada.")
            return

        niveles = self._obtener_niveles_profesionales_completos(entrevista)
        if niveles is None:
            self.controlador.msg.mostrar_advertencia(
                "Atencion",
                "Debe completar los niveles profesionales de las 10 preguntas antes de guardar.",
            )
            return

        for pregunta in list(getattr(entrevista, "respuestas", []) or []):
            actualizar_nivel_profesional_respuesta(
                entrevista.id_entrevista,
                int(getattr(pregunta, "id_pregunta", 0) or 0),
                int(getattr(pregunta, "nivel_profesional", -1) or -1),
            )

        actualizar_puntuacion_profesional_entrevista(
            entrevista.id_entrevista,
            getattr(entrevista, "puntuacion_profesional", -1),
        )

        self.controlador.ventana_profesional.pantalla_resumen_profesional.marcar_evaluacion_profesional_pendiente(False)
        self.controlador.msg.mostrar_mensaje("Guardado", "La evaluacion profesional se ha guardado correctamente.")

    @staticmethod
    def _buscar_pregunta_entrevista(entrevista, numero_pregunta):
        respuestas = list(getattr(entrevista, "respuestas", []) or [])
        for respuesta in respuestas:
            try:
                if int(getattr(respuesta, "id_pregunta", -1)) == int(numero_pregunta):
                    return respuesta
            except (TypeError, ValueError):
                continue
        return None

    def _iniciar_analisis_ia(self, preguntas, analizar_todas):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None or not getattr(entrevista, "id_entrevista", None):
            self.controlador.msg.mostrar_advertencia("Atencion", "No hay entrevista cargada.")
            return

        payload = []
        for pregunta in preguntas:
            payload.append(
                {
                    "id_pregunta": int(getattr(pregunta, "id_pregunta", 0) or 0),
                    "respuesta": str(getattr(pregunta, "respuesta", "") or "").strip(),
                }
            )

        if self.controlador._hilo_analisis_ia is not None and self.controlador._hilo_analisis_ia.isRunning():
            if self._encolar_analisis_si_procede(
                entrevista_id=entrevista.id_entrevista,
                payload=payload,
                analizar_todas=analizar_todas,
            ):
                return
            self.controlador.msg.mostrar_advertencia("Atencion", "Ese analisis IA ya esta en curso o en cola.")
            return

        self._arrancar_analisis_ia(
            entrevista_id=entrevista.id_entrevista,
            payload=payload,
            analizar_todas=analizar_todas,
        )

    def _arrancar_analisis_ia(self, entrevista_id, payload, analizar_todas, ventana_detalle=None):
        if not payload:
            return

        ids_preguntas = {int(item["id_pregunta"]) for item in payload}
        self.controlador._analisis_ia_trabajo_activo = {
            "entrevista_id": int(entrevista_id),
            "ids_preguntas": ids_preguntas,
            "analizar_todas": bool(analizar_todas),
        }
        pantalla = self.controlador.ventana_profesional.pantalla_resumen_profesional
        if self._es_entrevista_resumen_actual(entrevista_id):
            pantalla.set_estado_global_entrevista("evaluando")
            if analizar_todas:
                self.controlador._progreso_analisis_completo_actual = 0
                self.controlador._progreso_analisis_completo_total = len(payload)
                pantalla.iniciar_progreso_analisis_completo(len(payload))
            else:
                self.controlador._progreso_analisis_completo_actual = 0
                self.controlador._progreso_analisis_completo_total = 0
                pantalla.ocultar_progreso_analisis_completo()
        else:
            self.controlador._progreso_analisis_completo_actual = 0
            self.controlador._progreso_analisis_completo_total = 0
        self.controlador._analisis_ia_global_activo = bool(analizar_todas and self._es_entrevista_resumen_actual(entrevista_id))
        self.controlador._ventana_detalle_analisis = self._ventana_detalle_valida(ventana_detalle)

        if analizar_todas:
            self.controlador._preguntas_ia_bloqueadas |= {
                (int(entrevista_id), int(item["id_pregunta"])) for item in payload
            }
            if self._es_entrevista_resumen_actual(entrevista_id):
                pantalla.bloquear_controles_ia(True)
        else:
            id_pregunta = int(payload[0]["id_pregunta"])
            self.controlador._preguntas_ia_bloqueadas.add((int(entrevista_id), id_pregunta))
            if self._es_entrevista_resumen_actual(entrevista_id):
                pantalla.bloquear_ia_pregunta(id_pregunta, True)

        if self._es_entrevista_resumen_actual(entrevista_id):
            for item in payload:
                pantalla.set_estado_analisis_pregunta(
                    item["id_pregunta"],
                    "En cola..." if analizar_todas else "Preparando analisis...",
                    en_progreso=not analizar_todas,
                )

        self.controlador._hilo_analisis_ia = HiloAnalisisIA(
            id_entrevista=entrevista_id,
            preguntas=payload,
            analizar_todas=analizar_todas,
            parent=self.controlador.ventana_profesional,
        )
        self.controlador._hilo_analisis_ia.senal_inicio_pregunta.connect(self._on_inicio_pregunta_ia)
        self.controlador._hilo_analisis_ia.senal_pregunta_analizada.connect(self._on_pregunta_analizada_ia)
        self.controlador._hilo_analisis_ia.senal_estado_entrevista.connect(self._on_estado_entrevista_ia)
        self.controlador._hilo_analisis_ia.senal_analisis_finalizado.connect(self._on_analisis_ia_finalizado)
        self.controlador._hilo_analisis_ia.senal_error.connect(self._on_error_analisis_ia)
        self.controlador._hilo_analisis_ia.finished.connect(self._limpiar_hilo_analisis_ia)
        self.controlador._hilo_analisis_ia.start()

    def _encolar_analisis_si_procede(self, entrevista_id, payload, analizar_todas, ventana_detalle=None):
        entrevista_id = int(entrevista_id)
        ids_nuevos = {(entrevista_id, int(item["id_pregunta"])) for item in payload}

        if ids_nuevos & set(self.controlador._preguntas_ia_bloqueadas):
            return False

        for trabajo in self.controlador._cola_analisis_ia:
            ids_trabajo = {
                (int(trabajo.get("entrevista_id")), int(item["id_pregunta"]))
                for item in trabajo.get("payload", [])
            }
            if ids_nuevos & ids_trabajo:
                return False

        self.controlador._cola_analisis_ia.append(
            {
                "entrevista_id": int(entrevista_id),
                "payload": payload,
                "analizar_todas": bool(analizar_todas),
                "ventana_detalle": self._ventana_detalle_valida(ventana_detalle),
            }
        )

        pantalla = self.controlador.ventana_profesional.pantalla_resumen_profesional
        for item in payload:
            numero = int(item["id_pregunta"])
            self.controlador._preguntas_ia_bloqueadas.add((entrevista_id, numero))
            if self._es_entrevista_resumen_actual(entrevista_id):
                pantalla.bloquear_ia_pregunta(numero, True)
                pantalla.set_estado_analisis_pregunta(numero, "En cola...", en_progreso=False)

        if analizar_todas and self._es_entrevista_resumen_actual(entrevista_id):
            pantalla.bloquear_controles_ia(True)

        ventana_detalle = self._ventana_detalle_valida(ventana_detalle)
        if ventana_detalle is not None:
            ventana_detalle.set_estado_analisis("En cola...", en_progreso=False, bloqueado=True)
        return True

    def _analizar_pregunta_desde_detalle(self, ventana, numero_pregunta):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None:
            self.controlador.msg.mostrar_advertencia("Atencion", "No hay entrevista cargada.")
            return

        pregunta = self._buscar_pregunta_entrevista(entrevista, numero_pregunta)
        if pregunta is None:
            self.controlador.msg.mostrar_advertencia("Atencion", "No se encontro la pregunta seleccionada.")
            return

        if self.controlador._hilo_analisis_ia is not None and self.controlador._hilo_analisis_ia.isRunning():
            payload = [
                {
                    "id_pregunta": int(getattr(pregunta, "id_pregunta", 0) or 0),
                    "respuesta": str(getattr(pregunta, "respuesta", "") or "").strip(),
                }
            ]
            if self._encolar_analisis_si_procede(
                entrevista_id=entrevista.id_entrevista,
                payload=payload,
                analizar_todas=False,
                ventana_detalle=ventana,
            ):
                return
            self.controlador.msg.mostrar_advertencia("Atencion", "Esa pregunta ya se esta analizando o ya esta en cola.")
            return

        self.controlador._ventana_detalle_analisis = self._ventana_detalle_valida(ventana)
        ventana.set_estado_analisis("Preparando analisis...", en_progreso=True)
        self._iniciar_analisis_ia([pregunta], analizar_todas=False)

    def _on_inicio_pregunta_ia(self, id_pregunta, texto_estado):
        trabajo_activo = self.controlador._analisis_ia_trabajo_activo or {}
        entrevista_id = trabajo_activo.get("entrevista_id")
        if self._es_entrevista_resumen_actual(entrevista_id):
            self.controlador.ventana_profesional.pantalla_resumen_profesional.set_estado_analisis_pregunta(
                id_pregunta,
                texto_estado,
                en_progreso=True,
            )
        detalle = self.controlador._ventana_detalle_analisis
        if detalle is not None and int(getattr(detalle, "numero", -1)) == int(id_pregunta):
            detalle.set_estado_analisis(texto_estado, en_progreso=True)

    def _on_pregunta_analizada_ia(self, payload):
        entrevista = self.controlador._entrevista_actual_resumen
        trabajo_activo = self.controlador._analisis_ia_trabajo_activo or {}
        entrevista_id = trabajo_activo.get("entrevista_id")
        if entrevista is not None and self._es_entrevista_resumen_actual(entrevista_id):
            pregunta = self._buscar_pregunta_entrevista(entrevista, payload.get("id_pregunta"))
            if pregunta is not None:
                pregunta.nivel_ia = payload.get("nivel", -1)
                pregunta.valoracion_ia = str(payload.get("justificacion", "") or "").strip()
        if self._es_entrevista_resumen_actual(entrevista_id):
            self.controlador.ventana_profesional.pantalla_resumen_profesional.actualizar_resultado_analisis_pregunta(
                payload.get("id_pregunta"),
                payload.get("nivel"),
                payload.get("justificacion"),
            )
        if (
            self.controlador._analisis_ia_global_activo
            and self.controlador._hilo_analisis_ia is not None
            and self._es_entrevista_resumen_actual(entrevista_id)
        ):
            self.controlador._progreso_analisis_completo_actual += 1
            self.controlador.ventana_profesional.pantalla_resumen_profesional.actualizar_progreso_analisis_completo(
                self.controlador._progreso_analisis_completo_actual
            )
        detalle = self.controlador._ventana_detalle_analisis
        if detalle is not None and int(getattr(detalle, "numero", -1)) == int(payload.get("id_pregunta", -1)):
            detalle.actualizar_resultado_ia(payload.get("nivel"), payload.get("justificacion"))

    def _on_estado_entrevista_ia(self, estado):
        entrevista = self.controlador._entrevista_actual_resumen
        trabajo_activo = self.controlador._analisis_ia_trabajo_activo or {}
        entrevista_id = trabajo_activo.get("entrevista_id")
        if entrevista is not None and self._es_entrevista_resumen_actual(entrevista_id):
            entrevista.estado_evaluacion_ia = estado
            self.controlador.ventana_profesional.pantalla_resumen_profesional.set_estado_global_entrevista(estado)
            self.controlador.ventana_profesional.pantalla_lista_solicitud.refrescar_tarjetas()

    def _on_analisis_ia_finalizado(self, payload):
        entrevista = self.controlador._entrevista_actual_resumen
        trabajo_activo = self.controlador._analisis_ia_trabajo_activo or {}
        entrevista_id = trabajo_activo.get("entrevista_id")
        if entrevista is not None and self._es_entrevista_resumen_actual(entrevista_id) and payload.get("analizar_todas"):
            entrevista.puntuacion_ia = payload.get("puntuacion_ia")
            conclusion_entrevista = str(payload.get("conclusion_entrevista", "") or "").strip()
            if conclusion_entrevista:
                entrevista.comentario_ia_general = {
                    "id": None,
                    "id_entrevista": getattr(entrevista, "id_entrevista", None),
                    "id_profesional": None,
                    "comentario": conclusion_entrevista,
                    "fecha": payload.get("fecha_conclusion_ia", ""),
                    "es_ia": True,
                }
            self.controlador.ventana_profesional.pantalla_resumen_profesional.finalizar_progreso_analisis_completo()
        elif self._es_entrevista_resumen_actual(entrevista_id):
            self.controlador.ventana_profesional.pantalla_resumen_profesional.ocultar_progreso_analisis_completo()
        self.controlador._progreso_analisis_completo_actual = 0
        self.controlador._progreso_analisis_completo_total = 0
        self._limpiar_bloqueos_ia_activos()
        if self._es_entrevista_resumen_actual(entrevista_id):
            self._refrescar_resumen_entrevista_actual()
        detalle = self.controlador._ventana_detalle_analisis
        if detalle is not None:
            detalle.set_estado_analisis("Analisis completado.", en_progreso=False)
        self.controlador.msg.mostrar_mensaje("IA", "Analisis IA completado correctamente.")

    def _on_error_analisis_ia(self, mensaje):
        pantalla = self.controlador.ventana_profesional.pantalla_resumen_profesional
        entrevista = self.controlador._entrevista_actual_resumen
        trabajo_activo = self.controlador._analisis_ia_trabajo_activo or {}
        entrevista_id = trabajo_activo.get("entrevista_id")
        if entrevista is not None and self._es_entrevista_resumen_actual(entrevista_id):
            entrevista.estado_evaluacion_ia = "sin evaluacion"
            pantalla.set_estado_global_entrevista("sin evaluacion")
        pendientes_en_cola = {
            (int(trabajo.get("entrevista_id")), int(item.get("id_pregunta", 0) or 0))
            for trabajo in self.controlador._cola_analisis_ia
            for item in trabajo.get("payload", [])
        }
        for clave in list(self.controlador._preguntas_ia_bloqueadas):
            if clave in pendientes_en_cola:
                continue
            if self._es_entrevista_resumen_actual(clave[0]):
                pantalla.set_estado_analisis_pregunta(clave[1], "Error en el analisis.", en_progreso=False)
        self._limpiar_bloqueos_ia_activos()
        if self._es_entrevista_resumen_actual(entrevista_id):
            pantalla.ocultar_progreso_analisis_completo()
        self.controlador._progreso_analisis_completo_actual = 0
        self.controlador._progreso_analisis_completo_total = 0
        self._restaurar_estado_preguntas_en_cola()
        detalle = self.controlador._ventana_detalle_analisis
        if detalle is not None:
            detalle.set_estado_analisis("Error en el analisis.", en_progreso=False)
        self.controlador.ventana_profesional.pantalla_lista_solicitud.refrescar_tarjetas()
        self.controlador.msg.mostrar_advertencia("Error IA", mensaje)

    def _on_nivel_profesional_actualizado(self, numero_pregunta, nivel):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None or not getattr(entrevista, "id_entrevista", None):
            return

        pregunta = self._buscar_pregunta_entrevista(entrevista, numero_pregunta)
        if pregunta is not None:
            pregunta.nivel_profesional = int(nivel)

        niveles = self._obtener_niveles_profesionales_completos(entrevista)
        if niveles is None:
            entrevista.puntuacion_profesional = -1
        else:
            puntuacion = calcular_puntuacion_total_profesional(niveles)
            entrevista.puntuacion_profesional = puntuacion

        self.controlador.ventana_profesional.pantalla_resumen_profesional.marcar_evaluacion_profesional_pendiente(True)
        self._refrescar_resumen_entrevista_actual()

    @staticmethod
    def _obtener_niveles_profesionales_completos(entrevista):
        respuestas = list(getattr(entrevista, "respuestas", []) or [])
        if len(respuestas) < 10:
            return None

        niveles_por_pregunta = {}
        for respuesta in respuestas:
            try:
                id_pregunta = int(getattr(respuesta, "id_pregunta", 0))
                nivel = int(getattr(respuesta, "nivel_profesional", -1))
            except (TypeError, ValueError):
                return None
            if id_pregunta < 1 or id_pregunta > 10 or nivel < 0:
                return None
            niveles_por_pregunta[id_pregunta] = nivel

        if any(indice not in niveles_por_pregunta for indice in range(1, 11)):
            return None

        return [niveles_por_pregunta[indice] for indice in range(1, 11)]

    def _limpiar_hilo_analisis_ia(self):
        self.controlador._hilo_analisis_ia = None
        self.controlador._analisis_ia_trabajo_activo = None
        self.controlador._ventana_detalle_analisis = None
        self._iniciar_siguiente_analisis_en_cola()

    def _aplicar_bloqueos_ia_en_resumen(self):
        pantalla = self.controlador.ventana_profesional.pantalla_resumen_profesional
        entrevista_actual = self._id_entrevista_resumen_actual()
        pantalla.bloquear_controles_ia(self._analisis_completo_bloquea_entrevista(entrevista_actual))
        pantalla.limpiar_bloqueos_ia_preguntas()
        for entrevista_id, numero in self.controlador._preguntas_ia_bloqueadas:
            if entrevista_actual == int(entrevista_id):
                pantalla.bloquear_ia_pregunta(numero, True)

    def _limpiar_bloqueos_ia_activos(self):
        pantalla = self.controlador.ventana_profesional.pantalla_resumen_profesional
        pendientes = set()
        for trabajo in self.controlador._cola_analisis_ia:
            for item in trabajo.get("payload", []):
                pendientes.add((int(trabajo.get("entrevista_id")), int(item.get("id_pregunta", 0) or 0)))

        self.controlador._analisis_ia_global_activo = False
        self.controlador._preguntas_ia_bloqueadas = pendientes
        entrevista_actual = self._id_entrevista_resumen_actual()
        pantalla.bloquear_controles_ia(self._analisis_completo_bloquea_entrevista(entrevista_actual))
        pantalla.limpiar_bloqueos_ia_preguntas()
        for entrevista_id, numero in pendientes:
            if entrevista_actual == int(entrevista_id):
                pantalla.bloquear_ia_pregunta(numero, True)

    def _pregunta_ia_bloqueada(self, numero_pregunta):
        entrevista_id = self._id_entrevista_resumen_actual()
        return self._analisis_completo_bloquea_entrevista(entrevista_id) or (
            int(entrevista_id or 0), int(numero_pregunta)
        ) in self.controlador._preguntas_ia_bloqueadas

    def _pregunta_ia_en_cola(self, numero_pregunta):
        entrevista_id = self._id_entrevista_resumen_actual()
        numero = int(numero_pregunta)
        for trabajo in self.controlador._cola_analisis_ia:
            for item in trabajo.get("payload", []):
                if (
                    int(trabajo.get("entrevista_id", 0) or 0) == int(entrevista_id or 0)
                    and int(item.get("id_pregunta", 0) or 0) == numero
                ):
                    return True
        return False

    def _iniciar_siguiente_analisis_en_cola(self):
        if not self.controlador._cola_analisis_ia:
            return
        siguiente = self.controlador._cola_analisis_ia.pop(0)
        self._arrancar_analisis_ia(
            entrevista_id=siguiente.get("entrevista_id"),
            payload=list(siguiente.get("payload", [])),
            analizar_todas=bool(siguiente.get("analizar_todas")),
            ventana_detalle=siguiente.get("ventana_detalle"),
        )

    def _restaurar_estado_preguntas_en_cola(self):
        pantalla = self.controlador.ventana_profesional.pantalla_resumen_profesional
        entrevista_actual = self._id_entrevista_resumen_actual()
        for trabajo in self.controlador._cola_analisis_ia:
            for item in trabajo.get("payload", []):
                if int(trabajo.get("entrevista_id", 0) or 0) == int(entrevista_actual or 0):
                    pantalla.set_estado_analisis_pregunta(
                        item.get("id_pregunta"),
                        "En cola...",
                        en_progreso=False,
                    )

    @staticmethod
    def _ventana_detalle_valida(ventana):
        if ventana is None:
            return None
        try:
            ventana.isVisible()
        except RuntimeError:
            return None
        return ventana

    def _id_entrevista_resumen_actual(self):
        entrevista = self.controlador._entrevista_actual_resumen
        if entrevista is None:
            return None
        return getattr(entrevista, "id_entrevista", None)

    def _es_entrevista_resumen_actual(self, entrevista_id):
        return int(entrevista_id or 0) == int(self._id_entrevista_resumen_actual() or 0)

    def _analisis_completo_bloquea_entrevista(self, entrevista_id):
        trabajo_activo = self.controlador._analisis_ia_trabajo_activo or {}
        if (
            trabajo_activo
            and bool(trabajo_activo.get("analizar_todas"))
            and int(trabajo_activo.get("entrevista_id", 0) or 0) == int(entrevista_id or 0)
        ):
            return True

        for trabajo in self.controlador._cola_analisis_ia:
            if (
                bool(trabajo.get("analizar_todas"))
                and int(trabajo.get("entrevista_id", 0) or 0) == int(entrevista_id or 0)
            ):
                return True
        return False
