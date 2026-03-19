from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QIcon
from gui.estilos import *

FILTRO_ESTADO_A_VALOR = {
    "Todos": "todos",
    "Nuevas": "iniciada",
    "Iniciadas": "iniciada",
    "Pendientes": "pendiente",
    "Aceptada": "aceptada",
    "Aceptadas": "aceptada",
    "Rechazadas": "rechazada",
    "Canceladas": "cancelada",
    "Completadas": "completadas",
}

OPCIONES_COMBO_POR_TOP = {
    "por_evaluar": ["Todos", "Pendientes", "Iniciadas"],
    "completadas": ["Todos", "Aceptadas", "Canceladas", "Rechazadas"],
    "nuevas": ["Todos", "Pendientes", "Iniciadas"],
    None: ["Todos", "Nuevas", "Pendientes", "Completadas", "Aceptadas", "Rechazadas", "Canceladas"],
}

OPCIONES_COMBO_HISTORIAL = ["Todos", "Iniciadas", "Pendientes", "Aceptadas", "Rechazadas", "Canceladas"]


class TarjetaSolicitud(QFrame):
    """
    Widget que representa una solicitud en la lista principal. Muestra información básica del interno y la solicitud,
    y botones de asignar, ver perfil, ver entrevista y ver solicitud.
    """

    # Señales de la tarjeta, se emiten a controlador principal del profesional
    ver_perfil_interno = pyqtSignal(object)
    ver_entrevista = pyqtSignal(object)
    ver_solicitud = pyqtSignal(object)
    asignar_solicitud = pyqtSignal(object)

    def __init__(self, solicitud, interno, parent=None):
        super().__init__(parent)
        self.solicitud = solicitud
        self.interno = interno
        self._iniciar_ui()

    def _iniciar_ui(self):
        self.setStyleSheet(
            """
            QFrame {
                background-color: #F5F5F5;
                border: 1px solid #C9C9C9;
                border-radius: 18px;
            }
            QLabel { border: none; color: black; background: transparent; }
            """
        )

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 14, 20, 10)
        layout_principal.setSpacing(10)

        #CABECERA: perfil, nombre, num RC, fecha creación, estado
        cabecera = QHBoxLayout()
        cabecera.setSpacing(12)
    
        # Perfil
        boton_perfil_avatar = QPushButton(self._iniciales_interno())
        boton_perfil_avatar.setCursor(Qt.PointingHandCursor)
        boton_perfil_avatar.setFixedSize(52, 52)
        boton_perfil_avatar.setStyleSheet(ESTILO_BOTON_PERFIL)
        boton_perfil_avatar.setToolTip("Ver perfil del interno")
        boton_perfil_avatar.clicked.connect(lambda _=False: self.ver_perfil_interno.emit(self.interno))
        cabecera.addWidget(boton_perfil_avatar, alignment=Qt.AlignTop)

        bloque_info = QVBoxLayout()
        bloque_info.setSpacing(4)

        fila_nombre = QHBoxLayout()
        fila_nombre.setSpacing(8)

        # Nombre interno
        lbl_nombre = QLabel(self._nombre_interno())
        lbl_nombre.setStyleSheet(ESTILO_NOMBRE_INTERNO)
        # Columna fija para alinear el estado entre tarjetas.
        lbl_nombre.setFixedWidth(300)
        fila_nombre.addWidget(lbl_nombre)

        #Estado
        estado_txt, estado_color = ESTADOS_SOLICITUD_COLOR.get(
            str(getattr(self.solicitud, "estado", "")).lower(),
            ("Pendiente", "#F4E29A"),
        )
        estado_txt_color = color_texto_contraste(estado_color)
        lbl_estado = QLabel(estado_txt)
        lbl_estado.setStyleSheet(
            f"""
            QLabel {{
                background-color: {estado_color};
                color: {estado_txt_color};
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 10pt;
                font-weight: 500;
            }}
            """
        )
        fila_nombre.addWidget(lbl_estado, alignment=Qt.AlignVCenter)

        estado_ia_txt, estado_ia_color = self._estado_ia_visual()
        lbl_estado_ia = QLabel(f"IA: {estado_ia_txt}")
        lbl_estado_ia.setStyleSheet(f"QLabel {{ {estilo_chip_estado(estado_ia_color)} }}")
        fila_nombre.addWidget(lbl_estado_ia, alignment=Qt.AlignVCenter)

        fila_nombre.addStretch()

        bloque_info.addLayout(fila_nombre)

        # Número RC
        lbl_num_rc = QLabel(
            f"RC-{self._num_rc_interno()}"
        )
        lbl_num_rc.setStyleSheet(ESTILO_NUM_RC)
        bloque_info.addWidget(lbl_num_rc)

        # Fecha creación
        fila_fecha = QHBoxLayout()
        fila_fecha.setSpacing(6)

        icono_reloj = QLabel()
        tam_icono = lbl_num_rc.fontMetrics().height()  # mismo alto visual que la letra
        imagen = QPixmap("assets/reloj.png").scaled(
            tam_icono, tam_icono, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icono_reloj.setPixmap(imagen)
        icono_reloj.setFixedSize(tam_icono, tam_icono)

        fila_fecha.addWidget(icono_reloj, alignment=Qt.AlignVCenter)

        lbl_fecha = QLabel(f"{self._fecha_creacion()}")
        lbl_fecha.setStyleSheet(ESTILO_NUM_RC)
        fila_fecha.addWidget(lbl_fecha, alignment=Qt.AlignVCenter)
        fila_fecha.addStretch()
        bloque_info.addLayout(fila_fecha)

        cabecera.addLayout(bloque_info, 1)

        # botones de acción (ver entrevista, ver solicitud)
        botones_superior = QHBoxLayout()
        botones_superior.setSpacing(8)

        # Boton de entrevista: visible siempre, deshabilitado si no hay entrevista.
        boton_entrevista = self._crear_boton_accion("Ver entrevista")
        tiene_entrevista = self._tiene_entrevista_completa()
        boton_entrevista.setEnabled(tiene_entrevista)
        if tiene_entrevista:
            boton_entrevista.setToolTip("Ver entrevista del interno")
        else:
            boton_entrevista.setToolTip("Desactivado: esta solicitud aun no tiene entrevista.")
        if tiene_entrevista:
            boton_entrevista.clicked.connect(lambda _=False: self.ver_entrevista.emit(self.solicitud))
        botones_superior.addWidget(boton_entrevista)

        # Boton de solicitud
        boton_solicitud = self._crear_boton_accion("Ver solicitud")
        boton_solicitud.clicked.connect(lambda _=False: self.ver_solicitud.emit(self.solicitud))
        botones_superior.addWidget(boton_solicitud)

        # Boton de perfil
        boton_perfil = self._crear_boton_accion("Ver perfil")
        boton_perfil.setToolTip("Ver perfil del interno")
        boton_perfil.clicked.connect(lambda _=False: self.ver_perfil_interno.emit(self.interno))
        botones_superior.addWidget(boton_perfil)

        cabecera.addLayout(botones_superior)
        layout_principal.addLayout(cabecera)

        # Texto de conclusiones del profesional
        conc_prof = self._texto_conclusion_profesional()
        if conc_prof:
            caja_eval = QFrame()
            caja_eval.setStyleSheet(
                "QFrame { background-color: #E5E5E5; border: none; border-radius: 14px; }"
            )
            eval_layout = QVBoxLayout(caja_eval)
            eval_layout.setContentsMargins(16, 12, 16, 12)
            eval_layout.setSpacing(8)

            lbl_titulo_prof = QLabel("Conclusiones del profesional:")
            lbl_titulo_prof.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1A1A1A;")
            eval_layout.addWidget(lbl_titulo_prof)

            lbl_texto_prof = QLabel(conc_prof)
            lbl_texto_prof.setWordWrap(True)
            lbl_texto_prof.setStyleSheet("font-size: 11pt; color: #222222;")
            eval_layout.addWidget(lbl_texto_prof)

            layout_principal.addWidget(caja_eval)

        fila_inferior = QHBoxLayout()
        fila_inferior.addStretch()

        if self._sin_profesional_asignado():
            boton_asignar = self._crear_boton_accion("Asignar")
            boton_asignar.clicked.connect(lambda _=False: self.asignar_solicitud.emit(self.solicitud))
            fila_inferior.addWidget(boton_asignar)

        layout_principal.addLayout(fila_inferior)

    def _crear_boton_accion(self, texto):
        boton = QPushButton(texto)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedHeight(34)
        boton.setStyleSheet(
            ESTILO_BOTON_SOLICITUD
            + "\nQPushButton:disabled { background-color: #E0E0E0; opacity: 0.5; }"
        )
        return boton

    def _nombre_interno(self):
        return str(getattr(self.interno, "nombre", "Interno"))

    def _num_rc_interno(self):
        return str(getattr(self.interno, "num_RC", "----"))

    def _iniciales_interno(self):
        nombre = self._nombre_interno().strip()
        if not nombre:
            return "--"

        partes = [p for p in nombre.split() if p]
        if len(partes) == 1:
            return partes[0][:2].upper()
        return (partes[0][0] + partes[1][0]).upper()

    def _fecha_creacion(self):
        return str(getattr(self.solicitud, "fecha_creacion", ""))

    def _tiene_entrevista_completa(self):
        estado = str(getattr(self.solicitud, "estado", "") or "").strip().lower()
        if estado == "iniciada":
            return False
        return getattr(self.solicitud, "entrevista", None) is not None

    def _sin_profesional_asignado(self):
        return getattr(self.solicitud, "id_profesional", None) is None

    def _texto_conclusion_profesional(self):
        conc_prof = (getattr(self.solicitud, "conclusiones_profesional", "") or "").strip()
        return conc_prof

    def _estado_ia_visual(self):
        entrevista = getattr(self.solicitud, "entrevista", None)
        if entrevista is None:
            return obtener_estado_ia_visual("sin evaluacion")
        return obtener_estado_ia_visual(getattr(entrevista, "estado_evaluacion_ia", "sin evaluacion"))


class PantallaListaSolicitud(QWidget):
    """
    Pantalla principal de listado de solicitudes. Permite filtrar por estado y buscar por nombre o número de recluso.
    Muestra una tarjeta por cada solicitud, con información básica del interno y la solicitud"""

    # Señales de la pantalla, se emiten a controlador principal del profesional
    ver_perfil_interno = pyqtSignal(object)
    ver_entrevista = pyqtSignal(object)
    ver_solicitud = pyqtSignal(object)
    asignar_solicitud = pyqtSignal(object)
    filtro_superior_cambiado = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._solicitudes = []
        self._resultados_filtrados = []
        self._internos_por_rc = {}
        self._botones_top = {}
        self._top_activo = None
        self._sincronizando_filtros = False
        self._modo_historial = False
        self._tam_lote = 12
        self._num_visibles = 0
        self._estado_lista = "ok"
        self._mensaje_estado = ""

        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(35, 20, 60, 15)
        layout_principal.setSpacing(14)

        layout_principal.addLayout(self._crear_fila_estados_superior())
        layout_principal.addLayout(self._crear_fila_filtros())

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet(ESTILO_SCROLL)

        self.contenedor = QWidget()
        self.layout_lista = QVBoxLayout(self.contenedor)
        self.layout_lista.setContentsMargins(0, 0, 0, 0)
        self.layout_lista.setSpacing(10)
        self.layout_lista.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.contenedor)
        self.scroll.verticalScrollBar().valueChanged.connect(self._al_scroll_lista)
        layout_principal.addWidget(self.scroll, 1)

    def _crear_fila_estados_superior(self):
        """
        Crea la fila superior de botones de estado (pendientes, completadas, nuevas)
         y los configura para que activen el filtro correspondiente al hacer click.
        """
        fila = QHBoxLayout()
        fila.setSpacing(8)

        self._botones_top = {
            "por_evaluar": self._crear_boton_estado_superior("Por evaluar", "por_evaluar"),
            "completadas": self._crear_boton_estado_superior("Completadas", "completadas"),
            "nuevas": self._crear_boton_estado_superior("Nuevas", "nuevas"),
        }

        for boton in self._botones_top.values():
            fila.addWidget(boton)

        fila.addStretch()
        self._aplicar_estado_botones_superiores(None)
        return fila

    def _crear_boton_estado_superior(self, texto, clave):
        boton = QPushButton(texto)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedSize(150, 40)
        boton.clicked.connect(lambda _, c=clave: self._al_cambiar_filtro_superior(c))
        return boton

    def _crear_fila_filtros(self):
        fila = QHBoxLayout()
        fila.setSpacing(8)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por nombre o número de recluso ...")
        self.input_busqueda.setFixedHeight(40)
        self.input_busqueda.setStyleSheet(
            """
            QLineEdit {
                background-color: #ECECEC;
                border: 1px solid #BEBEBE;
                border-radius: 20px;
                padding: 0 16px;
                font-size: 11pt;
            }
            """
        )
        tam_icono_busqueda = self.input_busqueda.fontMetrics().height() + 3
        icono_busqueda_svg = QIcon("assets/buscar.svg")
        icono_busqueda = QIcon(icono_busqueda_svg.pixmap(tam_icono_busqueda, tam_icono_busqueda))
        self.input_busqueda.addAction(icono_busqueda, QLineEdit.LeadingPosition)
        self.input_busqueda.textChanged.connect(self._actualizar_lista)

        self.boton_filtros = QPushButton("Filtros")
        self.boton_filtros.setFixedSize(180, 40)
        self.boton_filtros.setCursor(Qt.PointingHandCursor)
        self.boton_filtros.setEnabled(False)
        self.boton_filtros.setToolTip("Desactivado: el filtrado avanzado aun no esta disponible.")
        tam_icono_filtros = self.boton_filtros.fontMetrics().height() + 3
        self.boton_filtros.setIcon(QIcon("assets/filtros.png"))
        self.boton_filtros.setIconSize(QSize(tam_icono_filtros, tam_icono_filtros))
        self.boton_filtros.setStyleSheet(
            """
            QPushButton {
                background-color: #ECECEC;
                border: 1px solid #BEBEBE;
                border-radius: 20px;
                color: #8E8E8E;
                font-size: 11pt;
                font-weight: 500;
                padding: 0 14px;
            }
            QPushButton:disabled { color: #A8A8A8; }
            """
        )

        self.combo_estado = QComboBox()
        self.combo_estado.setFixedSize(210, 40)
        self.combo_estado.addItems(OPCIONES_COMBO_POR_TOP[None])
        self.combo_estado.setToolTip("Filtrar por estado")
        self.combo_estado.setStyleSheet(ESTILO_COMBOBOX)
        self.combo_estado.currentTextChanged.connect(self._al_cambiar_combo_estado)

        fila.addWidget(self.input_busqueda, 1)
        fila.addWidget(self.boton_filtros)
        fila.addWidget(self.combo_estado)

        return fila

    def cargar_datos(self, solicitudes, internos):
        self._solicitudes = list(solicitudes or [])
        self._internos_por_rc = self._normalizar_internos(internos)
        self._estado_lista = "ok"
        self._mensaje_estado = ""
        self._actualizar_lista()

    def mostrar_error_carga(self, mensaje="Error al cargar las solicitudes. Intenta de nuevo."):
        self._estado_lista = "error"
        self._mensaje_estado = mensaje
        self._resultados_filtrados = []
        self._num_visibles = 0
        self._render_lista()

    def mostrar_sin_permiso(self, mensaje="No tienes permisos para ver esta lista."):
        self._estado_lista = "sin_permiso"
        self._mensaje_estado = mensaje
        self._resultados_filtrados = []
        self._num_visibles = 0
        self._render_lista()

    def aplicar_filtro_inicial(self, top_activo=None, combo_texto="Todos", solo_sin_profesional=False, modo_historial=False):
        self._top_activo = top_activo
        self._modo_historial = modo_historial
        self._aplicar_estado_botones_superiores(self._top_activo)
        self._configurar_combo_para_top(self._top_activo, combo_texto)
        self.input_busqueda.clear()
        self._actualizar_lista()

    def refrescar_tarjetas(self):
        if self._estado_lista != "ok":
            return
        self._render_lista()

    def _normalizar_internos(self, internos):
        if isinstance(internos, dict):
            return {str(k): v for k, v in internos.items()}

        resultado = {}
        for interno in internos or []:
            num_rc = getattr(interno, "num_RC", None)
            if num_rc is not None:
                resultado[str(num_rc)] = interno
        return resultado

    def _al_cambiar_filtro_superior(self, clave):
        self._top_activo = None if self._top_activo == clave else clave
        self._aplicar_estado_botones_superiores(self._top_activo)
        self._configurar_combo_para_top(self._top_activo, "Todos")
        self._actualizar_lista()
        self.filtro_superior_cambiado.emit(self._top_activo)

    def _al_cambiar_combo_estado(self, texto):
        if self._sincronizando_filtros:
            return

        # El combo queda restringido por el botón superior activo.
        self._actualizar_lista()

    def _configurar_combo_para_top(self, top_activo, seleccion="Todos"):
        if top_activo is None and self._modo_historial:
            opciones = OPCIONES_COMBO_HISTORIAL
        else:
            opciones = OPCIONES_COMBO_POR_TOP.get(top_activo, OPCIONES_COMBO_POR_TOP[None])
        self._sincronizando_filtros = True
        try:
            self.combo_estado.clear()
            self.combo_estado.addItems(opciones)
            if seleccion in opciones:
                self.combo_estado.setCurrentText(seleccion)
            else:
                self.combo_estado.setCurrentIndex(0)
        finally:
            self._sincronizando_filtros = False

    def _set_combo_estado(self, texto):
        self._sincronizando_filtros = True
        try:
            idx = self.combo_estado.findText(texto)
            if idx >= 0:
                self.combo_estado.setCurrentIndex(idx)
        finally:
            self._sincronizando_filtros = False

    def _aplicar_estado_botones_superiores(self, activo):
        for clave, boton in self._botones_top.items():
            if clave == activo:
                boton.setStyleSheet(
                    """
                    QPushButton {
                        background-color: black;
                        color: white;
                        border: 1px solid black;
                        border-radius: 10px;
                        font-size: 11pt;
                        font-weight: 600;
                    }
                    """
                )
            else:
                boton.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #F5F5F5;
                        color: black;
                        border: 1px solid #8C8C8C;
                        border-radius: 10px;
                        font-size: 11pt;
                        font-weight: 500;
                    }
                    QPushButton:hover { background-color: #EDEDED; }
                    """
                )

    def _actualizar_lista(self):
        self._resultados_filtrados = self._filtrar_solicitudes()
        self._num_visibles = min(self._tam_lote, len(self._resultados_filtrados))
        self._render_lista()

    def _al_scroll_lista(self, valor):
        barra = self.scroll.verticalScrollBar()
        if valor < (barra.maximum() - 80):
            return
        self._cargar_siguiente_lote()

    def _cargar_siguiente_lote(self):
        if self._num_visibles >= len(self._resultados_filtrados):
            return
        self._num_visibles = min(self._num_visibles + self._tam_lote, len(self._resultados_filtrados))
        self._render_lista()

    def _limpiar_lista(self):
        while self.layout_lista.count():
            item = self.layout_lista.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _render_lista(self):
        self._limpiar_lista()

        if self._estado_lista == "error":
            self._mostrar_mensaje_lista(self._mensaje_estado or "Error al cargar las solicitudes.")
            return
        if self._estado_lista == "sin_permiso":
            self._mostrar_mensaje_lista(self._mensaje_estado or "No tienes permisos para ver esta lista.")
            return

        if not self._resultados_filtrados:
            texto_busqueda = self.input_busqueda.text().strip()
            if not self._solicitudes:
                self._mostrar_mensaje_lista("No hay solicitudes disponibles.")
            elif texto_busqueda:
                self._mostrar_mensaje_lista("No hay resultados para la busqueda actual.")
            else:
                self._mostrar_mensaje_lista("No hay solicitudes con los filtros seleccionados.")
            return

        for solicitud, interno in self._resultados_filtrados[: self._num_visibles]:
            tarjeta = TarjetaSolicitud(solicitud, interno)
            tarjeta.ver_perfil_interno.connect(self.ver_perfil_interno.emit)
            tarjeta.ver_entrevista.connect(self.ver_entrevista.emit)
            tarjeta.ver_solicitud.connect(self.ver_solicitud.emit)
            tarjeta.asignar_solicitud.connect(self.asignar_solicitud.emit)
            self.layout_lista.addWidget(tarjeta)

        if self._num_visibles < len(self._resultados_filtrados):
            lbl_mas = QLabel(
                f"Mostrando {self._num_visibles} de {len(self._resultados_filtrados)} solicitudes. "
                "Desplaza para cargar mas."
            )
            lbl_mas.setAlignment(Qt.AlignCenter)
            lbl_mas.setStyleSheet("font-size: 10pt; color: #7A7A7A;")
            self.layout_lista.addWidget(lbl_mas)

        self.layout_lista.addStretch()

    def _mostrar_mensaje_lista(self, texto):
        lbl_vacio = QLabel(texto)
        lbl_vacio.setAlignment(Qt.AlignCenter)
        lbl_vacio.setStyleSheet("font-size: 12pt; color: #7A7A7A;")
        self.layout_lista.addWidget(lbl_vacio)
        self.layout_lista.addStretch()

    def _filtrar_solicitudes(self):
        filtro_texto = self.input_busqueda.text().strip().lower()
        filtro_estado = FILTRO_ESTADO_A_VALOR.get(self.combo_estado.currentText(), "todos")

        resultados = []
        for solicitud in self._solicitudes:
            interno = self._buscar_interno(solicitud)
            if interno is None:
                continue

            if not self._coincide_top_activo(solicitud):
                continue

            estado = str(getattr(solicitud, "estado", "")).lower()
            if not self._coincide_estado(estado, filtro_estado):
                continue

            nombre = str(getattr(interno, "nombre", "")).lower()
            num_rc = str(getattr(interno, "num_RC", "")).lower()
            if filtro_texto and filtro_texto not in nombre and filtro_texto not in num_rc:
                continue

            resultados.append((solicitud, interno))

        return resultados

    def _buscar_interno(self, solicitud):
        candidato = getattr(solicitud, "interno", None)
        if candidato is not None:
            return candidato

        id_interno = getattr(solicitud, "id_interno", None)
        if id_interno is None:
            id_interno = getattr(solicitud, "num_RC", None)

        if id_interno is None:
            return None

        return self._internos_por_rc.get(str(id_interno))

    def _coincide_estado(self, estado, filtro_estado):
        if filtro_estado == "todos":
            return True
        if filtro_estado == "completadas":
            return estado in {"aceptada", "rechazada", "cancelada"}
        return estado == filtro_estado

    def _coincide_top_activo(self, solicitud):
        estado = str(getattr(solicitud, "estado", "")).lower()
        sin_profesional = getattr(solicitud, "id_profesional", None) is None
        conc_prof = (getattr(solicitud, "conclusiones_profesional", "") or "").strip()

        if self._top_activo == "nuevas":
            return sin_profesional and estado in {"iniciada", "pendiente"}

        if self._top_activo == "por_evaluar":
            return (
                (not sin_profesional)
                and estado in {"iniciada", "pendiente"}
                and conc_prof == ""
            )

        if self._top_activo == "completadas":
            return estado in {"aceptada", "rechazada", "cancelada"}

        return True

