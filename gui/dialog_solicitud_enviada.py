from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class DialogSolicitudEnviada(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Solicitud Enviada")
        self.setModal(True)
        self.setFixedSize(520, 420)
        self.init_ui(datos)

    def init_ui(self, datos):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        # --- CABECERA ---
        cabecera = QHBoxLayout()

        icono = QLabel()
        icono.setPixmap(QPixmap("assets/info.png").scaled(48, 48, Qt.KeepAspectRatio))
        cabecera.addWidget(icono, alignment=Qt.AlignTop)

        textos = QVBoxLayout()

        titulo = QLabel("Solicitud Enviada Exitosamente")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))

        textos.addWidget(titulo)
        cabecera.addLayout(textos)
        cabecera.addStretch()

        layout_principal.addLayout(cabecera)
        layout_principal.addSpacing(15)

        # --- CUERPO ---
        cuerpo = QVBoxLayout()

        def fila(label, valor):
            fila = QHBoxLayout()
            l1 = QLabel(f"{label}:")
            l1.setFont(QFont("Arial", 10, QFont.Bold))
            l2 = QLabel(valor)
            fila.addWidget(l1)
            fila.addWidget(l2)
            fila.addStretch()
            cuerpo.addLayout(fila)

        fila("Tipo de Permiso", datos["tipo"])
        fila("Urgencia", datos["urgencia"])
        fila("Fecha Inicio", datos["fecha_inicio"])
        fila("Fecha Fin", datos["fecha_fin"])
        fila("Destino", datos["destino"])
        fila("Contacto Emergencia", datos["contacto"])
        fila("Teléfono", datos["telefono"])

        layout_principal.addLayout(cuerpo)
        layout_principal.addStretch()

        # BOTONES
        botones = QHBoxLayout()
        botones.addStretch()

        boton_no = QPushButton("No")
        boton_no.setFixedSize(90, 35)
        boton_no.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        boton_no.clicked.connect(self.reject)

        boton_si = QPushButton("Sí, enviar")
        boton_si.setFixedSize(120, 35)
        boton_si.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        boton_si.clicked.connect(self.accept)

        botones.addWidget(boton_no)
        botones.addWidget(boton_si)
        
        layout_principal.addLayout(botones)
