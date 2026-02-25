from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from gui.estilos import *

class PantallaBienvenidaProfesional(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        principal_layout = QVBoxLayout(self)             

        principal_layout.addStretch(1)
        
        self.titulo = QLabel("Bienvenido ...")
        self.titulo.setFont(QFont("Arial", 18))
        self.titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(self.titulo)   

        principal_layout.addSpacing(50)     
        
        self.contenido = QLabel("Tiene entrevistas pendientes")
        self.contenido.setFont(QFont("Arial", 22))
        self.contenido.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(self.contenido)

        principal_layout.addStretch(1)

        # Botones
        layout_botones = QHBoxLayout()

        self.boton_solicitudes_pendientes = QPushButton("Solicitudes pendientes")
        self.boton_solicitudes_pendientes.setToolTip("Solicitudes pendientes")
        self.boton_solicitudes_pendientes.setStyleSheet(ESTILO_BOTON_NEGRO)
        layout_botones.addWidget(self.boton_solicitudes_pendientes, alignment=Qt.AlignCenter)

        self.boton_historial_solicitudes = QPushButton("Historial de solicitudes")
        self.boton_historial_solicitudes.setToolTip("Historial de solicitudes")
        self.boton_historial_solicitudes.setStyleSheet(ESTILO_BOTON_NEGRO)
        layout_botones.addWidget(self.boton_historial_solicitudes, alignment=Qt.AlignCenter)

        self.boton_nueva_solicitud = QPushButton("Nueva solicitud")
        self.boton_nueva_solicitud.setToolTip("Nueva solicitud")
        self.boton_nueva_solicitud.setStyleSheet(ESTILO_BOTON_NEGRO)
        layout_botones.addWidget(self.boton_nueva_solicitud, alignment=Qt.AlignCenter)

        principal_layout.addLayout(layout_botones)

        principal_layout.addStretch(2)

    def set_profesional(self, profesional):
        if profesional:
            self.titulo.setText(f"Bienvenido, {profesional.nombre}")
        else:
            print("ERROR")

    def actualizar_interfaz(self, num_solicitudes_pendientes, num_solicitudes_completadas):
        if num_solicitudes_pendientes == 0 and num_solicitudes_completadas == 0:
            self.contenido.setText("No tiene solicitudes pendientes ni completadas")
        elif num_solicitudes_pendientes == 0:
            self.contenido.setText(f"Tiene {num_solicitudes_completadas} solicitudes completadas")
        elif num_solicitudes_completadas == 0:
            self.contenido.setText(f"Tiene {num_solicitudes_pendientes} solicitudes pendientes")
        else:
            self.contenido.setText(f"Tiene {num_solicitudes_pendientes} solicitudes pendientes\ny {num_solicitudes_completadas} solicitudes completadas")
        
        if num_solicitudes_pendientes == 0:
            self.boton_solicitudes_pendientes.setVisible(False)
        if num_solicitudes_completadas == 0:
            self.boton_solicitudes_completadas.setVisible(False)