from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap

from gui.estilos import *

class PantallaProgresoInterno(QWidget):

    # Señales para botones
    ver_entrevista_signal = pyqtSignal()
    descargar_solicitud_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.solicitud = None
        self.iniciar_ui()

        def iniciar_ui():

            # ---------- GRID PRINCIPAL ----------
            grid = QGridLayout()
            grid.setContentsMargins(0,0,0,0)
            grid.setHorizontalSpacing(15)
            grid.setVerticalSpacing(15)

            # definición de proporciones

            grid.setColumnStretch(0, 65)
            grid.setColumnStretch(1, 35)

            grid.setRowStretch(0, 75)
            grid.setRowStretch(1, 25)

            # ========== Resumen solicitud ==========

            resumen_frame = QFrame()
            resumen_frame.setObjectName("apartado")
            resumen_frame.setStyleSheet(ESTILO_APARTADO_FRAME)

            resumen_layout = QVBoxLayout(resumen_frame)

            # --- Encabezado ---
            encabezado_resumen = QHBoxLayout()
            
            # Icono documento
            doc_icon_label = QLabel(self)
            icono = QPixmap("assets/documento.png").scaled(40, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
            doc_icon_label.setPixmap(icono)
            doc_icon_label.setFixedSize(50,50)
            doc_icon_label.setStyleSheet("background: transparent; border: none;")

            encabezado_resumen.addWidget(doc_icon_label)

            titulo_layout = QVBoxLayout()
            titulo_layout.setSpacing(3)

            # Titulo
            self.titulo_resumen = QLabel("Solicitud #2025-0100") # Cargar de objeto id de solicitud
            self.titulo_resumen.setStyleSheet(ESTILO_TITULO_PASO_ENCA)

            # Subtitulo
            self.subtitulo_resumen = QLabel("Solicitud de permiso de salida familiar") # Cargar de objeto: motivo
            self.subtitulo_resumen.setStyleSheet(ESTILO_SUBTITULO_PASO_ENCA)

            titulo_layout.addWidget(self.titulo_resumen)
            titulo_layout.addWidget(self.subtitulo_resumen)  

            encabezado_resumen.addLayout(titulo_layout)                
            
            estado_layout = QHBoxLayout()

            # Icono estado
            estado_icon_label = QLabel(self)
            icono = QPixmap("assets/importante.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            estado_icon_label.setPixmap(icono)
            estado_icon_label.setFixedSize(45,45)
            estado_icon_label.setStyleSheet("background: transparent; border: none;")

            estado_layout.addWidget(estado_icon_label)

            # Estado
            self.estado_label = QLabel("En revisión") # Cargar de objeto: estado, cambiar texto y color
            self.estado_label.setAligment(Qt.AlignCenter) 
            self.estado_label.setFixedSize(100, 30)
            self.estado_label.setStyleSheet(ESTILO_NIVEL)

            estado_layout.addWidget(self.estado_label)

            encabezado_resumen.addLayout(estado_layout)

            resumen_layout.addLayout(encabezado_resumen)

            # Linea separadora
            linea_sep = QFrame()
            linea_sep.setFrameShape(QFrame.HLine)
            linea_sep.setStyleSheet("background-color: #E0E0E0; max-height: 1px;")

            resumen_layout.addWidget(linea_sep)

            # --- Scroll resumen ---
            scroll_resumen = QScrollArea()
            




            grid.addWidget(resumen_frame, 0, 0)

            # ========== Documentacion y acciones ==========
            acciones_layout = QVBoxLayout()

            grid.addLayout(acciones_layout, 1, 0)

            # ========== Progreso solicitud ==========
            progreso_layout = QVBoxLayout()


            grid.addLayout(progreso_layout, 0 ,1, 2, 1)


            
          
       