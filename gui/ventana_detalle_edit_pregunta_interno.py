from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QSlider, QFrame
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor
import json, os
from gui.mensajes import Mensajes
from gui.estilos import *
from utils.transcripcionVosk import HiloTranscripcion
from datetime import datetime

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

class VentanaDetallePreguntaEdit(QDialog):
    def __init__(self, pregunta, numero, id_entrevista ,parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)  #Quitar menu de pantalla, no se puede mover

        self.pregunta_actual = pregunta        
        self.id_entrevista = id_entrevista
        self.num_pregunta = numero

        self.PREGUNTAS_DATA = cargar_datos_preguntas()        
        self.grabando = False # Estado inicial de grabación
        self.tiene_nuevo_audio = False

        self.hilo_grabacion = None
         
        # Gestion ruta de audios
        ruta_base = os.path.dirname(os.path.dirname(__file__))
        self.ruta_modelo_vosk = os.path.join(ruta_base, "utils", "vosk-es", "small")  

        self.carpeta_audios = os.path.join(ruta_base, "data", "grabaciones")
        if not os.path.exists(self.carpeta_audios):
            os.makedirs(self.carpeta_audios)

        #Ruta original
        self.ruta_audio_original = pregunta.archivo_audio

        if self.ruta_audio_original is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_audio = f"audio_{timestamp}.wav"
            self.carpeta_audios = os.path.join(ruta_base, "data", "grabaciones")
            self.ruta_audio_original = os.path.join(self.carpeta_audios, nombre_audio)

        # Ruta temporal
        base, extension = os.path.splitext(self.ruta_audio_original)
        self.ruta_audio_temp = f"{base}_temp{extension}"
        

        self.setWindowTitle(f"Detalle Pregunta {self.num_pregunta}")
        self.setFixedSize(1000, 650)        

        principal_layout = QVBoxLayout(self)
        principal_layout.setSpacing(20)
        principal_layout.setContentsMargins(10,10,10,10)

        # --- Título y Nivel ---
        top_layout = QHBoxLayout()
        datos = self.PREGUNTAS_DATA.get(str(self.num_pregunta), {})
        titulo_json = datos.get("titulo", f"Pregunta {self.num_pregunta}")
        
        titulo_texto = f"Pregunta {self.num_pregunta}: {titulo_json}"
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
        self.txt_respuesta.setText(self.pregunta_actual.respuesta)
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
        self.boton_play.setFocusPolicy(Qt.NoFocus)
        self.boton_play.setIcon(QIcon("assets/play.png")) 
        self.boton_play.setIconSize(QSize(20, 20))
        self.boton_play.setFixedSize(50, 50)
        self.boton_play.setToolTip("Reproducir grabación")
        self.boton_play.setCursor(Qt.PointingHandCursor)
        self.boton_play.setStyleSheet(ESTILO_BOTON_PLAY)
        
        self.boton_play.clicked.connect(self.toggle_audio)

        # Botón Grabar
        self.boton_grabar = QPushButton()
        self.boton_grabar.setFocusPolicy(Qt.NoFocus)
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
        self.boton_guardar.clicked.connect(self.guardar_datos)

        boton_layout.addWidget(self.boton_cerrar)
        boton_layout.addStretch() 
        boton_layout.addWidget(self.boton_guardar)

        principal_layout.addLayout(boton_layout)

    def guardar_datos(self):
        """
        Si hay audio nuevo, borra el original y renombra el temporal.
        Luego acepta el diálogo.
        """
        # 1. Detener cualquier reproducción para liberar el archivo
        self.player.stop()
        self.player.setMedia(QMediaContent())

        # Si se grabó un nuevo audio
        if self.tiene_nuevo_audio and os.path.exists(self.ruta_audio_temp):
            try:
                # Si existe el original, lo borramos
                if os.path.exists(self.ruta_audio_original):
                    os.remove(self.ruta_audio_original)
                
                # Renombramos el temporal -> original
                os.rename(self.ruta_audio_temp, self.ruta_audio_original)                            
                
            except Exception as e:
                print(f"Error al guardar/renombrar audio: {e}")     
                msg = Mensajes(self)           
                msg.mostrar_advertencia("Error", f"No se pudo guardar el audio: {e}")
                return

        # 3. Cerramos el diálogo con éxito
        self.accept()

    # --- LÓGICA DE GRABACIÓN ---
    def toggle_grabacion(self):
        if not self.grabando:
            # INICIAR GRABACIÓN
            self.grabando = True

            #Bloquear botones cerrar y guardar
            self.boton_cerrar.setEnabled(False) 
            self.boton_guardar.setEnabled(False)  

            # Bloquear reproducción
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            self.boton_play.setEnabled(False) # No reproducir mientras grabas      
            
            # Visuales
            self.boton_grabar.setProperty("grabando", True)
            self.boton_grabar.style().unpolish(self.boton_grabar)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/pausa.png")) # Icono de stop
            self.boton_grabar.setIconSize((QSize(20, 20)))        

            # Hilo
            self.hilo_grabacion = HiloTranscripcion(self.ruta_modelo_vosk, self.ruta_audio_temp)

            #Señales
            self.hilo_grabacion.texto_signal.connect(self.actualizar_texto_final)
            self.hilo_grabacion.parcial_signal.connect(self.actualizar_texto_parcial)
            self.hilo_grabacion.error_signal.connect(self.mostrar_error_transcripcion)
            self.hilo_grabacion.start() 
                                    
            # Feedback
            self.lbl_estado_grabacion.setText("🔴 Grabando... (Hable ahora)")
            self.lbl_estado_grabacion.setStyleSheet("color: #D32F2F; font-weight: bold;")
            self.txt_respuesta.setPlaceholderText("Escuchando...")
            self.txt_respuesta.clear()        

        else:
            # DETENER GRABACIÓN
            self.grabando = False

            self.tiene_nuevo_audio = True

            # Detener hilo
            if self.hilo_grabacion:
                self.hilo_grabacion.detener()
                self.hilo_grabacion.wait()
                self.hilo_grabacion = None
            
            # Visuales
            self.boton_grabar.setProperty("grabando", False)
            self.boton_grabar.style().unpolish(self.boton_grabar)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/micro.png"))
            
            
            # Desbloquear botones
            self.boton_play.setEnabled(True)
            self.boton_cerrar.setEnabled(True)
            self.boton_guardar.setEnabled(True)
            
            # Feedback
            self.lbl_estado_grabacion.setText("✅ Audio listo")
            self.lbl_estado_grabacion.setStyleSheet("color: #388E3C; font-weight: bold;")
            
            # Resetear player para nuevo archivo
            self.player.stop()
            self.player.setMedia(QMediaContent()) 

    def actualizar_texto_final(self,texto):
        """Recibe el texto del hilo y lo añade al cuadro de texto"""
        texto_actual = self.txt_respuesta.toPlainText()
        if texto_actual:
            self.txt_respuesta.append(texto) # Añade en nueva línea o con espacio
        else:
            self.txt_respuesta.setText(texto)
        
        # Movemos el cursor al final
        cursor = self.txt_respuesta.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.txt_respuesta.setTextCursor(cursor)

    def detener_grabacion(self):
        self.grabando = False

        if self.hilo_grabacion:
            self.hilo_grabacion.detener()
            self.hilo_grabacion = None

        self.boton_grabar.setProperty("grabando", False)
        self.boton_grabar.style().polish(self.boton_grabar)
        self.boton_grabar.setIcon(QIcon("assets/micro.png"))
        self.boton_grabar.setIconSize(QSize(30, 30))

        self.lbl_estado_grabacion.setText("Pulse para grabar")
        self.lbl_estado_grabacion.setStyleSheet("color: #666;")     

    def actualizar_texto_parcial(self, parcial):
        """Muestra lo que se está hablando en tiempo real en la etiqueta de estado"""
        # Limitamos el largo para que no descuadre la interfaz
        if len(parcial) > 50:
            parcial = "..." + parcial[-50:]
        self.lbl_estado_grabacion.setText(f"👂 {parcial}")    

    def mostrar_error_transcripcion(self, error):
        self.detener_grabacion() # Detener grabación visualmente
        msg = Mensajes(self)           
        msg.mostrar_advertencia(f"Error de audio", f"Error: {error}\n\nVerifique la carpeta del modelo: {self.ruta_modelo_vosk}")

    # --- LÓGICA DE REPRODUCCIÓN ---
    def toggle_audio(self):
        if self.grabando:
            return

        # 1. Determinar la ruta del archivo
        ruta = None
        if self.tiene_nuevo_audio and os.path.exists(self.ruta_audio_temp):
            ruta = self.ruta_audio_temp
        elif self.ruta_audio_original and os.path.exists(self.ruta_audio_original):
            ruta = self.ruta_audio_original

        if not ruta:
            self.lbl_estado_grabacion.setText("⚠️ No hay audio disponible")
            return

        # 2. Lógica de Control: Play / Pause
        # Solo cargamos el medio si es un archivo distinto o si el reproductor está vacío
        actual_url = QUrl.fromLocalFile(os.path.abspath(ruta))
        
        if self.player.media().canonicalUrl() != actual_url:
            self.player.setMedia(QMediaContent(actual_url))

        # Alternar estado sin reiniciar la posición
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()  # Se detiene en el punto actual
        else:
            self.player.play()   # Reanuda desde donde se quedó


    def cambio_estado_reproductor(self, estado):
        if estado == QMediaPlayer.PlayingState:
            self.boton_play.setIcon(QIcon("assets/pausa.png"))
            self.lbl_estado_grabacion.setText("Reproduciendo...")
            self.lbl_estado_grabacion.setStyleSheet("color: green;")
            self.boton_grabar.setEnabled(False)
        elif estado == QMediaPlayer.PausedState:
            self.boton_play.setIcon(QIcon("assets/play.png"))
            self.lbl_estado_grabacion.setText("Pausado")
            self.lbl_estado_grabacion.setStyleSheet("color: orange;")
            self.boton_grabar.setEnabled(True)
        else: # StoppedState
            self.boton_play.setIcon(QIcon("assets/play.png"))
            if not self.grabando:
                self.lbl_estado_grabacion.setText("Listo")
                self.boton_grabar.setEnabled(True)

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
    
    def get_datos(self):
        """
        Devuelve la información necesaria para el controlador.
        """
        return {
            "texto": self.txt_respuesta.toPlainText(),
            "ruta_audio": self.ruta_audio_original,            
        }
    
    def mostrar_confirmacion_cerrar(self):
        dialogo = QDialog(self)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        dialogo.setModal(True)

        # Layout principal
        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)

        # --- FONDO ---
        fondo = QFrame()
        fondo.setObjectName("FondoDialogo")
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR) 

        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(10)

        # --- CABECERA ---
        layout_cabecera = QHBoxLayout()

        lbl_icono = QLabel()
        pixmap = QPixmap("assets/error.png").scaled(
            30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        lbl_icono.setPixmap(pixmap)        

        titulo = QLabel("Cerrar respuesta")
        titulo.setObjectName("TituloError")

        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()

        # --- MENSAJE ---
        lbl_mensaje = QLabel(
            "¿Está seguro de cerrar?\nPerderá los datos no guardados"
        )
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(320)

        # --- BOTONES ---
        btn_si = QPushButton("Sí")
        btn_no = QPushButton("No")

        btn_si.setCursor(Qt.PointingHandCursor)
        btn_no.setCursor(Qt.PointingHandCursor)

        btn_si.setStyleSheet("""
            QPushButton {
                background-color: #792A24;
                color: white;
                border-radius: 10px;
                padding: 8px 25px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C03930; }
        """)

        btn_no.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 10px;
                padding: 8px 25px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #777; }
        """)

        btn_si.clicked.connect(dialogo.accept)
        btn_no.clicked.connect(dialogo.reject)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(btn_no)
        layout_botones.addWidget(btn_si)

        # --- ENSAMBLADO ---
        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(10)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(20)
        layout_interno.addLayout(layout_botones)

        layout_main.addWidget(fondo)

        # --- EJECUCIÓN ---
        resultado = dialogo.exec_()
        return resultado == QDialog.Accepted

    def cerrar_ventana(self):
        if self.mostrar_confirmacion_cerrar() is True:
            self.reject()

    def closeEvent(self, event):
        """
        Si cerramos (reject), borramos el temporal.
        Si guardamos (accept), el temporal ya se renombró en guardar_datos, 
        así que no hay nada que borrar en esa ruta.
        """
        # Detener procesos siempre
        if self.hilo_grabacion:
            self.detener_grabacion()
        
        self.player.stop()
        self.player.setMedia(QMediaContent()) # Liberar archivo

        # Si el resultado NO es aceptado (es decir, es cancelar/cerrar)
        if self.result() != QDialog.Accepted:
            if os.path.exists(self.ruta_audio_temp):
                try:
                    os.remove(self.ruta_audio_temp)
                    print("Cancelado: Audio temporal eliminado.")
                except Exception as e:
                    print(f"Error borrando temp: {e}")
        
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.grabando:
                self.toggle_grabacion() # Si está grabando, lo para
            return # Evita que el evento se propague y haga otras cosas
        super().keyPressEvent(event)
