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

    # Método para obtener interno y actualizar vista
    def set_interno(self, interno):
        if interno:
            self.titulo.setText(f"Bienvenido {interno.nombre}")
        else:
            print("ERROR")

    def actualizar_interfaz(self, tiene_pendiente):
        """
        Cambia los texto dependiendo de si hay entrevista pendiente o no
        """
        if tiene_pendiente:
            self.contenido.setText("Tiene una entrevista pendiente")
            self.boton_iniciar.setText("Iniciar entrevista")
        else:
            self.contenido.setText("No tiene solicitudes pendientes")
            self.boton_iniciar.setText("Nueva solicitud")
