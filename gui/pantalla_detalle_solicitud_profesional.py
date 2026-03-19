from unicodedata import normalize

import html

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QScrollArea,
)

from gui.estilos import *


class PantallaDetalleSolicitudProfesional(QWidget):
    volver = pyqtSignal()
    ver_perfil_interno = pyqtSignal(object)

    DOCUMENTOS = [
        "Documento de identidad del familiar",
        "Comprobante de relación familiar",
        "Carta de invitación",
    ]

    COMPROMISOS = [
        "Cumplir estrictamente con los horarios establecidos",
        "Mantener contacto permanente con la institución",
        "No consumir alcohol ni sustancias prohibidas",
        "Presentar comprobantes de las actividades realizadas",
        "Informar cualquier cambio en la programación",
        "No alejarse del lugar autorizado sin permiso",
    ]

    ESTADOS_ENTREVISTA_IA = {
        "evaluada": ("Evaluada", "#D9C4F1"),
        "sin evaluacion": ("Sin evaluación", "#EFE6F8"),
        "evaluando": ("Evaluando", "#E7D6F7"),
    }

    TIPOS_PERMISO = {
        "familiar": "Familiar",
        "medico": "Médico",
        "educativo": "Educativo",
        "laboral": "Laboral",
        "defuncion": "Defunción",
        "juridico": "Jurí­dico",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._interno = None
        self._solicitud = None
        self._solo_lectura = False
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(10, 0, 60, 30)
        layout_principal.setSpacing(30)

        self._crear_cabecera_fija(layout_principal)
        self._crear_scroll_contenido(layout_principal)
        self._crear_fila_inferior(layout_principal)

    def _crear_cabecera_fija(self, layout_principal):
        cabecera = QFrame()
        lay = QHBoxLayout(cabecera)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        cuadro_info = self._crear_frame_apartado()
        fila_superior = QHBoxLayout(cuadro_info)
        fila_superior.setContentsMargins(16, 10, 16, 10)
        fila_superior.setSpacing(10)

        self.boton_perfil_interno = QPushButton("--")
        self.boton_perfil_interno.setFixedSize(52, 52)
        self.boton_perfil_interno.setCursor(Qt.PointingHandCursor)
        self.boton_perfil_interno.setStyleSheet(ESTILO_BOTON_PERFIL)
        self.boton_perfil_interno.clicked.connect(self._emitir_ver_perfil_interno)
        fila_superior.addWidget(self.boton_perfil_interno, alignment=Qt.AlignTop)

        bloque_info = QVBoxLayout()
        bloque_info.setSpacing(3)

        self.lbl_nombre = QLabel("-")
        self.lbl_nombre.setStyleSheet(ESTILO_NOMBRE_INTERNO)
        self.lbl_rc = QLabel("RC----")
        self.lbl_rc.setStyleSheet(ESTILO_NUM_RC)
        bloque_info.addWidget(self.lbl_nombre)
        bloque_info.addWidget(self.lbl_rc)

        fila_superior.addLayout(bloque_info)
        fila_superior.addSpacing(12)

        self.lbl_estado_solicitud = QLabel("-")
        self.lbl_estado_solicitud.setAlignment(Qt.AlignCenter)
        fila_superior.addWidget(self.lbl_estado_solicitud, alignment=Qt.AlignVCenter)

        self.lbl_estado_entrevista = QLabel("Sin evaluación")
        self.lbl_estado_entrevista.setAlignment(Qt.AlignCenter)
        fila_superior.addWidget(self.lbl_estado_entrevista, alignment=Qt.AlignVCenter)
        fila_superior.addStretch()

        cuadro_acciones = self._crear_frame_apartado()
        fila_acciones = QHBoxLayout(cuadro_acciones)
        fila_acciones.setContentsMargins(16, 10, 16, 10)
        fila_acciones.setSpacing(10)
        estilo_boton_accion = (
            ESTILO_BOTON_SOLICITUD
            + "\nQPushButton:disabled { background-color: #E0E0E0; opacity: 0.5; }"
        )
        estilo_boton_finalizar = (
            ESTILO_BOTON_SOLICITUD.replace("#2B2A2A", "#792A24").replace("#464545", "#C03930")
            + "\nQPushButton:disabled { background-color: #E0E0E0; opacity: 0.5; }"
        )

        self.boton_finalizar = QPushButton("Finalizar")
        self.boton_finalizar.setFixedHeight(34)
        self.boton_finalizar.setCursor(Qt.PointingHandCursor)
        self.boton_finalizar.setStyleSheet(estilo_boton_finalizar)
        self.boton_finalizar.setToolTip("Finalizar solicitud")
        self.boton_finalizar.clicked.connect(self._sin_accion)
        fila_acciones.addWidget(self.boton_finalizar)

        self.boton_ver_entrevista = QPushButton("Ver entrevista")
        self.boton_ver_entrevista.setFixedHeight(34)
        self.boton_ver_entrevista.setCursor(Qt.PointingHandCursor)
        self.boton_ver_entrevista.setStyleSheet(estilo_boton_accion)
        self.boton_ver_entrevista.setEnabled(False)
        self.boton_ver_entrevista.setToolTip("Desactivado: esta solicitud no tiene entrevista.")
        self.boton_ver_entrevista.clicked.connect(self._sin_accion)
        fila_acciones.addWidget(self.boton_ver_entrevista)

        self.boton_descargar_solicitud = QPushButton("Descargar solicitud")
        self.boton_descargar_solicitud.setFixedHeight(34)
        self.boton_descargar_solicitud.setCursor(Qt.PointingHandCursor)
        self.boton_descargar_solicitud.setStyleSheet(estilo_boton_accion)
        self.boton_descargar_solicitud.setToolTip("Descargar solicitud (próximamente).")
        self.boton_descargar_solicitud.clicked.connect(self._sin_accion)
        fila_acciones.addWidget(self.boton_descargar_solicitud)

        lay.addWidget(cuadro_info, 1)
        lay.addWidget(cuadro_acciones, 0)
        layout_principal.addWidget(cabecera)

    def _crear_scroll_contenido(self, layout_principal):
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet(ESTILO_SCROLL)

        contenedor = QWidget()
        self.layout_scroll = QVBoxLayout(contenedor)
        self.layout_scroll.setContentsMargins(10, 0, 10, 30)
        self.layout_scroll.setSpacing(30)

        self._crear_bloque_info_basica()
        self._crear_bloque_fecha_destino()
        self._crear_bloque_contactos()
        self._crear_bloque_observaciones()
        self._crear_bloque_compromisos_documentos()
        self._crear_bloque_conclusiones()
        self.layout_scroll.addStretch()

        self.scroll.setWidget(contenedor)
        layout_principal.addWidget(self.scroll, 1)

    def _crear_fila_inferior(self, layout_principal):
        fila = QHBoxLayout()
        fila.setContentsMargins(0, 0, 0, 0)
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setCursor(Qt.PointingHandCursor)
        self.boton_volver.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_volver.clicked.connect(self.volver.emit)
        fila.addWidget(self.boton_volver, alignment=Qt.AlignLeft)
        fila.addStretch()
        layout_principal.addLayout(fila)

    def _crear_bloque_info_basica(self):
        frame = self._crear_frame_apartado()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        fila_titulo = QHBoxLayout()
        fila_titulo.setContentsMargins(0, 0, 0, 0)
        fila_titulo.setSpacing(8)

        titulo = QLabel("Información básica")
        titulo.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size = max(33, titulo.fontMetrics().height())

        icono_documento = QLabel()
        icono_documento.setPixmap(
            QPixmap("assets/documento.png").scaled(
                icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_documento.setFixedSize(icon_size, icon_size)
        icono_documento.setStyleSheet("background: transparent; border: none;")

        fila_titulo.addWidget(icono_documento, alignment=Qt.AlignVCenter)
        fila_titulo.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo.addStretch()
        layout.addLayout(fila_titulo)
        layout.addSpacing(10)

        grid = QGridLayout()
        grid.setHorizontalSpacing(26)
        grid.setVerticalSpacing(6)

        self.lbl_identificador = self._crear_par_label(grid, 0, 0, "Identificador:")
        self.lbl_fecha_creacion = self._crear_par_label(grid, 0, 1, "Fecha creación:")
        self.lbl_tipo = self._crear_par_label(grid, 1, 0, "Tipo:")
        self.lbl_urgencia = self._crear_par_label(grid, 1, 1, "Urgencia:")
        self.lbl_motivo = self._crear_par_label(grid, 2, 0, "Motivo específico:", colspan=2)
        self.lbl_descripcion = self._crear_par_label(grid, 3, 0, "Descripción detallada:", colspan=2)
        self.lbl_descripcion.setWordWrap(True)

        layout.addLayout(grid)
        self.layout_scroll.addWidget(frame)

    def _crear_bloque_fecha_destino(self):
        frame = self._crear_frame_apartado()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        fila_titulo = QHBoxLayout()
        fila_titulo.setContentsMargins(0, 0, 0, 0)
        fila_titulo.setSpacing(8)

        titulo = QLabel("Fecha y destino")
        titulo.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size = max(33, titulo.fontMetrics().height())

        icono_calendario = QLabel()
        icono_calendario.setPixmap(
            QPixmap("assets/calendario.png").scaled(
                icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_calendario.setFixedSize(icon_size, icon_size)
        icono_calendario.setStyleSheet("background: transparent; border: none;")

        fila_titulo.addWidget(icono_calendario, alignment=Qt.AlignVCenter)
        fila_titulo.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo.addStretch()
        layout.addLayout(fila_titulo)
        layout.addSpacing(10)

        grid = QGridLayout()
        grid.setHorizontalSpacing(26)
        grid.setVerticalSpacing(6)

        self.lbl_fecha_inicio = self._crear_par_label(grid, 0, 0, "Fecha inicio:")
        self.lbl_hora_salida = self._crear_par_label(grid, 0, 1, "Hora salida:")
        self.lbl_fecha_fin = self._crear_par_label(grid, 1, 0, "Fecha fin:")
        self.lbl_hora_entrada = self._crear_par_label(grid, 1, 1, "Hora entrada:")
        self.lbl_direccion_destino = self._crear_par_label(grid, 2, 0, "Dirección destino:", colspan=2)

        layout.addLayout(grid)
        self.layout_scroll.addWidget(frame)

    def _crear_bloque_contactos(self):
        frame = self._crear_frame_apartado()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        fila_titulo = QHBoxLayout()
        fila_titulo.setContentsMargins(0, 0, 0, 0)
        fila_titulo.setSpacing(8)

        titulo = QLabel("Datos de contactos")
        titulo.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size = max(33, titulo.fontMetrics().height())

        icono_contactos = QLabel()
        icono_contactos.setPixmap(
            QPixmap("assets/contactos.png").scaled(
                icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_contactos.setFixedSize(icon_size, icon_size)
        icono_contactos.setStyleSheet("background: transparent; border: none;")

        fila_titulo.addWidget(icono_contactos, alignment=Qt.AlignVCenter)
        fila_titulo.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo.addStretch()
        layout.addLayout(fila_titulo)
        layout.addSpacing(10)

        lbl_cp = QLabel("Contacto Principal")
        lbl_cp.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
        layout.addWidget(lbl_cp)

        grid_cp = QGridLayout()
        grid_cp.setHorizontalSpacing(26)
        grid_cp.setVerticalSpacing(6)
        self.lbl_cp_nombre = self._crear_par_label(grid_cp, 0, 0, "Nombre:")
        self.lbl_cp_telf = self._crear_par_label(grid_cp, 0, 1, "Teléfono:")
        self.lbl_cp_relacion = self._crear_par_label(grid_cp, 0, 2, "Relación:")
        self.lbl_cp_direccion = self._crear_par_label(grid_cp, 1, 0, "Dirección:", colspan=3)
        layout.addLayout(grid_cp)

        lbl_cs = QLabel("Contacto Secundario")
        lbl_cs.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
        layout.addWidget(lbl_cs)

        grid_cs = QGridLayout()
        grid_cs.setHorizontalSpacing(26)
        grid_cs.setVerticalSpacing(6)
        self.lbl_cs_nombre = self._crear_par_label(grid_cs, 0, 0, "Nombre:")
        self.lbl_cs_telf = self._crear_par_label(grid_cs, 0, 1, "Teléfono:")
        self.lbl_cs_relacion = self._crear_par_label(grid_cs, 0, 2, "Relación:")
        layout.addLayout(grid_cs)

        self.layout_scroll.addWidget(frame)

    def _crear_bloque_observaciones(self):
        self.frame_observaciones = self._crear_frame_apartado()
        layout = QVBoxLayout(self.frame_observaciones)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        fila_titulo = QHBoxLayout()
        fila_titulo.setContentsMargins(0, 0, 0, 0)
        fila_titulo.setSpacing(8)

        titulo = QLabel("Observaciones del interno")
        titulo.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size = max(33, titulo.fontMetrics().height())

        icono_observaciones = QLabel()
        icono_observaciones.setPixmap(
            QPixmap("assets/info.png").scaled(
                icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_observaciones.setFixedSize(icon_size, icon_size)
        icono_observaciones.setStyleSheet("background: transparent; border: none;")

        fila_titulo.addWidget(icono_observaciones, alignment=Qt.AlignVCenter)
        fila_titulo.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo.addStretch()
        layout.addLayout(fila_titulo)
        layout.addSpacing(6)

        self.lbl_observaciones = QLabel("-")
        self.lbl_observaciones.setWordWrap(True)
        self.lbl_observaciones.setStyleSheet(ESTILO_TEXTO)
        layout.addWidget(self.lbl_observaciones)

        self.layout_scroll.addWidget(self.frame_observaciones)

    def _crear_bloque_compromisos_documentos(self):
        fila = QHBoxLayout()
        fila.setSpacing(10)

        frame_comp = self._crear_frame_apartado()
        lay_comp = QVBoxLayout(frame_comp)
        lay_comp.setContentsMargins(14, 10, 14, 10)
        lay_comp.setSpacing(8)
        fila_titulo_comp = QHBoxLayout()
        fila_titulo_comp.setContentsMargins(0, 0, 0, 0)
        fila_titulo_comp.setSpacing(8)

        titulo_comp = QLabel("Compromisos")
        titulo_comp.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size_comp = max(33, titulo_comp.fontMetrics().height())

        icono_compromiso = QLabel()
        icono_compromiso.setPixmap(
            QPixmap("assets/compromiso.png").scaled(
                icon_size_comp, icon_size_comp, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_compromiso.setFixedSize(icon_size_comp, icon_size_comp)
        icono_compromiso.setStyleSheet("background: transparent; border: none;")

        fila_titulo_comp.addWidget(icono_compromiso, alignment=Qt.AlignVCenter)
        fila_titulo_comp.addWidget(titulo_comp, alignment=Qt.AlignVCenter)
        fila_titulo_comp.addStretch()
        lay_comp.addLayout(fila_titulo_comp)
        lay_comp.addSpacing(10)
        self.lbl_compromisos = QLabel("-")
        self.lbl_compromisos.setWordWrap(True)
        self.lbl_compromisos.setStyleSheet(ESTILO_TEXTO)
        lay_comp.addWidget(self.lbl_compromisos)

        frame_docs = self._crear_frame_apartado()
        lay_docs = QVBoxLayout(frame_docs)
        lay_docs.setContentsMargins(14, 10, 14, 10)
        lay_docs.setSpacing(8)
        fila_titulo_docs = QHBoxLayout()
        fila_titulo_docs.setContentsMargins(0, 0, 0, 0)
        fila_titulo_docs.setSpacing(8)

        titulo_docs = QLabel("Documentos")
        titulo_docs.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size_docs = max(33, titulo_docs.fontMetrics().height())

        icono_docs = QLabel()
        icono_docs.setPixmap(
            QPixmap("assets/doc_solicitud.png").scaled(
                icon_size_docs, icon_size_docs, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_docs.setFixedSize(icon_size_docs, icon_size_docs)
        icono_docs.setStyleSheet("background: transparent; border: none;")

        fila_titulo_docs.addWidget(icono_docs, alignment=Qt.AlignVCenter)
        fila_titulo_docs.addWidget(titulo_docs, alignment=Qt.AlignVCenter)
        fila_titulo_docs.addStretch()
        lay_docs.addLayout(fila_titulo_docs)
        lay_docs.addSpacing(10)
        self.lbl_docs = QLabel("-")
        self.lbl_docs.setWordWrap(True)
        self.lbl_docs.setStyleSheet(ESTILO_TEXTO)
        lay_docs.addWidget(self.lbl_docs)

        fila.addWidget(frame_comp, 1)
        fila.addWidget(frame_docs, 1)
        self.layout_scroll.addLayout(fila)

    def _crear_bloque_conclusiones(self):
        self.frame_conclusiones = self._crear_frame_apartado()
        layout = QVBoxLayout(self.frame_conclusiones)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        fila_titulo = QHBoxLayout()
        fila_titulo.setContentsMargins(0, 0, 0, 0)
        fila_titulo.setSpacing(8)

        titulo = QLabel("Conclusiones")
        titulo.setStyleSheet(ESTILO_TITULO_PASO)
        icon_size = max(33, titulo.fontMetrics().height())

        icono_conclusion = QLabel()
        icono_conclusion.setPixmap(
            QPixmap("assets/conclusion.png").scaled(
                icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icono_conclusion.setFixedSize(icon_size, icon_size)
        icono_conclusion.setStyleSheet("background: transparent; border: none;")

        fila_titulo.addWidget(icono_conclusion, alignment=Qt.AlignVCenter)
        fila_titulo.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo.addStretch()
        layout.addLayout(fila_titulo)
        layout.addSpacing(10)

        self.lbl_conclusiones = QLabel("-")
        self.lbl_conclusiones.setWordWrap(True)
        self.lbl_conclusiones.setStyleSheet(ESTILO_TEXTO)
        layout.addWidget(self.lbl_conclusiones)

        self.layout_scroll.addWidget(self.frame_conclusiones)

    @staticmethod
    def _crear_frame_apartado():
        frame = QFrame()
        frame.setObjectName("apartado")
        frame.setStyleSheet(ESTILO_APARTADO_FRAME)
        return frame

    def _crear_par_label(self, grid, fila, col, titulo, colspan=1):
        lbl = QLabel(self._texto_campo(titulo, "-"))
        lbl.setWordWrap(True)
        grid.addWidget(lbl, fila, col, 1, colspan)
        return lbl

    @staticmethod
    def _estilo_inline(estilo):
        txt = str(estilo or "").strip()
        if "QLabel" in txt:
            ini = txt.find("{")
            fin = txt.rfind("}")
            if ini != -1 and fin != -1 and fin > ini:
                txt = txt[ini + 1 : fin]
        return " ".join(txt.replace("\n", " ").split())

    @staticmethod
    def _texto_campo(titulo, valor):
        titulo_txt = html.escape(str(titulo or "").strip())
        valor_txt = html.escape(PantallaDetalleSolicitudProfesional._txt(valor))
        estilo_titulo = PantallaDetalleSolicitudProfesional._estilo_inline(ESTILO_TITULO_APARTADO)
        estilo_valor = PantallaDetalleSolicitudProfesional._estilo_inline(ESTILO_TEXTO)
        return (
            f'<span style="{estilo_titulo}">{titulo_txt} </span>'
            f'<span style="{estilo_valor}">{valor_txt}</span>'
        )

    def cargar_datos(self, solicitud, interno):
        self._solicitud = solicitud
        self._interno = interno
        tiene_entrevista = getattr(solicitud, "entrevista", None) is not None
        self.boton_ver_entrevista.setEnabled(tiene_entrevista)
        if tiene_entrevista:
            self.boton_ver_entrevista.setToolTip("Ver entrevista del interno")
        else:
            self.boton_ver_entrevista.setToolTip("Desactivado: esta solicitud no tiene entrevista.")

        nombre = str(getattr(interno, "nombre", "") or "-")
        num_rc = str(getattr(interno, "num_RC", getattr(solicitud, "id_interno", "-")) or "-")
        self.lbl_nombre.setText(nombre)
        self.lbl_rc.setText(f"RC-{num_rc}")
        self.boton_perfil_interno.setText(self._iniciales(nombre))

        estado_sol = str(getattr(solicitud, "estado", "") or "").lower()
        texto_estado, color_estado = ESTADOS_SOLICITUD_COLOR.get(estado_sol, ("Pendiente", "#F4E29A"))
        self.lbl_estado_solicitud.setText(texto_estado)
        self.lbl_estado_solicitud.setStyleSheet(
            f"background-color: {color_estado}; color: {color_texto_contraste(color_estado)}; "
            "border-radius: 10px; padding: 3px 10px; font-size: 10pt; font-weight: 500;"
        )

        estado_eval = self._estado_entrevista_desde_solicitud(solicitud)
        self._aplicar_estado_entrevista(estado_eval)

        self.lbl_identificador.setText(self._texto_campo("Identificador:", getattr(solicitud, "id_solicitud", "-")))
        self.lbl_fecha_creacion.setText(self._texto_campo("Fecha creación:", getattr(solicitud, "fecha_creacion", "")))
        self.lbl_tipo.setText(
            self._texto_campo(
                "Tipo:",
                self.TIPOS_PERMISO.get(str(getattr(solicitud, "tipo", "")).lower(), self._txt(getattr(solicitud, "tipo", ""))),
            )
        )
        self.lbl_urgencia.setText(self._texto_campo("Urgencia:", self._capitalizar(getattr(solicitud, "urgencia", ""))))
        self.lbl_motivo.setText(self._texto_campo("Motivo específico:", getattr(solicitud, "motivo", "")))
        self.lbl_descripcion.setText(self._texto_campo("Descripción detallada:", getattr(solicitud, "descripcion", "")))

        self.lbl_fecha_inicio.setText(self._texto_campo("Fecha inicio:", getattr(solicitud, "fecha_inicio", "")))
        self.lbl_hora_salida.setText(self._texto_campo("Hora salida:", getattr(solicitud, "hora_salida", "")))
        self.lbl_fecha_fin.setText(self._texto_campo("Fecha fin:", getattr(solicitud, "fecha_fin", "")))
        self.lbl_hora_entrada.setText(self._texto_campo("Hora entrada:", getattr(solicitud, "hora_llegada", "")))
        dir_dest = self._unir_con_coma(
            getattr(solicitud, "direccion", ""),
            getattr(solicitud, "destino", ""),
            getattr(solicitud, "provincia", ""),
            getattr(solicitud, "cod_pos", ""),
        )
        self.lbl_direccion_destino.setText(self._texto_campo("Dirección destino:", dir_dest))

        self.lbl_cp_nombre.setText(self._texto_campo("Nombre:", getattr(solicitud, "nombre_cp", "")))
        self.lbl_cp_telf.setText(self._texto_campo("Teléfono:", getattr(solicitud, "telf_cp", "")))
        self.lbl_cp_relacion.setText(self._texto_campo("Relación:", getattr(solicitud, "relacion_cp", "")))
        self.lbl_cp_direccion.setText(self._texto_campo("Dirección:", getattr(solicitud, "direccion_cp", "")))
        self.lbl_cs_nombre.setText(self._texto_campo("Nombre:", getattr(solicitud, "nombre_cs", "")))
        self.lbl_cs_telf.setText(self._texto_campo("Teléfono:", getattr(solicitud, "telf_cs", "")))
        self.lbl_cs_relacion.setText(self._texto_campo("Relación:", getattr(solicitud, "relacion_cs", "")))

        observaciones = str(getattr(solicitud, "observaciones", "") or "").strip()
        self.frame_observaciones.setVisible(bool(observaciones))
        self.lbl_observaciones.setText(observaciones)

        compromisos = self._seleccionados_por_bitmask(getattr(solicitud, "compromisos", 0), self.COMPROMISOS)
        docs = self._seleccionados_por_bitmask(getattr(solicitud, "docs", 0), self.DOCUMENTOS)
        self.lbl_compromisos.setText(self._lista_a_texto(compromisos))
        self.lbl_docs.setText(self._lista_a_texto(docs))

        conclusiones = str(getattr(solicitud, "conclusiones_profesional", "") or "").strip()
        self.frame_conclusiones.setVisible(bool(conclusiones))
        self.lbl_conclusiones.setText(conclusiones)
        self.set_modo_solo_lectura(False)

    def set_modo_solo_lectura(self, solo_lectura):
        self._solo_lectura = bool(solo_lectura)
        tiene_entrevista = getattr(getattr(self, "_solicitud", None), "entrevista", None) is not None
        self.boton_finalizar.setEnabled(not self._solo_lectura)
        self.boton_descargar_solicitud.setEnabled(not self._solo_lectura)
        self.boton_ver_entrevista.setEnabled(tiene_entrevista)

        if self._solo_lectura:
            self.boton_finalizar.setToolTip("Desactivado: solicitud abierta en modo lectura.")
            self.boton_descargar_solicitud.setToolTip("Desactivado: solicitud abierta en modo lectura.")
            if tiene_entrevista:
                self.boton_ver_entrevista.setToolTip("Ver entrevista en modo lectura")
            else:
                self.boton_ver_entrevista.setToolTip("Desactivado: esta solicitud no tiene entrevista.")

    def _emitir_ver_perfil_interno(self):
        if self._interno is not None:
            self.ver_perfil_interno.emit(self._interno)

    def _estado_entrevista_desde_solicitud(self, solicitud):
        entrevista = getattr(solicitud, "entrevista", None)
        estado = getattr(entrevista, "estado_evaluacion_ia", "") if entrevista else ""
        normalizado = self._normalizar_clave(estado)
        if normalizado in self.ESTADOS_ENTREVISTA_IA:
            return normalizado
        return "sin evaluacion"

    def _aplicar_estado_entrevista(self, estado_normalizado):
        texto, color = self.ESTADOS_ENTREVISTA_IA.get(estado_normalizado, ("Sin evaluación", "#F2A0A0"))
        self.lbl_estado_entrevista.setText(texto)
        self.lbl_estado_entrevista.setStyleSheet(
            f"background-color: {color}; color: {color_texto_contraste(color)}; "
            "border-radius: 8px; padding: 3px 10px; font-size: 10pt; font-weight: 500;"
        )

    @staticmethod
    def _normalizar_clave(texto):
        base = normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode("ascii")
        return " ".join(base.strip().lower().split())

    @staticmethod
    def _txt(valor):
        texto = str(valor or "").strip()
        return texto if texto else "-"

    @staticmethod
    def _capitalizar(valor):
        texto = str(valor or "").strip()
        return texto.capitalize() if texto else "-"

    @staticmethod
    def _iniciales(nombre):
        partes = [p for p in str(nombre or "").split() if p]
        if not partes:
            return "--"
        if len(partes) == 1:
            return partes[0][:2].upper()
        return f"{partes[0][0]}{partes[1][0]}".upper()

    @staticmethod
    def _unir_con_coma(*valores):
        partes = [str(v).strip() for v in valores if str(v or "").strip()]
        return ", ".join(partes) if partes else "-"

    @staticmethod
    def _seleccionados_por_bitmask(valor_mask, opciones):
        try:
            mask = int(valor_mask or 0)
        except (TypeError, ValueError):
            mask = 0
        seleccionados = []
        for i, opcion in enumerate(opciones):
            if mask & (1 << i):
                seleccionados.append(opcion)
        return seleccionados

    @staticmethod
    def _lista_a_texto(items):
        if not items:
            return "Sin elementos"
        return "\n".join([f"- {item}" for item in items])

    @staticmethod
    def _sin_accion():
        return
