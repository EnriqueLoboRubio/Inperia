from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PantallaSolicitudInterno(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        principal_layout = QVBoxLayout(self)             

        principal_layout.addStretch(1)           

        self.titulo = QLabel("PANTALLA SOLICITUD")
        self.titulo.setFont(QFont("Arial", 18))
        self.titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(self.titulo)

        principal_layout.addSpacing(50)        