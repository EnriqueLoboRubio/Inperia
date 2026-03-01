from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from db.pregunta_db import obtener_preguntas_como_diccionario, insertar_o_actualizar_pregunta
from gui.estilos import *


class VentanaDetallePreguntaEditProfesional(QDialog):
    def __init__(self, numero_pregunta, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.numero_pregunta = int(numero_pregunta)
        self._cierre_confirmado = False
        self._datos_iniciales = obtener_preguntas_como_diccionario().get(str(self.numero_pregunta), {})
        self._titulo_inicial = self._datos_iniciales.get("titulo", f"Pregunta {self.numero_pregunta}")
        self._texto_inicial = self._datos_iniciales.get("texto", "")

        self.setWindowTitle(f"Detalle Pregunta {self.numero_pregunta}")
        self.setFixedSize(1000, 650)

        layout_contenedor = QVBoxLayout(self)
        layout_contenedor.setContentsMargins(0, 0, 0, 0)

        self.frame_fondo = QFrame()
        self.frame_fondo.setObjectName("FondoDetalle")
        self.frame_fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        layout_contenedor.addWidget(self.frame_fondo)

        principal_layout = QVBoxLayout(self.frame_fondo)
        principal_layout.setSpacing(20)
        principal_layout.setContentsMargins(10, 10, 10, 10)

        top_layout = QHBoxLayout()
        lbl_titulo = QLabel(f"Pregunta {self.numero_pregunta}")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(lbl_titulo)
        top_layout.addStretch()
        principal_layout.addLayout(top_layout)

        lbl_titulo_edit = QLabel("<b>Título (Editable):</b>")
        lbl_titulo_edit.setFont(QFont("Arial", 11))
        principal_layout.addWidget(lbl_titulo_edit)

        self.txt_titulo = QTextEdit()
        self.txt_titulo.setReadOnly(False)
        self.txt_titulo.setStyleSheet(ESTILO_INPUT)
        self.txt_titulo.setText(self._titulo_inicial)
        self.txt_titulo.setFixedHeight(80)
        principal_layout.addWidget(self.txt_titulo)

        lbl_pregunta_edit = QLabel("<b>Pregunta (Editable):</b>")
        lbl_pregunta_edit.setFont(QFont("Arial", 11))
        principal_layout.addWidget(lbl_pregunta_edit)

        self.txt_pregunta = QTextEdit()
        self.txt_pregunta.setReadOnly(False)
        self.txt_pregunta.setStyleSheet(ESTILO_INPUT)
        self.txt_pregunta.setText(self._texto_inicial)
        self.txt_pregunta.setMinimumHeight(220)
        principal_layout.addWidget(self.txt_pregunta)

        boton_layout = QHBoxLayout()
        boton_layout.setContentsMargins(0, 0, 0, 0)

        self.boton_cerrar = QPushButton("Cerrar")
        self.boton_cerrar.clicked.connect(self.cerrar_ventana)
        self.boton_cerrar.setFont(QFont("Arial", 11))
        self.boton_cerrar.setFixedSize(110, 40)
        self.boton_cerrar.setToolTip("Cerrar ventana")
        self.boton_cerrar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_cerrar.setCursor(Qt.PointingHandCursor)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.setFont(QFont("Arial", 11))
        self.boton_guardar.setFixedSize(110, 40)
        self.boton_guardar.setToolTip("Guardar datos")
        self.boton_guardar.setStyleSheet(
            ESTILO_BOTON_SIG_ATR.replace("black", "#792A24").replace("rgba(71, 70, 70, 0.7)", "#C03930")
        )
        self.boton_guardar.setCursor(Qt.PointingHandCursor)
        self.boton_guardar.clicked.connect(self.guardar_datos)

        boton_layout.addWidget(self.boton_cerrar)
        boton_layout.addStretch()
        boton_layout.addWidget(self.boton_guardar)
        principal_layout.addLayout(boton_layout)

    def get_datos(self):
        return {
            "id_pregunta": self.numero_pregunta,
            "titulo": self.txt_titulo.toPlainText().strip(),
            "texto": self.txt_pregunta.toPlainText().strip(),
        }

    def guardar_datos(self):
        datos = self.get_datos()
        insertar_o_actualizar_pregunta(datos["id_pregunta"], datos["titulo"], datos["texto"])
        self.accept()

    def hay_cambios(self):
        return (
            self.txt_titulo.toPlainText().strip() != self._titulo_inicial.strip()
            or self.txt_pregunta.toPlainText().strip() != self._texto_inicial.strip()
        )

    def mostrar_confirmacion_cerrar(self):
        dialogo = QDialog(self)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        dialogo.setModal(True)

        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setObjectName("FondoDialogo")
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)

        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(10)

        layout_cabecera = QHBoxLayout()
        lbl_icono = QLabel()
        pixmap = QPixmap("assets/error.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_icono.setPixmap(pixmap)

        titulo = QLabel("Cerrar edición")
        titulo.setObjectName("TituloError")

        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()

        lbl_mensaje = QLabel("¿Está seguro de cerrar?\nPerderá los datos no guardados")
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(320)

        btn_si = QPushButton("Sí")
        btn_no = QPushButton("No")
        btn_si.setCursor(Qt.PointingHandCursor)
        btn_no.setCursor(Qt.PointingHandCursor)

        btn_si.setStyleSheet(
            """
            QPushButton {
                background-color: #792A24;
                color: white;
                border-radius: 10px;
                padding: 8px 25px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C03930; }
            """
        )
        btn_no.setStyleSheet(
            """
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 10px;
                padding: 8px 25px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #777; }
            """
        )

        btn_si.clicked.connect(dialogo.accept)
        btn_no.clicked.connect(dialogo.reject)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(btn_no)
        layout_botones.addWidget(btn_si)

        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(10)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(20)
        layout_interno.addLayout(layout_botones)

        layout_main.addWidget(fondo)
        return dialogo.exec_() == QDialog.Accepted

    def cerrar_ventana(self):
        if not self.hay_cambios():
            self._cierre_confirmado = True
            self.reject()
            return

        if self.mostrar_confirmacion_cerrar():
            self._cierre_confirmado = True
            self.reject()

    def closeEvent(self, event):
        if self.result() == QDialog.Accepted or self._cierre_confirmado or not self.hay_cambios():
            event.accept()
            return

        if self.mostrar_confirmacion_cerrar():
            event.accept()
        else:
            event.ignore()
