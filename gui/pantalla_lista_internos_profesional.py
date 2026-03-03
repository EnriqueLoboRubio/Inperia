from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QFrame,
    QPushButton,
)

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

COLOR_RIESGO = {
    "Riesgo muy bajo": ("#DFF3C8", "#2E7D32"),
    "Riesgo bajo": ("#CBE8B5", "#2E7D32"),
    "Riesgo normal": ("#F4E29A", "#8A6D00"),
    "Riesgo elevado": ("#F2C1C1", "#C62828"),
    "Riesgo bastante elevado": ("#EEA8A8", "#A61F1F"),
    "Riesgo muy elevado": ("#E98E8E", "#8E1111"),
    "Riesgo máximo": ("#D77272", "#6D0000"),
}


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
        avatar.setFixedSize(56, 56)
        avatar.setStyleSheet(ESTILO_BOTON_PERFIL)
        cabecera.addWidget(avatar, alignment=Qt.AlignTop)

        bloque_info = QVBoxLayout()
        bloque_info.setSpacing(4)

        fila_nombre = QHBoxLayout()
        fila_nombre.setSpacing(10)
        lbl_nombre = QLabel(str(getattr(self.interno, "nombre", "-")))
        lbl_nombre.setStyleSheet(ESTILO_NOMBRE_INTERNO)
        fila_nombre.addWidget(lbl_nombre)

        clasif, pct, color_bg, color_txt = self._clasificar_riesgo(self.dato.get("puntuacion_global"))
        badge = QLabel(f"{clasif} ({pct})")
        badge.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color_bg};
                color: {color_txt};
                border-radius: 8px;
                padding: 3px 10px;
                font-size: 10pt;
                font-weight: 600;
            }}
            """
        )
        fila_nombre.addWidget(badge, alignment=Qt.AlignVCenter)
        fila_nombre.addStretch()
        bloque_info.addLayout(fila_nombre)

        lbl_rc = QLabel(f"RC-{getattr(self.interno, 'num_RC', '-')}")
        lbl_rc.setStyleSheet(ESTILO_NUM_RC)
        bloque_info.addWidget(lbl_rc)

        cabecera.addLayout(bloque_info, 1)

        boton_perfil = QPushButton("Ver perfil completo")
        boton_perfil.setCursor(Qt.PointingHandCursor)
        boton_perfil.setFixedHeight(38)
        boton_perfil.setStyleSheet(ESTILO_BOTON_SOLICITUD)
        boton_perfil.clicked.connect(lambda: self.ver_perfil_interno.emit(self.interno))
        cabecera.addWidget(boton_perfil, alignment=Qt.AlignTop)

        layout.addLayout(cabecera)

        fila_detalles = QHBoxLayout()
        fila_detalles.setSpacing(28)

        fila_detalles.addLayout(self._crear_bloque_texto("Delito", str(getattr(self.interno, "delito", "-") or "-")))
        fila_detalles.addLayout(self._crear_bloque_texto("Condena", f"{getattr(self.interno, 'condena', '-') or '-'} años"))
        fila_detalles.addLayout(self._crear_bloque_con_icono("Ingreso", self._fmt_fecha(getattr(self.interno, "fecha_ingreso", "-")), "assets/calendario.png"))

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
            )
        )
        fila_detalles.addStretch()
        layout.addLayout(fila_detalles)

    def _crear_bloque_texto(self, titulo, valor):
        cont = QVBoxLayout()
        cont.setSpacing(2)
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("color: #9A9A9A; font-size: 10pt; font-weight: 500;")
        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #6A6A6A; font-size: 12pt; font-weight: 500;")
        cont.addWidget(lbl_titulo)
        cont.addWidget(lbl_valor)
        return cont

    def _crear_bloque_con_icono(self, titulo, valor, ruta_icono, extra=None):
        cont = QVBoxLayout()
        cont.setSpacing(2)

        fila_tit = QHBoxLayout()
        fila_tit.setSpacing(6)
        icono = QLabel()
        tam = 16
        icono.setFixedSize(tam, tam)
        pix = QPixmap(ruta_icono).scaled(tam, tam, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icono.setPixmap(pix)
        fila_tit.addWidget(icono, alignment=Qt.AlignVCenter)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("color: #9A9A9A; font-size: 10pt; font-weight: 500;")
        fila_tit.addWidget(lbl_titulo, alignment=Qt.AlignVCenter)
        fila_tit.addStretch()

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #6A6A6A; font-size: 12pt; font-weight: 500;")
        cont.addLayout(fila_tit)
        cont.addWidget(lbl_valor)

        if extra:
            lbl_extra = QLabel(extra)
            lbl_extra.setStyleSheet("color: #808080; font-size: 10pt; font-weight: 500;")
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
    def _clasificar_riesgo(puntuacion):
        if puntuacion is None:
            color_bg, color_txt = "#D8D8D8", "#5A5A5A"
            return "Sin entrevista", "-", color_bg, color_txt

        try:
            valor = float(puntuacion)
        except Exception:
            color_bg, color_txt = "#D8D8D8", "#5A5A5A"
            return "Sin entrevista", "-", color_bg, color_txt

        for limite, texto, pct in BAREMOS_RIESGO:
            if valor <= limite:
                color_bg, color_txt = COLOR_RIESGO.get(texto, ("#D8D8D8", "#5A5A5A"))
                return texto, pct, color_bg, color_txt

        color_bg, color_txt = COLOR_RIESGO["Riesgo máximo"]
        return "Riesgo máximo", "100 %", color_bg, color_txt


class PantallaListaInternosProfesional(QWidget):
    ver_perfil_interno = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._datos = []
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
        self.input_busqueda.addAction(
            QIcon(QPixmap("assets/buscar.png").scaled(tam_icono, tam_icono, Qt.KeepAspectRatio, Qt.SmoothTransformation)),
            QLineEdit.LeadingPosition,
        )
        self.input_busqueda.textChanged.connect(self._actualizar_lista)
        fila_filtros.addWidget(self.input_busqueda, 1)

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
        layout_principal.addWidget(self.scroll, 1)

    def cargar_datos(self, datos):
        self._datos = list(datos or [])
        self._actualizar_lista()

    def _actualizar_lista(self):
        while self.layout_lista.count():
            item = self.layout_lista.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        texto = self.input_busqueda.text().strip().lower()
        filtrados = []
        for dato in self._datos:
            interno = dato.get("interno")
            nombre = str(getattr(interno, "nombre", "")).lower()
            rc = str(getattr(interno, "num_RC", "")).lower()
            if texto and texto not in nombre and texto not in rc:
                continue
            filtrados.append(dato)

        if not filtrados:
            lbl_vacio = QLabel("No hay internos asignados con los filtros seleccionados")
            lbl_vacio.setAlignment(Qt.AlignCenter)
            lbl_vacio.setStyleSheet("font-size: 12pt; color: #7A7A7A;")
            self.layout_lista.addWidget(lbl_vacio)
            self.layout_lista.addStretch()
            return

        for dato in filtrados:
            tarjeta = TarjetaInternoAsignado(dato)
            tarjeta.ver_perfil_interno.connect(self.ver_perfil_interno.emit)
            self.layout_lista.addWidget(tarjeta)

        self.layout_lista.addStretch()
