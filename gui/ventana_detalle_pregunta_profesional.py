from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QScrollArea, QFrame, QWidget, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import json, os

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

        self.setWindowTitle(f"Detalle Pregunta {numero}")
        self.setFixedSize(1000, 900) 
        self.setStyleSheet("background-color: white;")

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
        
        lbl_nivel = QLabel(f"Nivel: {pregunta.nivel}")
        lbl_nivel.setFont(QFont("Arial", 11, QFont.Bold))
        lbl_nivel.setStyleSheet(("""
            background-color: transparent; 
            border: 1.5px solid #808080; 
            color: #555555;
            border-radius: 10px; 
            padding: 2px 12px;
        """)) 
        lbl_nivel.setFixedSize(110,50)
        top_layout.addWidget(lbl_nivel)
        
        principal_layout.addLayout(top_layout)   

        # --- Texto de la Respuesta (Transcripción) ---
        estilo_text_box = """
        QTextEdit {
            background-color: #F9FAFB; 
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 10px;
            color: #374151;
            font-family: Arial;
            font-size: 18px; 
        }
        """     

        lbl_trancripcion = QLabel("<b>Transcripción:</b>")
        lbl_trancripcion.setFont(QFont("Arial",11))
        principal_layout.addWidget(lbl_trancripcion)

        self.txt_respuesta = QTextEdit()
        self.txt_respuesta.setReadOnly(True)
        self.txt_respuesta.setStyleSheet(estilo_text_box)
        self.txt_respuesta.setText(pregunta.respuesta)
        self.txt_respuesta.setMaximumHeight(150) # Altura limitada para dejar sitio al scroll
        self.txt_respuesta.setMinimumHeight(60)

        principal_layout.addWidget(self.txt_respuesta)

       # --- Reproductor de Audio ---
        self.player = QMediaPlayer()

        audio_layout = QVBoxLayout()
        audio_layout.setSpacing(10)

        # Estado
        self.lbl_estado_audio = QLabel("")
        self.lbl_estado_audio.setAlignment(Qt.AlignCenter)
        self.lbl_estado_audio.setStyleSheet("color: #6B7280; font-size: 12px;")

        # Barra de progreso
        self.slider_audio = QSlider(Qt.Horizontal)
        self.slider_audio.setRange(0, 0)
        self.slider_audio.setCursor(Qt.PointingHandCursor)
        self.slider_audio.setStyleSheet("""
        QSlider::groove:horizontal {
            height: 6px;
            background: #E5E7EB;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            width: 14px;
            background: #1E5631;
            border-radius: 7px;
            margin: -4px 0;
        }
        QSlider::sub-page:horizontal {
            background: #3A9D5A;
            border-radius: 3px;
        }
        """)

        # Tiempo
        time_layout = QHBoxLayout()
        self.lbl_tiempo_actual = QLabel("00:00")
        self.lbl_tiempo_total = QLabel("00:00")

        for lbl in (self.lbl_tiempo_actual, self.lbl_tiempo_total):
            lbl.setFont(QFont("Arial", 10))
            lbl.setStyleSheet("color: #374151;")

        time_layout.addWidget(self.lbl_tiempo_actual)
        time_layout.addStretch()
        time_layout.addWidget(self.lbl_estado_audio)
        time_layout.addStretch()
        time_layout.addWidget(self.lbl_tiempo_total)

        # Botón Play / Pause
        self.boton_play = QPushButton()
        self.boton_play.setIcon(QIcon("assets/play.png"))
        self.boton_play.setIconSize(QSize(20, 20))
        self.boton_play.setFixedSize(30, 30)
        self.boton_play.setCursor(Qt.PointingHandCursor)
        self.boton_play.setStyleSheet("""
            /* Estilo Base */
            QPushButton { 
                background: rgba(200, 200, 200, 0.6); 
                border-radius: 15px;
                padding: 10px; 
            }
            
            /* Estilo al pasar el ratón */
            QPushButton:hover { 
                background-color: rgba(128, 128, 128, 0.6); 
            }
            
            /* Estilo cuando el estado es activo */
            QPushButton[estado_grabando="true"] { 
                background-color: #FF0000;
            }

            /* Estilo hover cuando ya está GRABANDO */
            QPushButton[estado_grabando="true"]:hover { 
                background-color: #CC0000;
            }
        """)

        self.boton_play.clicked.connect(
            lambda: self.toggle_audio(pregunta.archivo_audio)
        )

        audio_layout.addWidget(self.boton_play, alignment=Qt.AlignCenter)
        audio_layout.addWidget(self.slider_audio)
        audio_layout.addLayout(time_layout)
                
        #Señales del reproductor
        self.player.positionChanged.connect(self.actualizar_posicion)
        self.player.durationChanged.connect(self.actualizar_duracion)
        self.slider_audio.sliderMoved.connect(self.player.setPosition)
        self.player.stateChanged.connect(self.cambio_estado)

        principal_layout.addLayout(audio_layout)

        # --- Análisis de la IA ---
        lbl_analisis = QLabel("<b>Análisis de IA:</b>")
        lbl_analisis.setFont(QFont("Arial",11))
        principal_layout.addWidget(lbl_analisis)

        self.txt_analisis = QTextEdit()
        self.txt_analisis.setReadOnly(True)
        self.txt_analisis.setStyleSheet(estilo_text_box)
        self.txt_analisis.setText(pregunta.valoracion_ia)
        self.txt_analisis.setMaximumHeight(150)
        self.txt_analisis.setMinimumHeight(60)

        principal_layout.addWidget(self.txt_analisis) 

        # --- Comentarios ---
        lbl_comentarios = QLabel("<b>Comentarios:</b>")
        lbl_comentarios.setFont(QFont("Arial", 11))
        principal_layout.addWidget(lbl_comentarios)

        # Configuración del Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.StyledPanel)
                
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)            
        scroll_area.setStyleSheet("""
        QScrollArea {
            background-color: #F9FAFB; 
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 10px;
            color: #374151;
            font-family: Arial;
            font-size: 14px; 
        }""")
        
        scroll_content_widget = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content_widget)
        scroll_content_layout.setAlignment(Qt.AlignTop)
        scroll_content_layout.setSpacing(10)
        scroll_content_layout.setContentsMargins(10, 10, 10, 10)
    
        lista_comentarios = pregunta.comentarios                

        if not lista_comentarios:
            # Si no hay comentarios, mostrar un aviso
            lbl_vacio = QLabel("No hay comentarios disponibles para esta pregunta.")
            lbl_vacio.setStyleSheet("color: gray; font-style: italic; padding: 20px;")
            lbl_vacio.setAlignment(Qt.AlignCenter)
            scroll_content_layout.addWidget(lbl_vacio)
        else:
            # Si hay comentarios
            for comentario in lista_comentarios:
                try:
                    tarjeta = self.crear_tarjeta_comentario(comentario)
                    if tarjeta is not None:
                        scroll_content_layout.addWidget(tarjeta)
                    else:
                        print("DEBUG: Error, crear_tarjeta_comentario devolvió None")
                except Exception as e:
                    print(f"DEBUG: Error creando tarjeta: {e}")

        scroll_content_layout.addStretch()
        scroll_area.setWidget(scroll_content_widget)
        
        scroll_area.setMinimumHeight(200) 
        principal_layout.addWidget(scroll_area, 1)

        # --- Botón Cerrar ---
        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(self.close)
        boton_cerrar.setFont(QFont("Arial", 11))   
        boton_cerrar.setFixedSize(110,40)
        boton_cerrar.setStyleSheet("""                                   
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
        boton_cerrar.setCursor(Qt.PointingHandCursor)
        boton_cerrar.setToolTip("Cerrar detalles de la pregunta")
        principal_layout.addWidget(boton_cerrar, alignment=Qt.AlignCenter)

    def reproducir_audio(self, ruta):
        if ruta and os.path.exists(ruta):
            try:
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

    def crear_tarjeta_comentario(self, comentario):
        tarjeta_frame = QFrame()        
        tarjeta_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5; 
                border-radius: 20px;
                border: 2px solid #E0E0E0;
            }
            QLabel {
                border: none;
                background-color: transparent;
                color: black;
            }               
        """)

        tarjeta_layout = QVBoxLayout(tarjeta_frame)
        tarjeta_layout.setContentsMargins(25, 20, 25, 10)
        tarjeta_layout.setSpacing(10)        

        # profesional
        lbl_profesional = QLabel(comentario.id_profesional + " - Nombre Apellidos")
        lbl_profesional.setFont(QFont("Arial", 9))
        lbl_profesional.setStyleSheet("border: none; color: grey;")
        lbl_profesional.setAlignment(Qt.AlignLeft)

        tarjeta_layout.addWidget(lbl_profesional)

        lbl_comentario = QLabel(comentario.contenido)
        lbl_comentario.setFont(QFont("Arial", 10))
        lbl_comentario.setStyleSheet("border: none; color: black;")     
        lbl_comentario.setWordWrap(True)   

        tarjeta_layout.addWidget(lbl_comentario)
                
        return tarjeta_frame
    
    def toggle_audio(self, ruta):
        if not ruta or not os.path.exists(ruta):
            self.lbl_estado_audio.setText("❌ Archivo de audio no encontrado")
            self.lbl_estado_audio.setStyleSheet("color: red;")
            return

        if self.player.mediaStatus() == QMediaPlayer.NoMedia:
            url = QUrl.fromLocalFile(os.path.abspath(ruta))
            self.player.setMedia(QMediaContent(url))

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def cambio_estado(self, estado):
        if estado == QMediaPlayer.PlayingState:
            self.boton_play.setIcon(QIcon("assets/pausa.png"))
            self.boton_play.setIconSize(QSize(15, 15))
            self.lbl_estado_audio.setText("Reproduciendo…")
            self.lbl_estado_audio.setStyleSheet("color: green;")
        else:
            self.boton_play.setIcon(QIcon("assets/play.png"))
            self.boton_play.setIconSize(QSize(20, 20))
            self.lbl_estado_audio.setText("")

    def actualizar_posicion(self, posicion):
        self.slider_audio.setValue(posicion)
        self.lbl_tiempo_actual.setText(self.formatear_tiempo(posicion))

    def actualizar_duracion(self, duracion):
        self.slider_audio.setRange(0, duracion)
        self.lbl_tiempo_total.setText(self.formatear_tiempo(duracion))

    def formatear_tiempo(self, ms):
        segundos = ms // 1000
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02}:{segundos:02}"
