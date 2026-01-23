from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSlider, QHBoxLayout, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
import os

class VentanaDetallePregunta(QDialog):
    def __init__(self, datos_pregunta, numero, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalle Pregunta {numero}")
        self.setFixedSize(500, 600) # Tamaño fijo para que se vea ordenado
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        # --- 1. Título y Nivel ---
        lbl_titulo = QLabel(datos_pregunta.get("titulo", "Pregunta"))
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(lbl_titulo)

        lbl_nivel = QLabel(f"Nivel Asignado: {datos_pregunta.get('nivel', '0')}")
        lbl_nivel.setStyleSheet("color: gray; font-size: 14px;")
        layout.addWidget(lbl_nivel)

        # --- 2. Texto de la Respuesta (Transcripción) ---
        layout.addWidget(QLabel("Transcripción:"))
        txt_respuesta = QTextEdit()
        txt_respuesta.setReadOnly(True)
        txt_respuesta.setText(datos_pregunta.get("respuesta_texto", "Sin transcripción disponible."))
        layout.addWidget(txt_respuesta)

        # --- 3. Análisis de la IA ---
        layout.addWidget(QLabel("Análisis:"))
        txt_analisis = QTextEdit()
        txt_analisis.setReadOnly(True)
        txt_analisis.setText(datos_pregunta.get("analisis", "Pendiente de análisis."))
        txt_analisis.setStyleSheet("background-color: #f0f8ff;")
        layout.addWidget(txt_analisis)

        # --- 4. Reproductor de Audio ---
        player_layout = QHBoxLayout()
        
        self.player = QMediaPlayer()
        ruta_audio = datos_pregunta.get("ruta_audio", "") # Asegúrate de guardar la ruta en tu JSON
        
        btn_play = QPushButton("▶ Reproducir")
        btn_play.clicked.connect(lambda: self.reproducir_audio(ruta_audio))
        
        player_layout.addWidget(btn_play)
        layout.addLayout(player_layout)

        # Botón Cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)

    def reproducir_audio(self, ruta):
        if ruta and os.path.exists(ruta):
            url = QUrl.fromLocalFile(ruta)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
        else:
            print("Audio no encontrado")