import os

from PyQt5.QtCore import QStandardPaths
from PyQt5.QtWidgets import QDialog, QFileDialog

from db.solicitud_db import (
    actualizar_estado_y_conclusiones_solicitud,
    asignar_profesional_a_solicitud,
    listar_solicitudes_nuevas_sin_profesional,
    listar_solicitudes_profesional,
)
from gui.ventana_finalizar_solicitud_profesional import VentanaFinalizarSolicitudProfesional
from models.solicitud import Solicitud
from utils.documentoPDF import DocumentoPDF
from utils.enums import Tipo_estado_solicitud


class ProfesionalSolicitudesController:
    """
    Controlador para la gestiÃ³n de las solicitudes.
    """

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar_lista_nuevas(self):
        self.controlador._modo_lista_actual = "nuevas"
        filas = listar_solicitudes_nuevas_sin_profesional()
        self._mostrar_lista_solicitudes(filas, "nuevas", "Todos", True)

    def mostrar_lista_pendientes(self):
        if not self.controlador.profesional:
            return

        self.controlador._modo_lista_actual = "pendientes"
        filas = listar_solicitudes_profesional(self.controlador.profesional.id_usuario)
        self._mostrar_lista_solicitudes(filas, "por_evaluar", "Todos", False)

    def mostrar_lista_historial(self):
        if not self.controlador.profesional:
            return

        self.controlador._modo_lista_actual = "historial"
        filas = listar_solicitudes_profesional(self.controlador.profesional.id_usuario)
        self._mostrar_lista_solicitudes(filas, None, "Todos", False)

    def mostrar_lista_completadas(self):
        if not self.controlador.profesional:
            return

        self.controlador._modo_lista_actual = "completadas"
        filas = listar_solicitudes_profesional(self.controlador.profesional.id_usuario)
        self._mostrar_lista_solicitudes(filas, "completadas", "Todos", False)

    def gestionar_filtro_superior_lista(self, top_activo):
        if top_activo == "nuevas":
            self.mostrar_lista_nuevas()
        elif top_activo == "por_evaluar":
            self.mostrar_lista_pendientes()
        elif top_activo == "completadas":
            self.mostrar_lista_completadas()

    def asignar_solicitud_a_profesional(self, solicitud):
        if not self.controlador.profesional or not solicitud:
            return

        id_solicitud = getattr(solicitud, "id_solicitud", None)
        if id_solicitud is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se pudo identificar la solicitud.")
            return

        ok = asignar_profesional_a_solicitud(id_solicitud, self.controlador.profesional.id_usuario)
        if not ok:
            self.controlador.msg.mostrar_advertencia("Atención", "No se pudo asignar la solicitud.")
            return

        self.controlador.msg.mostrar_mensaje("Solicitud asignada", "Solicitud asignada correctamente")
        self.controlador.actualizar_inicio_profesional()
        self.recargar_lista_actual()

    def recargar_lista_actual(self):
        if self.controlador._modo_lista_actual == "nuevas":
            self.mostrar_lista_nuevas()
        elif self.controlador._modo_lista_actual == "pendientes":
            self.mostrar_lista_pendientes()
        elif self.controlador._modo_lista_actual == "completadas":
            self.mostrar_lista_completadas()
        elif self.controlador._modo_lista_actual == "historial":
            self.mostrar_lista_historial()

    def _mostrar_lista_solicitudes(self, filas_solicitud, top_activo, combo_texto, solo_sin_profesional):
        solicitudes = [self._construir_solicitud_desde_fila(fila) for fila in (filas_solicitud or [])]
        internos = self.controlador.internos._cargar_internos_para_solicitudes(solicitudes)

        pantalla = self.controlador.ventana_profesional.pantalla_lista_solicitud
        pantalla.cargar_datos(solicitudes, internos)
        pantalla.aplicar_filtro_inicial(
            top_activo=top_activo,
            combo_texto=combo_texto,
            solo_sin_profesional=solo_sin_profesional,
            modo_historial=(self.controlador._modo_lista_actual == "historial"),
        )
        self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(pantalla)
        titulos_modo = {
            "nuevas": "Nuevas solicitudes",
            "pendientes": "Solicitudes por evaluar",
            "completadas": "Solicitudes completadas",
            "historial": "Historial de solicitudes",
        }
        self.controlador.ventana_profesional.establecer_titulo_pantalla(
            titulos_modo.get(self.controlador._modo_lista_actual, "Solicitudes")
        )

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
        solicitud.entrevista = self.controlador.entrevistas.cargar_entrevista_solicitud(solicitud.id_solicitud)
        return solicitud

    def mostrar_detalle_solicitud(self, solicitud):
        return self._mostrar_detalle_solicitud(solicitud, solo_lectura=False)

    def mostrar_solicitud_desde_perfil_interno(self, id_solicitud):
        pantalla_perfil = self.controlador.ventana_profesional.pantalla_perfil_interno
        solicitudes = list(getattr(pantalla_perfil, "_solicitudes_actuales", []) or [])
        solicitud = None
        for fila in solicitudes:
            try:
                if int(fila[0]) == int(id_solicitud):
                    solicitud = self._construir_solicitud_desde_fila(fila)
                    break
            except (TypeError, ValueError, IndexError):
                continue

        if solicitud is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se pudo cargar la solicitud seleccionada.")
            return

        return self._mostrar_detalle_solicitud(solicitud, solo_lectura=True)

    def _mostrar_detalle_solicitud(self, solicitud, solo_lectura=False):
        if solicitud is None:
            return

        self.controlador._vista_origen_detalle_solicitud = self.controlador.ventana_profesional.stacked_widget.currentWidget()
        self.controlador._titulo_origen_detalle_solicitud = self.controlador.ventana_profesional.titulo_pantalla.text()
        self.controlador._detalle_solicitud_solo_lectura = bool(solo_lectura)

        interno = self.controlador.internos._obtener_interno_de_solicitud(solicitud)
        if interno is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No se encontró la información del interno.")
            return

        pantalla = self.controlador.ventana_profesional.pantalla_detalle_solicitud
        pantalla.cargar_datos(solicitud, interno)
        self._configurar_acciones_detalle(pantalla, solicitud)
        pantalla.set_modo_solo_lectura(solo_lectura)
        self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(pantalla)
        self.controlador.ventana_profesional.establecer_titulo_pantalla("Solicitud")

    def finalizar_solicitud_desde_detalle(self):
        pantalla = self.controlador.ventana_profesional.pantalla_detalle_solicitud
        solicitud = getattr(pantalla, "_solicitud", None)
        interno = getattr(pantalla, "_interno", None)
        if solicitud is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay solicitud cargada para finalizar.")
            return

        puede_finalizar, motivo = self._puede_finalizar_o_descargar(solicitud)
        if not puede_finalizar:
            self.controlador.msg.mostrar_advertencia("Atención", motivo)
            return

        ventana = VentanaFinalizarSolicitudProfesional(
            solicitud=solicitud,
            parent=self.controlador.ventana_profesional,
        )
        if ventana.exec_() != QDialog.Accepted:
            return

        datos = ventana.get_datos() or {}
        estado_nuevo = str(datos.get("estado", "") or "").strip().lower()
        conclusiones = str(datos.get("conclusiones_profesional", "") or "").strip()
        if not conclusiones:
            self.controlador.msg.mostrar_advertencia("Atención", "Debe indicar una conclusión para finalizar la solicitud.")
            return

        if not self.controlador.entrevistas._tiene_evaluacion_ia(solicitud):
            confirmar = self.controlador.msg.mostrar_confirmacion(
                "Sin evaluación automática",
                "La entrevista asociada no tiene evaluación de IA.\n"
                "¿Está seguro de concluir la solicitud?\n"
                "Esta decisión es definitiva.",
            )
            if not confirmar:
                return

        ok = actualizar_estado_y_conclusiones_solicitud(
            getattr(solicitud, "id_solicitud", None),
            estado_nuevo,
            conclusiones,
        )
        if not ok:
            self.controlador.msg.mostrar_advertencia("Error BD", "No se pudo actualizar la solicitud en base de datos.")
            return

        solicitud.estado = estado_nuevo
        solicitud.conclusiones_profesional = conclusiones
        self.controlador._recargar_lista_al_salir_detalle = True
        if interno is not None:
            pantalla.cargar_datos(solicitud, interno)
            self._configurar_acciones_detalle(pantalla, solicitud)

        self.controlador.actualizar_inicio_profesional()
        self.controlador.msg.mostrar_mensaje("Verificación", "La solicitud se ha finalizado y guardado correctamente.")

    def descargar_solicitud_desde_detalle(self):
        pantalla = self.controlador.ventana_profesional.pantalla_detalle_solicitud
        solicitud = getattr(pantalla, "_solicitud", None)
        interno = getattr(pantalla, "_interno", None)
        if solicitud is None:
            self.controlador.msg.mostrar_advertencia("Atención", "No hay solicitud cargada para descargar.")
            return

        puede_descargar, motivo = self._puede_finalizar_o_descargar(solicitud)
        if not puede_descargar:
            self.controlador.msg.mostrar_advertencia("Atención", motivo)
            return

        incluir_detalles_entrevista = self.controlador.msg.mostrar_confirmacion(
            "Incluir entrevista",
            "¿Desea incluir detalles de la entrevista en el PDF?\n\n"
            "Si selecciona 'No', se generará el mismo PDF estándar del interno.",
        )

        try:
            ruta_guardado, _ = QFileDialog.getSaveFileName(
                self.controlador.ventana_profesional,
                "Guardar Solicitud",
                os.path.join(
                    QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
                    f"Solicitud_{getattr(solicitud, 'id_solicitud', '')}.pdf",
                ),
                "PDF Files (*.pdf)",
            )
            if not ruta_guardado:
                return

            DocumentoPDF.generar_pdf_solicitud(
                solicitud,
                ruta_guardado,
                interno,
                incluir_detalles_entrevista=incluir_detalles_entrevista,
            )
            self.controlador.msg.mostrar_mensaje(
                "Descarga exitosa",
                f"La solicitud se ha guardado en:\n{ruta_guardado}",
            )
        except Exception as e:
            self.controlador.msg.mostrar_advertencia(
                "Error al descargar",
                f"No se pudo guardar la solicitud:\n{str(e)}",
            )

    def volver_desde_detalle_solicitud(self):
        self.controlador._detalle_solicitud_solo_lectura = False
        if self.controlador._recargar_lista_al_salir_detalle:
            self.controlador._recargar_lista_al_salir_detalle = False
            self.recargar_lista_actual()
            return

        if self.controlador._vista_origen_detalle_solicitud is not None:
            self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(self.controlador._vista_origen_detalle_solicitud)
            self.controlador.ventana_profesional.establecer_titulo_pantalla(self.controlador._titulo_origen_detalle_solicitud)
            return
        self.recargar_lista_actual()

    def _configurar_acciones_detalle(self, pantalla, solicitud):
        if self.controlador._detalle_solicitud_solo_lectura:
            pantalla.boton_finalizar.setEnabled(False)
            pantalla.boton_descargar_solicitud.setEnabled(False)
            pantalla.boton_finalizar.setToolTip("Desactivado: solicitud abierta en modo lectura.")
            pantalla.boton_descargar_solicitud.setToolTip("Desactivado: solicitud abierta en modo lectura.")
            return

        puede_operar, motivo = self._puede_finalizar_o_descargar(solicitud)
        tooltip_bloqueo = f"Desactivado: {motivo[0].lower()}{motivo[1:]}" if motivo else ""

        pantalla.boton_finalizar.setEnabled(puede_operar)
        pantalla.boton_descargar_solicitud.setEnabled(puede_operar)

        if puede_operar:
            pantalla.boton_finalizar.setToolTip("Finalizar solicitud")
            pantalla.boton_descargar_solicitud.setToolTip("Descargar solicitud")
        else:
            pantalla.boton_finalizar.setToolTip(tooltip_bloqueo)
            pantalla.boton_descargar_solicitud.setToolTip(tooltip_bloqueo)

    def _puede_finalizar_o_descargar(self, solicitud):
        id_prof_solicitud = getattr(solicitud, "id_profesional", None)
        id_prof_actual = getattr(self.controlador.profesional, "id_usuario", None)

        estado = str(getattr(solicitud, "estado", "") or "").strip().lower()
        conclusiones = str(getattr(solicitud, "conclusiones_profesional", "") or "").strip()
        estados_finales = {
            Tipo_estado_solicitud.ACEPTADA.value,
            Tipo_estado_solicitud.RECHAZADA.value,
            Tipo_estado_solicitud.CANCELADA.value,
        }
        solicitud_finalizada = estado in estados_finales and bool(conclusiones)

        if id_prof_solicitud is None:
            return False, "La solicitud y su entrevista no están asignadas a ningún profesional."

        if id_prof_solicitud != id_prof_actual:
            return False, "La solicitud y su entrevista están asignadas a otro profesional."

        if solicitud_finalizada:
            return False, "La solicitud ya ha sido finalizada."

        return True, ""
