from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal

from gui.estilos import *


class PantallaPerfil(QWidget):
    guardar_cambios = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._nombre_original = ""
        self._iniciar_ui()

    def _iniciar_ui(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setContentsMargins(20, 20, 20, 20)
        principal_layout.setSpacing(20)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")

        marco = QFrame()
        marco.setObjectName("apartado")
        marco.setStyleSheet(ESTILO_APARTADO_FRAME)
        perfil_layout = QVBoxLayout(marco)
        perfil_layout.setContentsMargins(30, 24, 30, 24)
        perfil_layout.setSpacing(16)

        self.titulo = QLabel("Mi perfil")
        self.titulo.setStyleSheet(ESTILO_TITULO_PASO_ENCA)
        perfil_layout.addWidget(self.titulo)

        subtitulo = QLabel("Actualiza tus datos personales y de acceso")
        subtitulo.setStyleSheet(ESTILO_SUBTITULO_SOLICITUD)
        perfil_layout.addWidget(subtitulo)

        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("background-color: #E0E0E0; max-height: 1px;")
        perfil_layout.addWidget(separador)

        cabecera_form = QHBoxLayout()
        cabecera_form.setSpacing(20)

        bloque_email = QVBoxLayout()
        bloque_email.setSpacing(5)

        lbl_email_titulo = QLabel("Correo de la cuenta")
        lbl_email_titulo.setStyleSheet(ESTILO_TITULO_APARTADO)
        bloque_email.addWidget(lbl_email_titulo)

        self.lbl_email = QLabel("")
        self.lbl_email.setStyleSheet(ESTILO_TEXTO)
        self.lbl_email.setWordWrap(True)
        bloque_email.addWidget(self.lbl_email)

        cabecera_form.addLayout(bloque_email)
        cabecera_form.addStretch()
        perfil_layout.addLayout(cabecera_form)        

        perfil_layout.addWidget(self._label_campo("Nombre completo"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        self.input_nombre.setStyleSheet(ESTILO_INPUT)
        perfil_layout.addWidget(self.input_nombre)

        perfil_layout.addWidget(self._label_campo("Nueva contraseña"))
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Nueva contraseña (opcional)")
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setStyleSheet(ESTILO_INPUT)
        perfil_layout.addWidget(self.input_pass)

        perfil_layout.addWidget(self._label_campo("Confirmar nueva contraseña"))
        self.input_pass_2 = QLineEdit()
        self.input_pass_2.setPlaceholderText("Repetir nueva contraseña")
        self.input_pass_2.setEchoMode(QLineEdit.Password)
        self.input_pass_2.setStyleSheet(ESTILO_INPUT)
        perfil_layout.addWidget(self.input_pass_2)

        ayuda_password = QLabel("Si dejas vacíos los campos de contraseña, no se modificará.")
        ayuda_password.setStyleSheet(ESTILO_TEXTO)
        ayuda_password.setWordWrap(True)
        perfil_layout.addWidget(ayuda_password)

        self.boton_guardar = QPushButton("Guardar cambios")
        self.boton_guardar.setFixedSize(200, 46)
        self.boton_guardar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_guardar.setCursor(Qt.PointingHandCursor)
        self.boton_guardar.clicked.connect(self.guardar_cambios.emit)
        perfil_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        principal_layout.addWidget(marco)
        principal_layout.addStretch(1)

    def _label_campo(self, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet(ESTILO_TITULO_APARTADO)
        return lbl

    def set_datos_usuario(self, usuario):
        self._nombre_original = str(usuario.nombre or "")
        self.input_nombre.setText(self._nombre_original)
        self.input_pass.clear()
        self.input_pass_2.clear()
        self.lbl_email.setText(f"{usuario.email}")

    def get_datos_edicion(self):
        return {
            "nombre": self.input_nombre.text().strip(),
            "nombre_original": self._nombre_original,
            "password": self.input_pass.text(),
            "password_confirm": self.input_pass_2.text(),
        }
