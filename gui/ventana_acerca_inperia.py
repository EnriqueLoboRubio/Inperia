from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton


class VentanaAcercaInperia(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(540, 500)
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_main = QVBoxLayout(self)
        layout_main.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 14px;
            }
            QLabel {
                background: transparent;
                border: none;
                color: #1A1A1A;
            }
            """
        )
        layout_main.addWidget(fondo)

        layout = QVBoxLayout(fondo)
        layout.setContentsMargins(20, 14, 20, 18)
        layout.setSpacing(8)

        fila_top = QHBoxLayout()
        fila_top.addStretch()
        boton_cerrar = QPushButton("✕")
        boton_cerrar.setCursor(Qt.PointingHandCursor)
        boton_cerrar.setFixedSize(24, 24)
        boton_cerrar.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                color: #666666;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F1F1F1;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                color: #111111;
            }
            """
        )
        boton_cerrar.clicked.connect(self.accept)
        fila_top.addWidget(boton_cerrar)
        layout.addLayout(fila_top)

        logo = QLabel()
        pixmap = QPixmap("assets/inperiaNegro.png").scaled(88, 88, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        titulo = QLabel("INPERIA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20pt; font-weight: 700; color: #111111;")
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Inteligencia Penitenciaria para la evaluación de Riesgo mediante Inteligencia Artificial"
        )
        descripcion.setWordWrap(True)
        descripcion.setAlignment(Qt.AlignCenter)
        descripcion.setStyleSheet("font-size: 10.5pt; color: #2C2C2C;")
        layout.addWidget(descripcion)

        layout.addSpacing(6)
        version = QLabel("Versión 1")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("font-size: 10pt; font-weight: 600;")
        layout.addWidget(version)

        autor = QLabel("Autor\nEnrique Lobo Rubio")
        autor.setAlignment(Qt.AlignCenter)
        autor.setStyleSheet("font-size: 10pt;")
        layout.addWidget(autor)

        tecnologias = QLabel("Tecnologías\nPython · PyQt5 · SQLite · LLM")
        tecnologias.setAlignment(Qt.AlignCenter)
        tecnologias.setStyleSheet("font-size: 10pt;")
        layout.addWidget(tecnologias)

        licencias = QLabel(
            'Licencias<br>Iconos: <a href="https://iconos8.es/">Icons8</a><br>Modelo IA: Qwen 2.5 (Ollama)'
        )
        licencias.setAlignment(Qt.AlignCenter)
        licencias.setTextFormat(Qt.RichText)
        licencias.setOpenExternalLinks(True)
        licencias.setStyleSheet("font-size: 10pt;")
        layout.addWidget(licencias)

        pie = QLabel(
            "Trabajo de Fin de Grado – Ingeniería Informática\n"
            "Universidad de Huelva\n"
            "© 2026"
        )
        pie.setAlignment(Qt.AlignCenter)
        pie.setStyleSheet("font-size: 9.5pt; color: #3A3A3A;")
        layout.addWidget(pie)
