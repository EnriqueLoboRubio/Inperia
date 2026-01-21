# gui/pagina_bienvenida.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

class PantallaBienvenidaProfesional(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        principal_layout = QVBoxLayout(self)             

        principal_layout.addStretch(1)
        
        titulo = QLabel("Bienvenido, Nom Ape")
        titulo.setFont(QFont("Arial", 18))
        titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(titulo)   

        principal_layout.addSpacing(50)     
        
        texto_entrevistas = QLabel("Se han completado _ entrevistas")
        texto_entrevistas.setFont(QFont("Arial", 22))
        texto_entrevistas.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(texto_entrevistas)

        principal_layout.addStretch(1)