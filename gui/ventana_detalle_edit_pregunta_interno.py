from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QMessageBox, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
import json, os

from gui.estilos import *

def cargar_datos_preguntas():
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_json = os.path.join(ruta_base, 'data', 'preguntas.json')

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos_preguntas = json.load(f)
            return datos_preguntas
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta_json}")
        return {"1": {"titulo": "Error", "texto": "No se pudo cargar el archivo 'preguntas.json'."}}
    except json.JSONDecodeError:
        print(f"Error: El archivo {ruta_json} tiene un formato JSON inválido.")
        return {"1": {"titulo": "Error", "texto": "Error al leer el archivo 'preguntas.json'."}}

class VentanaDetallePregunta(QDialog):
    def __init__(self, pregunta, numero, parent=None):
        super().__init__(parent)

        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        self.pregunta_actual = pregunta
        self.grabando = False # Estado inicial de grabación

        self.setWindowTitle(f"Detalle Pregunta {numero}")
        self.setFixedSize(1000, 650)        

        principal_layout = QVBoxLayout(self)
        principal_layout.setSpacing(20)
        principal_layout.setContentsMargins(10,10,10,10)

        # --- Título y Nivel ---
        top_layout = QHBoxLayout()
        datos = self.PREGUNTAS_DATA.get(str(numero), {})
        titulo_json = datos.get("titulo", f"Pregunta {numero}")
        
        titulo_texto = f"Pregunta {numero}: {titulo_json}"
        lbl_titulo = QLabel(titulo_texto)
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(lbl_titulo)

        top_layout.addStretch()              
        
        principal_layout.addLayout(top_layout)   

        # --- Texto de la Respuesta (Transcripción) ---           

        lbl_trancripcion = QLabel("<b>Transcripción (Editable):</b>")
        lbl_trancripcion.setFont(QFont("Arial",11))
        principal_layout.addWidget(lbl_trancripcion)

        self.txt_respuesta = QTextEdit()    
        self.txt_respuesta.setReadOnly(False) 
        self.txt_respuesta.setStyleSheet(ESTILO_INPUT)
        self.txt_respuesta.setText(pregunta.respuesta)
        self.txt_respuesta.setMinimumHeight(100)

        principal_layout.addWidget(self.txt_respuesta)

       # --- Reproductor de Audio y Grabadora ---
        self.player = QMediaPlayer()

        audio_layout = QVBoxLayout()
        audio_layout.setSpacing(10)

        # Estado visual
        self.lbl_estado_grabacion = QLabel("Listo para reproducir o grabar")
        self.lbl_estado_grabacion.setAlignment(Qt.AlignCenter)
        self.lbl_estado_grabacion.setStyleSheet("color: #6B7280; font-size: 12px;")

        # Barra de progreso
        self.slider_audio = QSlider(Qt.Horizontal)
        self.slider_audio.setRange(0, 0)
        self.slider_audio.setCursor(Qt.PointingHandCursor)
        self.slider_audio.setStyleSheet(ESTILO_SLIDER)

        # Tiempo
        time_layout = QHBoxLayout()
        self.lbl_tiempo_actual = QLabel("00:00")
        self.lbl_tiempo_total = QLabel("00:00")

        for lbl in (self.lbl_tiempo_actual, self.lbl_tiempo_total):
            lbl.setFont(QFont("Arial", 10))
            lbl.setStyleSheet("color: #374151;")

        time_layout.addWidget(self.lbl_tiempo_actual)
        time_layout.addStretch()
        time_layout.addWidget(self.lbl_estado_grabacion)
        time_layout.addStretch()
        time_layout.addWidget(self.lbl_tiempo_total)

        # --- CONTROLES DE AUDIO (PLAY y GRABAR) ---
        controles_layout = QHBoxLayout()
        controles_layout.setSpacing(20)
        controles_layout.setAlignment(Qt.AlignCenter)

        # Botón Play / Pause
        self.boton_play = QPushButton()
        self.boton_play.setIcon(QIcon("assets/play.png")) 
        self.boton_play.setIconSize(QSize(20, 20))
        self.boton_play.setFixedSize(50, 50)
        self.boton_play.setToolTip("Reproducir grabación")
        self.boton_play.setCursor(Qt.PointingHandCursor)
        self.boton_play.setStyleSheet(ESTILO_BOTON_PLAY)
        
        self.boton_play.clicked.connect(lambda: self.toggle_audio(pregunta.archivo_audio))

        # CAMBIO 2: Botón Grabar
        self.boton_grabar = QPushButton()
        self.boton_grabar.setIcon(QIcon("assets/micro.png"))
        self.boton_grabar.setIconSize(QSize(25, 25))
        self.boton_grabar.setFixedSize(50, 50)
        self.boton_grabar.setToolTip("Responder por voz")
        self.boton_grabar.setCursor(Qt.PointingHandCursor)
        self.boton_grabar.setStyleSheet(ESTILO_BOTON_GRABAR)
        self.boton_grabar.clicked.connect(self.toggle_grabacion)

        controles_layout.addWidget(self.boton_play)
        controles_layout.addWidget(self.boton_grabar)

        # Añadir al layout principal de audio
        audio_layout.addLayout(controles_layout)
        audio_layout.addWidget(self.slider_audio)
        audio_layout.addLayout(time_layout)
                
        #Señales del reproductor
        self.player.positionChanged.connect(self.actualizar_posicion)
        self.player.durationChanged.connect(self.actualizar_duracion)
        self.slider_audio.sliderMoved.connect(self.player.setPosition)
        self.player.stateChanged.connect(self.cambio_estado_reproductor)

        principal_layout.addLayout(audio_layout)

        # ------- Botones Inferiores --------
        boton_layout = QHBoxLayout()
        boton_layout.setContentsMargins(0, 0, 0, 0)

        # Botón Cerrar
        self.boton_cerrar = QPushButton("Cerrar")
        self.boton_cerrar.clicked.connect(self.cerrar_ventana) 
        self.boton_cerrar.setFont(QFont("Arial", 11))   
        self.boton_cerrar.setFixedSize(110,40)
        self.boton_cerrar.setToolTip("Cerrar ventana")
        self.boton_cerrar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_cerrar.setCursor(Qt.PointingHandCursor)

        # Botón Guardar
        self.boton_guardar = QPushButton("Guardar")       
        self.boton_guardar.setFont(QFont("Arial", 11))   
        self.boton_guardar.setFixedSize(110,40)
        self.boton_guardar.setToolTip("Guardar datos")
        self.boton_guardar.setStyleSheet(ESTILO_BOTON_SIG_ATR.replace("black", "#792A24").replace("rgba(71, 70, 70, 0.7)", "#C03930"))
        self.boton_guardar.setCursor(Qt.PointingHandCursor)

        boton_layout.addWidget(self.boton_cerrar)
        boton_layout.addStretch() 
        boton_layout.addWidget(self.boton_guardar)

        principal_layout.addLayout(boton_layout)

    # --- LÓGICA DE GRABACIÓN ---
    def toggle_grabacion(self):
        if not self.grabando:
            # INICIAR GRABACIÓN
            self.grabando = True
            
            # Visuales
            self.boton_grabar.setProperty("grabando", True)
            self.boton_grabar.style().unpolish(self.boton_grabar)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/pausa.png")) # Icono de stop
            self.boton_grabar.setIconSize((QSize(20, 20)))
            
            # Bloquear reproducción
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            self.boton_play.setEnabled(False) # No reproducir mientras grabas
            
            # Feedback
            self.lbl_estado_grabacion.setText("🔴 Grabando... (Hable ahora)")
            self.lbl_estado_grabacion.setStyleSheet("color: #D32F2F; font-weight: bold;")
            self.txt_respuesta.setPlaceholderText("Escuchando...")
            self.txt_respuesta.clear()        

        else:
            # DETENER GRABACIÓN
            self.grabando = False
            
            # Visuales
            self.boton_grabar.setProperty("grabando", False)
            self.boton_grabar.style().unpolish(self.boton_grabar)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/micro.png"))
            
            # Desbloquear reproducción
            self.boton_play.setEnabled(True)
            
            # Feedback
            self.lbl_estado_grabacion.setText("⏳ Procesando audio...")
            self.lbl_estado_grabacion.setStyleSheet("color: #F57C00; font-weight: bold;")
            
            # SIMULACIÓN DE TRANSCRIPCIÓN (Delay de 1.5 seg)
            QTimer.singleShot(1500, self.simular_transcripcion)

    def simular_transcripcion(self):
        # Esta función simula que la IA ha transcrito el audio
        texto_simulado = "Esta es una nueva respuesta transcrita automáticamente después de grabar el audio. El usuario puede editar esto si hay errores."
        
        self.txt_respuesta.setText(texto_simulado)
        self.lbl_estado_grabacion.setText("✅ Transcripción completada")
        self.lbl_estado_grabacion.setStyleSheet("color: #388E3C; font-weight: bold;")
        
        # IMPORTANTE: actualizar ruta del audio en self.pregunta_actual.archivo_audio para que al dar play suene el nuevo archivo.
        # self.pregunta_actual.archivo_audio = "ruta/del/nuevo/audio.wav"
        
        # Resetear player para nuevo archivo
        self.player.stop()
        self.player.setMedia(QMediaContent()) 

    # --- LÓGICA DE REPRODUCCIÓN ---
    def toggle_audio(self, ruta):
        # Si está grabando, no hacemos nada
        if self.grabando:
            return

        if not ruta or not os.path.exists(ruta):
            # Nota: En un caso real, si acabas de grabar, la ruta debería apuntar al temporal
            self.lbl_estado_grabacion.setText("⚠️ Archivo de audio no encontrado (Simulación)")
            # return # Comentado para permitir probar la UI sin archivo real

        if self.player.mediaStatus() == QMediaPlayer.NoMedia or self.player.mediaStatus() == QMediaPlayer.InvalidMedia:
             # Aquí cargamos el audio (el original o el nuevo grabado)
             if os.path.exists(ruta):
                url = QUrl.fromLocalFile(os.path.abspath(ruta))
                self.player.setMedia(QMediaContent(url))

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def cambio_estado_reproductor(self, estado):
        # Bloquear grabación si se está reproduciendo
        if estado == QMediaPlayer.PlayingState:
            self.boton_play.setIcon(QIcon("assets/pausa.png"))
            self.lbl_estado_grabacion.setText("Reproduciendo...")
            self.lbl_estado_grabacion.setStyleSheet("color: green;")
            self.boton_grabar.setEnabled(False) # No grabar mientras reproduce
            self.boton_grabar.setToolTip("Pausa el audio para grabar")
        else:
            self.boton_play.setIcon(QIcon("assets/play.png"))
            if not self.grabando:
                self.lbl_estado_grabacion.setText("Pausado / Listo")
                self.boton_grabar.setEnabled(True) # Permitir grabar de nuevo
                self.boton_grabar.setToolTip("Grabar nueva respuesta")

    def actualizar_posicion(self, posicion):
        self.slider_audio.setValue(posicion)
        self.lbl_tiempo_actual.setText(self.formatear_tiempo(posicion))

    def actualizar_duracion(self, duracion):
        self.slider_audio.setRange(0, duracion)
        self.lbl_tiempo_total.setText(self.formatear_tiempo(duracion))

    def formatear_tiempo(self, ms):
        if ms is None: ms = 0
        segundos = ms // 1000
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02}:{segundos:02}"
    
    def mostrar_confirmacion_cerrar(self):
            respuesta = QMessageBox.question(
                self, "Cerrar Respuesta",
                "¿Está seguro de cerrar?\nPerderá los datos no guardados",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            return respuesta == QMessageBox.Yes 

    def cerrar_ventana(self):
        if self.mostrar_confirmacion_cerrar() is True:
            self.close()
        else:
            return