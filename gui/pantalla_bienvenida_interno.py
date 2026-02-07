from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from gui.estilos import *

class PantallaBienvenidaInterno(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        principal_layout = QVBoxLayout(self)             

        principal_layout.addStretch(1)           

        self.titulo = QLabel("Bienvenido ...")
        self.titulo.setFont(QFont("Arial", 18))
        self.titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(self.titulo)

        principal_layout.addSpacing(50)


        # Si tiene una entrevista pendiente
        self.contenido = QLabel("Tiene una entrevista pendiente")
        self.contenido.setFont(QFont("Arial", 22))
        self.contenido.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(self.contenido)
        
        principal_layout.addStretch(1)

        # Botón iniciar nueva entrevista       
        self.boton_iniciar = QPushButton("Iniciar nueva entrevista")             
        self.boton_iniciar.setStyleSheet(ESTILO_BOTON_NEGRO)

        principal_layout.addWidget(self.boton_iniciar, alignment=Qt.AlignCenter)
        principal_layout.addStretch(2)

    # Método para obtener interno y actualizar vista
    def set_interno(self, interno):
        if interno:
            self.titulo.setText(f"Bienvenido {interno.nombre}")
        else:
            print("ERROR")

    def actualizar_interfaz(self, tiene_pendiente_iniciada, tiene_entrevista):
        """
        Cambia los texto dependiendo de si hay entrevista pendiente o no
        """

        if not tiene_pendiente_iniciada:
            self.contenido.setText("No tiene solicitudes pendientes o iniciadas")
            self.boton_iniciar.setText("Nueva solicitud")
            self.boton_iniciar.setToolTip("Crear una nueva solicitud")
        elif not tiene_entrevista:    
            self.contenido.setText("Tiene una entrevista pendiente")
            self.boton_iniciar.setText("Iniciar entrevista")
            self.boton_iniciar.setToolTip("Realizar entrevista completa")
        else:                    
            self.contenido.setText("No tiene nada pendiente")
            self.boton_iniciar.setText("Ver Progreso")
            self.boton_iniciar.setToolTip("Ver progreso de la última solicitud")
