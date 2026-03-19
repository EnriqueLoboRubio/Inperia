from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QSizePolicy, QButtonGroup
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from db.pregunta_db import obtener_preguntas_como_diccionario
from gui.estilos import *


class PantallaListaModificarPreguntas(QWidget):
    """
    Pantalla de listado de preguntas para modificar.
    Por ahora solo muestra la lista y el boton de editar sin comportamiento.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._preguntas_data = {}
        self.grupo_botones_editar = QButtonGroup(self)
        self._iniciar_ui()
        self.cargar_preguntas()

    def _iniciar_ui(self):
        principal_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(ESTILO_SCROLL)

        self.scroll_content_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content_widget)
        self.scroll_content_layout.setAlignment(Qt.AlignTop)
        self.scroll_content_layout.setSpacing(20)
        self.scroll_content_layout.setContentsMargins(50, 20, 60, 0)

        self.scroll_area.setWidget(self.scroll_content_widget)
        principal_layout.addWidget(self.scroll_area, 1)

    def crear_tarjeta_pregunta(self, id_pregunta, numero_mostrar, titulo, texto):
        tarjeta_frame = QFrame()
        tarjeta_frame.setStyleSheet(ESTILO_TARJETA_RESUMEN)

        tarjeta_layout = QVBoxLayout(tarjeta_frame)
        tarjeta_layout.setContentsMargins(25, 20, 25, 10)
        tarjeta_layout.setSpacing(10)

        top_tarjeta_layout = QHBoxLayout()

        lbl_titulo = QLabel(f"Pregunta {numero_mostrar}: {titulo}")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)
        top_tarjeta_layout.addWidget(lbl_titulo)
        top_tarjeta_layout.addStretch()
        tarjeta_layout.addLayout(top_tarjeta_layout)

        lbl_pregunta = QLabel(texto)
        lbl_pregunta.setFont(QFont("Arial", 11))
        lbl_pregunta.setWordWrap(True)
        lbl_pregunta.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_pregunta.setAlignment(Qt.AlignJustify)
        tarjeta_layout.addWidget(lbl_pregunta)

        boton_layout = QHBoxLayout()
        boton_layout.addStretch()

        boton_editar = QPushButton()
        boton_editar.setFixedSize(45, 45)
        boton_editar.setIcon(QIcon("assets/editar.png"))
        boton_editar.setIconSize(QSize(25, 25))
        boton_editar.setCursor(Qt.PointingHandCursor)
        boton_editar.setStyleSheet(ESTILO_BOTON_TARJETA)
        boton_editar.setToolTip(f"Editar pregunta {numero_mostrar}")
        self.grupo_botones_editar.addButton(boton_editar, int(id_pregunta))
        boton_layout.addWidget(boton_editar)

        tarjeta_layout.addLayout(boton_layout)
        return tarjeta_frame

    def cargar_preguntas(self):
        for boton in self.grupo_botones_editar.buttons():
            self.grupo_botones_editar.removeButton(boton)

        while self.scroll_content_layout.count():
            item = self.scroll_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self._preguntas_data = obtener_preguntas_como_diccionario()

        claves_ordenadas = sorted(
            self._preguntas_data.keys(),
            key=lambda clave: int(clave) if str(clave).isdigit() else 9999
        )

        for clave in claves_ordenadas:
            datos = self._preguntas_data.get(clave, {})
            if not str(clave).isdigit():
                continue
            numero = int(clave)
            titulo = datos.get("titulo", f"Pregunta {numero}")
            texto = datos.get("texto", "")
            tarjeta = self.crear_tarjeta_pregunta(numero, numero, titulo, texto)
            self.scroll_content_layout.addWidget(tarjeta)
