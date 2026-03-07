from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QFrame,
    QPushButton,
)
from datetime import datetime, date

from gui.estilos import *


BAREMOS_RIESGO = [
    (887.5, "Riesgo muy bajo", "5 %"),
    (910.0, "Riesgo bajo", "10 %"),
    (920.0, "Riesgo bajo", "15 %"),
    (928.0, "Riesgo normal", "20 %"),
    (932.5, "Riesgo normal", "25 %"),
    (940.0, "Riesgo normal", "30 %"),
    (942.5, "Riesgo normal", "35 %"),
    (945.0, "Riesgo elevado", "40 %"),
    (947.5, "Riesgo elevado", "45 %"),
    (955.5, "Riesgo elevado", "50 %"),
    (959.0, "Riesgo elevado", "55 %"),
    (962.5, "Riesgo bastante elevado", "60 %"),
    (966.25, "Riesgo bastante elevado", "65 %"),
    (970.0, "Riesgo bastante elevado", "70 %"),
    (977.0, "Riesgo bastante elevado", "75 %"),
    (985.0, "Riesgo muy elevado", "80 %"),
    (988.75, "Riesgo muy elevado", "85 %"),
    (992.5, "Riesgo muy elevado", "90 %"),
    (996.5, "Riesgo muy elevado", "95 %"),
]


