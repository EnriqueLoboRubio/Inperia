from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from gui.estilos import ESTILO_BOTON_NEGRO


class PantallaPerfil(QWidget):
    guardar_cambios = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        principal_layout = QVBoxLayout(self)
        principal_layout.setContentsMargins(60, 30, 60, 30)
        principal_layout.setSpacing(14)

        self.titulo = QLabel("Mi perfil")
        self.titulo.setFont(QFont("Arial", 22, QFont.Bold))
        self.titulo.setAlignment(Qt.AlignLeft)
        principal_layout.addWidget(self.titulo)

        marco = QFrame()
        marco.setStyleSheet(
            """
            QFrame {
                background-color: #F0F0F0;
                border: 2px solid #E0E0E0;
                border-radius: 14px;
            }
            """
        )
        layout_form = QVBoxLayout(marco)
        layout_form.setContentsMargins(30, 25, 30, 25)
        layout_form.setSpacing(12)

        self.lbl_email = QLabel("")
        self.lbl_email.setStyleSheet("color: #666; font-size: 11pt;")
        layout_form.addWidget(self.lbl_email)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        self.input_nombre.setStyleSheet(self._estilo_input())
        layout_form.addWidget(self._label_campo("Nombre"))
        layout_form.addWidget(self.input_nombre)

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Nueva contraseña (opcional)")
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setStyleSheet(self._estilo_input())
        layout_form.addWidget(self._label_campo("Nueva contraseña"))
        layout_form.addWidget(self.input_pass)

        self.input_pass_2 = QLineEdit()
        self.input_pass_2.setPlaceholderText("Repetir nueva contraseña")
        self.input_pass_2.setEchoMode(QLineEdit.Password)
        self.input_pass_2.setStyleSheet(self._estilo_input())
        layout_form.addWidget(self._label_campo("Confirmar contraseña"))
        layout_form.addWidget(self.input_pass_2)

        self.boton_guardar = QPushButton("Guardar cambios")
        self.boton_guardar.setStyleSheet(ESTILO_BOTON_NEGRO)
        self.boton_guardar.setCursor(Qt.PointingHandCursor)
        self.boton_guardar.clicked.connect(self.guardar_cambios.emit)
        layout_form.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        principal_layout.addWidget(marco)
        principal_layout.addStretch(1)

        self._nombre_original = ""

    def _label_campo(self, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet("color: #444; font-size: 11pt; font-weight: bold;")
        return lbl

    def _estilo_input(self):
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                padding: 9px 12px;
                font-size: 11pt;
                min-height: 24px;
            }
            QLineEdit:focus {
                border: 1px solid #8A8A8A;
            }
        """

    def set_datos_usuario(self, usuario):
        self._nombre_original = str(usuario.nombre or "")
        self.input_nombre.setText(self._nombre_original)
        self.input_pass.clear()
        self.input_pass_2.clear()
        self.lbl_email.setText(f"Correo: {usuario.email}")

    def get_datos_edicion(self):
        return {
            "nombre": self.input_nombre.text().strip(),
            "nombre_original": self._nombre_original,
            "password": self.input_pass.text(),
            "password_confirm": self.input_pass_2.text(),
        }
