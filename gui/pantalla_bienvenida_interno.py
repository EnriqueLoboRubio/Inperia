from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

class PantallaBienvenidaInterno(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        principal_layout = QVBoxLayout(self)             

        principal_layout.addStretch(1)
        
        #titulo_texto = f"Bienvenido,  {nombre}"

        titulo = QLabel("Bienvenido Nombre")
        titulo.setFont(QFont("Arial", 18))
        titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(titulo)

        principal_layout.addSpacing(50)


        # Si tiene una entrevista pendiente

        contenido = QLabel("Tiene una entrevista pendiente")
        contenido.setFont(QFont("Arial", 22))
        contenido.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(contenido)
        
        principal_layout.addStretch(1)

        # Botón iniciar nueva entrevista       
        self.boton_iniciar = QPushButton("Iniciar nueva entrevista")
        self.boton_iniciar.setFont(QFont("Arial", 14))        
        self.boton_iniciar.setStyleSheet("""                                   
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: center;
                background-color: black; 
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: rgba(71, 70, 70, 0.7); 
            }
        """)

        principal_layout.addWidget(self.boton_iniciar, alignment=Qt.AlignCenter)
        principal_layout.addStretch(2)