class TarjetaInternoAsignado(QFrame):
    ver_perfil_interno = pyqtSignal(object)

    def __init__(self, dato, parent=None):
        super().__init__(parent)
        self.dato = dato or {}
        self.interno = self.dato.get("interno")
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(12)

        cabecera = QHBoxLayout()
        cabecera.setSpacing(12)

        avatar = QPushButton(self._iniciales())
        avatar.setEnabled(False)
        avatar.setFixedSize(52, 52)
        avatar.setStyleSheet(ESTILO_BOTON_PERFIL)
        cabecera.addWidget(avatar, alignment=Qt.AlignTop)

        bloque_info = QVBoxLayout()
        bloque_info.setSpacing(4)

        fila_nombre = QHBoxLayout()
        fila_nombre.setSpacing(10)
        lbl_nombre = QLabel(str(getattr(self.interno, "nombre", "-")))
        lbl_nombre.setStyleSheet(ESTILO_NOMBRE_INTERNO)
        # Mantiene la misma columna visual para que el estado quede alineado entre tarjetas.
        lbl_nombre.setFixedWidth(300)
        fila_nombre.addWidget(lbl_nombre)

        clasif, pct, color_bg, color_txt = self._clasificar_riesgo(self.dato.get("puntuacion_global"))
        lbl_riesgo = QLabel(f"{clasif} ({pct})")
        lbl_riesgo.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color_bg};
                color: {color_txt};
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 10pt;
                font-weight: 500;
            }}
            """
        )
        fila_nombre.addWidget(lbl_riesgo, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        tendencia_txt = self._texto_tendencia(self.dato.get("tendencia_riesgo"))
        if tendencia_txt:
            lbl_tendencia = QLabel(tendencia_txt.strip())
            lbl_tendencia.setStyleSheet("font-size: 11pt; font-weight: 700; color: #333333;")
            fila_nombre.addWidget(lbl_tendencia, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        fila_nombre.addStretch()
        bloque_info.addLayout(fila_nombre)

        lbl_rc = QLabel(f"RC-{getattr(self.interno, 'num_RC', '-')}")
        lbl_rc.setStyleSheet(ESTILO_NUM_RC)
        bloque_info.addWidget(lbl_rc)

        cabecera.addLayout(bloque_info, 1)

        bloque_acciones = QHBoxLayout()
        bloque_acciones.setSpacing(8)
        boton_perfil = QPushButton("Ver perfil completo")
        boton_perfil.setCursor(Qt.PointingHandCursor)
        boton_perfil.setFixedHeight(38)
        boton_perfil.setStyleSheet(ESTILO_BOTON_SOLICITUD)
        boton_perfil.clicked.connect(lambda: self.ver_perfil_interno.emit(self.interno))
        bloque_acciones.addWidget(boton_perfil)

        boton_ultima_entrevista = QPushButton("Ver última entrevista")
        boton_ultima_entrevista.setFixedHeight(34)
        boton_ultima_entrevista.setEnabled(False)
        boton_ultima_entrevista.setToolTip("Proximamente disponible")
        boton_ultima_entrevista.setStyleSheet(ESTILO_BOTON_SOLICITUD)
        bloque_acciones.addWidget(boton_ultima_entrevista)

        cabecera.addLayout(bloque_acciones, 0)

        layout.addLayout(cabecera)

        fila_detalles = QGridLayout()
        fila_detalles.setHorizontalSpacing(24)
        fila_detalles.setVerticalSpacing(0)
        fila_detalles.setColumnMinimumWidth(0, 150)
        fila_detalles.setColumnMinimumWidth(1, 120)
        fila_detalles.setColumnMinimumWidth(2, 180)
        fila_detalles.setColumnMinimumWidth(3, 280)
        fila_detalles.setColumnStretch(3, 1)

        fila_detalles.addLayout(
            self._crear_bloque_texto("Delito", str(getattr(self.interno, "delito", "-") or "-")),
            0, 0, alignment=Qt.AlignTop | Qt.AlignLeft
        )
        fila_detalles.addLayout(
            self._crear_bloque_texto("Condena", f"{getattr(self.interno, 'condena', '-') or '-'} años"),
            0, 1, alignment=Qt.AlignTop | Qt.AlignLeft
        )
        fila_detalles.addLayout(
            self._crear_bloque_con_icono("Ingreso", self._fmt_fecha(getattr(self.interno, "fecha_ingreso", "-")), "assets/calendario.png"),
            0, 2, alignment=Qt.AlignTop | Qt.AlignLeft
        )

        ultima_entrevista = self._fmt_fecha(self.dato.get("fecha_ultima_entrevista"))
        puntuacion = self.dato.get("puntuacion_global")
        if puntuacion is None:
            puntuacion_txt = "Puntuación directa: -"
        else:
            puntuacion_txt = f"Puntuación directa: {float(puntuacion):.2f}"
        fila_detalles.addLayout(
            self._crear_bloque_con_icono(
                "Última entrevista",
                ultima_entrevista,
                "assets/reloj.png",
                extra=puntuacion_txt,
            ),
            0, 3, alignment=Qt.AlignTop | Qt.AlignLeft
        )
        layout.addLayout(fila_detalles)

        fila_pie = QHBoxLayout()
        fila_pie.addStretch()
        lbl_hace_dias = QLabel(self._texto_hace_dias(self.dato.get("fecha_ultima_entrevista")))
        lbl_hace_dias.setStyleSheet(ESTILO_DATO_SECUNDARIO_PERFIL)
        fila_pie.addWidget(lbl_hace_dias, alignment=Qt.AlignRight)
        layout.addLayout(fila_pie)

    def _crear_bloque_texto(self, titulo, valor):
        cont = QVBoxLayout()
        cont.setSpacing(2)
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(ESTILO_TITULO_DETALLE_PERFIL)
        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(ESTILO_DATO_PERFIL)
        cont.addWidget(lbl_titulo)
        cont.addWidget(lbl_valor)
        return cont

    def _crear_bloque_con_icono(self, titulo, valor, ruta_icono, extra=None):
        cont = QVBoxLayout()
        cont.setSpacing(2)

        fila_tit = QHBoxLayout()
        fila_tit.setSpacing(6)
        icono = QLabel()
        tam = 20
        icono.setFixedSize(tam, tam)
        pix = QPixmap(ruta_icono).scaled(tam, tam, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icono.setPixmap(pix)
        fila_tit.addWidget(icono, alignment=Qt.AlignVCenter)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(ESTILO_TITULO_DETALLE_PERFIL)
        fila_tit.addWidget(lbl_titulo, alignment=Qt.AlignVCenter)
        fila_tit.addStretch()

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(ESTILO_DATO_PERFIL)
        cont.addLayout(fila_tit)
        cont.addWidget(lbl_valor)

        if extra:
            lbl_extra = QLabel(extra)
            lbl_extra.setStyleSheet(ESTILO_DATO_SECUNDARIO_PERFIL)
            cont.addWidget(lbl_extra)

        return cont

    def _iniciales(self):
        nombre = str(getattr(self.interno, "nombre", "") or "").strip()
        partes = [p for p in nombre.split() if p]
        if not partes:
            return "--"
        if len(partes) == 1:
            return partes[0][:2].upper()
        return (partes[0][0] + partes[1][0]).upper()

    @staticmethod
    def _fmt_fecha(fecha):
        texto = str(fecha or "-").strip()
        if texto in {"", "-", "None"}:
            return "-"
        if len(texto) >= 10 and texto[4] == "-" and texto[7] == "-":
            return f"{texto[8:10]}/{texto[5:7]}/{texto[:4]}"
        return texto

    @staticmethod
    def _parse_fecha_iso(fecha):
        texto = str(fecha or "").strip()
        if not texto or texto in {"-", "None"}:
            return None
        try:
            if len(texto) >= 10 and texto[4] == "-" and texto[7] == "-":
                return datetime.strptime(texto[:10], "%Y-%m-%d").date()
            if len(texto) >= 10 and texto[2] == "/" and texto[5] == "/":
                return datetime.strptime(texto[:10], "%d/%m/%Y").date()
        except ValueError:
            return None
        return None

    @classmethod
    def _texto_hace_dias(cls, fecha):
        fecha_dt = cls._parse_fecha_iso(fecha)
        if fecha_dt is None:
            return "Sin entrevista"
        dias = (date.today() - fecha_dt).days
        if dias <= 0:
            return "hace 0 d"
        return f"hace {dias} d"

    @staticmethod
    def _texto_tendencia(tendencia):
        if tendencia == "sube":
            return " \u2191"
        if tendencia == "baja":
            return " \u2193"
        return ""

    @staticmethod
    def _clasificar_riesgo(puntuacion):
        if puntuacion is None:
            color_bg = "#D8D8D8"
            return "Sin entrevista", "-", color_bg, color_texto_contraste(color_bg)

        try:
            valor = float(puntuacion)
        except Exception:
            color_bg = "#D8D8D8"
            return "Sin entrevista", "-", color_bg, color_texto_contraste(color_bg)

        for limite, texto, pct in BAREMOS_RIESGO:
            if valor <= limite:
                color_bg = COLOR_RIESGO.get(texto, "#D8D8D8")
                return texto, pct, color_bg, color_texto_contraste(color_bg)

        color_bg = COLOR_RIESGO["Riesgo maximo"]
        return "Riesgo maximo", "100 %", color_bg, color_texto_contraste(color_bg)


class PantallaListaInternosProfesional(QWidget):
    ver_perfil_interno = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._datos = []
        self._datos_filtrados = []
        self._tam_lote = 12
        self._num_visibles = 0
        self._estado_lista = "ok"
        self._mensaje_estado = ""
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(35, 20, 35, 15)
        layout_principal.setSpacing(14)

        fila_filtros = QHBoxLayout()
        fila_filtros.setSpacing(8)

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
        tam_icono = self.input_busqueda.fontMetrics().height() + 3
        icono_busqueda_svg = QIcon("assets/buscar.svg")
        icono_busqueda = QIcon(icono_busqueda_svg.pixmap(tam_icono, tam_icono))
        self.input_busqueda.addAction(icono_busqueda, QLineEdit.LeadingPosition)
        self.input_busqueda.textChanged.connect(self._actualizar_lista)
        fila_filtros.addWidget(self.input_busqueda, 1)

        self.boton_filtros = QPushButton("Filtros")
        self.boton_filtros.setFixedSize(180, 40)
        self.boton_filtros.setCursor(Qt.PointingHandCursor)
        self.boton_filtros.setEnabled(False)
        self.boton_filtros.setToolTip("Se habilitara cuando se implemente el filtrado avanzado")
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
        fila_filtros.addWidget(self.boton_filtros)

        layout_principal.addLayout(fila_filtros)

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

    def cargar_datos(self, datos):
        self._datos = list(datos or [])
        self._estado_lista = "ok"
        self._mensaje_estado = ""
        self._actualizar_lista()

    def mostrar_error_carga(self, mensaje="Error al cargar los internos. Intenta de nuevo."):
        self._estado_lista = "error"
        self._mensaje_estado = mensaje
        self._datos_filtrados = []
        self._num_visibles = 0
        self._render_lista()

    def mostrar_sin_permiso(self, mensaje="No tienes permisos para ver esta lista."):
        self._estado_lista = "sin_permiso"
        self._mensaje_estado = mensaje
        self._datos_filtrados = []
        self._num_visibles = 0
        self._render_lista()

    def _actualizar_lista(self):
        texto = self.input_busqueda.text().strip().lower()
        filtrados = []
        for dato in self._datos:
            interno = dato.get("interno")
            nombre = str(getattr(interno, "nombre", "")).lower()
            rc = str(getattr(interno, "num_RC", "")).lower()
            if texto and texto not in nombre and texto not in rc:
                continue
            filtrados.append(dato)

        self._datos_filtrados = filtrados
        self._num_visibles = min(self._tam_lote, len(self._datos_filtrados))
        self._render_lista()

    def _al_scroll_lista(self, valor):
        barra = self.scroll.verticalScrollBar()
        if valor < (barra.maximum() - 80):
            return
        self._cargar_siguiente_lote()

    def _cargar_siguiente_lote(self):
        if self._num_visibles >= len(self._datos_filtrados):
            return
        self._num_visibles = min(self._num_visibles + self._tam_lote, len(self._datos_filtrados))
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
            self._mostrar_mensaje_lista(self._mensaje_estado or "Error al cargar los internos.")
            return
        if self._estado_lista == "sin_permiso":
            self._mostrar_mensaje_lista(self._mensaje_estado or "No tienes permisos para ver esta lista.")
            return

        if not self._datos_filtrados:
            texto_busqueda = self.input_busqueda.text().strip()
            if not self._datos:
                self._mostrar_mensaje_lista("No hay internos asignados actualmente.")
            elif texto_busqueda:
                self._mostrar_mensaje_lista("No hay resultados para la busqueda actual.")
            else:
                self._mostrar_mensaje_lista("No hay internos con los filtros seleccionados.")
            return

        for dato in self._datos_filtrados[: self._num_visibles]:
            tarjeta = TarjetaInternoAsignado(dato)
            tarjeta.ver_perfil_interno.connect(self.ver_perfil_interno.emit)
            self.layout_lista.addWidget(tarjeta)

        if self._num_visibles < len(self._datos_filtrados):
            lbl_mas = QLabel(
                f"Mostrando {self._num_visibles} de {len(self._datos_filtrados)} internos. "
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



