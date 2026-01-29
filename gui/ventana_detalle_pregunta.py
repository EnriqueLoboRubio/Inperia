from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
import os

class VentanaDetallePregunta(QDialog):
    def __init__(self, datos_pregunta, numero, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalle Pregunta {numero}")
        self.setFixedSize(600, 700) 
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        # --- 1. Título y Nivel ---
        titulo_texto = datos_pregunta.get("titulo", f"Pregunta {numero}")
        lbl_titulo = QLabel(titulo_texto)
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_titulo.setWordWrap(True)
        layout.addWidget(lbl_titulo)

        nivel_texto = datos_pregunta.get("nivel", "0")
        lbl_nivel = QLabel(f"Nivel Asignado: {nivel_texto}")
        lbl_nivel.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")
        layout.addWidget(lbl_nivel)

        # --- 2. Texto de la Respuesta (Transcripción) ---
        layout.addWidget(QLabel("<b>Transcripción:</b>"))
        self.txt_respuesta = QTextEdit()
        self.txt_respuesta.setReadOnly(True)
        # Busca "respuesta" o "respuesta_texto" en el JSON
        contenido_respuesta = datos_pregunta.get("respuesta", datos_pregunta.get("respuesta_texto", "Sin transcripción."))
        self.txt_respuesta.setText(contenido_respuesta)
        layout.addWidget(self.txt_respuesta)

        # --- 3. Análisis de la IA ---
        layout.addWidget(QLabel("<b>Análisis de IA:</b>"))
        self.txt_analisis = QTextEdit()
        self.txt_analisis.setReadOnly(True)
        contenido_analisis = datos_pregunta.get("analisis", "Pendiente de análisis.")
        self.txt_analisis.setText(contenido_analisis)
        self.txt_analisis.setStyleSheet("background-color: #f0f8ff; border: 1px solid #dcdcdc;")
        layout.addWidget(self.txt_analisis)

        # --- 4. Reproductor de Audio ---
        player_layout = QHBoxLayout()
        self.player = QMediaPlayer()
        
        # Obtenemos la ruta del audio del JSON
        ruta_audio = datos_pregunta.get("ruta_audio", "")
        self.lbl_estado_audio = QLabel("Listo para reproducir")
        
        btn_play = QPushButton("▶ Reproducir Audio")
        btn_play.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        
        # Usamos una variable local para no perder la referencia en la lambda
        btn_play.clicked.connect(lambda: self.reproducir_audio(ruta_audio))
        
        player_layout.addWidget(btn_play)
        player_layout.addWidget(self.lbl_estado_audio)
        layout.addLayout(player_layout)

        # Botón Cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        btn_cerrar.setStyleSheet("margin-top: 10px;")
        layout.addWidget(btn_cerrar)

    def reproducir_audio(self, ruta):
        if ruta and os.path.exists(ruta):
            try:
                # Url local absoluta
                full_path = os.path.abspath(ruta)
                url = QUrl.fromLocalFile(full_path)
                content = QMediaContent(url)
                self.player.setMedia(content)
                self.player.play()
                self.lbl_estado_audio.setText("Reproduciendo...")
                self.lbl_estado_audio.setStyleSheet("color: green;")
            except Exception as e:
                 self.lbl_estado_audio.setText(f"Error: {str(e)}")
        else:
            self.lbl_estado_audio.setText("Archivo de audio no encontrado")
            self.lbl_estado_audio.setStyleSheet("color: red;")