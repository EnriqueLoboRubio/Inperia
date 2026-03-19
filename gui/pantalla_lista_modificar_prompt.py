from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QSizePolicy, QButtonGroup
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from db.prompt_db import obtener_prompts_como_diccionario
from gui.estilos import *


class PantallaListaModificarPrompt(QWidget):
    """Pantalla de listado de prompts para modificar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._prompts_data = {}
        self.grupo_botones_editar = QButtonGroup(self)
        self._iniciar_ui()
        self.cargar_prompts()

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

    def crear_tarjeta_prompt(self, id_prompt, numero_mostrar, titulo, texto, version=None):
        tarjeta_frame = QFrame()
        tarjeta_frame.setStyleSheet(ESTILO_TARJETA_RESUMEN)

        tarjeta_layout = QVBoxLayout(tarjeta_frame)
        tarjeta_layout.setContentsMargins(25, 20, 25, 10)
        tarjeta_layout.setSpacing(10)

        top_tarjeta_layout = QHBoxLayout()

        sufijo_version = f" - Versión {int(version)}" if version is not None else ""
        lbl_titulo = QLabel(f"Prompt {numero_mostrar}: {titulo}{sufijo_version}")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)
        top_tarjeta_layout.addWidget(lbl_titulo)
        top_tarjeta_layout.addStretch()
        tarjeta_layout.addLayout(top_tarjeta_layout)

        texto_preview = self._resumir_texto_tarjeta(texto, max_chars=180)
        lbl_prompt = QLabel(texto_preview)
        lbl_prompt.setFont(QFont("Arial", 11))
        lbl_prompt.setWordWrap(True)
        lbl_prompt.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_prompt.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        lbl_prompt.setToolTip(texto)
        tarjeta_layout.addWidget(lbl_prompt)

        boton_layout = QHBoxLayout()
        boton_layout.addStretch()

        boton_editar = QPushButton()
        boton_editar.setFixedSize(45, 45)
        boton_editar.setIcon(QIcon("assets/editar.png"))
        boton_editar.setIconSize(QSize(25, 25))
        boton_editar.setCursor(Qt.PointingHandCursor)
        boton_editar.setStyleSheet(ESTILO_BOTON_TARJETA)
        boton_editar.setToolTip(f"Editar prompt {numero_mostrar}")
        self.grupo_botones_editar.addButton(boton_editar, int(id_prompt))
        boton_layout.addWidget(boton_editar)

        tarjeta_layout.addLayout(boton_layout)
        return tarjeta_frame

    @staticmethod
    def _resumir_texto_tarjeta(texto, max_chars=180):
        texto_limpio = " ".join(str(texto or "").split())
        if len(texto_limpio) <= max_chars:
            return texto_limpio
        return texto_limpio[:max_chars].rstrip() + "..."

    def cargar_prompts(self):
        for boton in self.grupo_botones_editar.buttons():
            self.grupo_botones_editar.removeButton(boton)

        while self.scroll_content_layout.count():
            item = self.scroll_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self._prompts_data = obtener_prompts_como_diccionario(solo_activos=True)

        claves_ordenadas = sorted(
            self._prompts_data.keys(),
            key=lambda clave: int(clave) if str(clave).isdigit() else 9999
        )

        for clave in claves_ordenadas:
            if not str(clave).isdigit():
                continue
            numero = int(clave)
            datos = self._prompts_data.get(clave, {})
            titulo = datos.get("titulo", f"Prompt {numero}")
            texto = datos.get("texto", "")
            version = datos.get("version")
            tarjeta = self.crear_tarjeta_prompt(numero, numero, titulo, texto, version=version)
            self.scroll_content_layout.addWidget(tarjeta)
