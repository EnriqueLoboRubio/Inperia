from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QDialog, QFrame
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QTextCursor
from PyQt5.QtCore import Qt, QSize, pyqtSignal 
from datetime import datetime
import json, os

from utils.transcripcionVosk import HiloTranscripcion

from gui.estilos import *

def cargar_datos_preguntas():
    
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_json = os.path.join(ruta_base, 'data', 'preguntas.json')

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos_preguntas = json.load(f)
            return datos_preguntas
    except Exception as e:
        return {"1": {"titulo": "Error", "texto": "Error al cargar archivo."}}

class PantallaPreguntas(QWidget):

    #Señales
    entrevista_finalizada = pyqtSignal(list, list)  

    def __init__(self, parent=None):
        super().__init__(parent)    

        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        self.grabando = False # Estado inicial de la grabación    
        self.hilo_grabacion = None

        ruta_base = os.path.dirname(os.path.dirname(__file__))
        self.ruta_modelo_vosk = os.path.join(ruta_base, "utils", "vosk-es", "small")      

        self.id_entrevista = 0       
        self.carpeta_audios = os.path.join(ruta_base, "data", "grabaciones")
        if not os.path.exists(self.carpeta_audios):
            os.makedirs(self.carpeta_audios)     
            
        principal_layout = QVBoxLayout(self)                     
        
        # ------------------- 1. Título pregunta con botón de información -------------------
        self.pregunta_widget = QWidget()
        self.pregunta_layout = QHBoxLayout(self.pregunta_widget)
        self.pregunta_layout.setAlignment(Qt.AlignCenter)

        # Botón de información
        self.boton_info = QPushButton()
        self.boton_info.setToolTip("Información sobre la pregunta")
        self.boton_info.setFixedSize(40, 40)
        self.boton_info.setIcon(QIcon("assets/info.png"))
        self.boton_info.setIconSize(QSize(30, 30))
        self.boton_info.setStyleSheet("""
            QPushButton { background: rgba(200, 200, 200, 0.6); border-radius: 15px;; padding: 10px; }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 15px; }
        """)

        #Popup ayuda
        self.popup_ayuda = QLabel(self)
        self.popup_ayuda.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;       
                color: #333333;                  
                border: 2px solid #333333;       
                border-radius: 15px;            
                padding: 20px;               
                font-family: 'Arial';
                font-size: 20px;               
                font-weight: normal;
            }
        """)
        self.popup_ayuda.setWordWrap(True)
        self.popup_ayuda.setFixedWidth(400)
        self.popup_ayuda.hide() #oculto al principio

        # filtro de eventos para detectar el ratón en el botón
        self.boton_info.installEventFilter(self)

        # Variable para el número de pregunta
        self.numero_pregunta = 1
        
        # Título de la pregunta
        self.titulo_pregunta = QLabel("Pregunta "+ str(self.numero_pregunta) + " :")
        self.titulo_pregunta.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo_pregunta.setAlignment(Qt.AlignLeft)

        self.pregunta_layout.addWidget(self.boton_info)
        self.pregunta_layout.setSpacing(10)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        # ------------------- 2. Texto con la pregunta -------------------        
        self.lista_respuestas = [""] * len(self.PREGUNTAS_DATA)
        self.lista_audios = [""] * len(self.PREGUNTAS_DATA)

        self.texto_pregunta = QLabel()
        self.texto_pregunta.setFont(QFont("Arial", 14))
        self.texto_pregunta.setAlignment(Qt.AlignCenter)
        self.texto_pregunta.setWordWrap(True) # Para que el texto no se corte si es largo

        # ------------------- 3. Entrada de la pregunta -------------------  
        self.txt_respuesta = QTextEdit()
        self.txt_respuesta.setFont(QFont("Arial", 12))
        self.txt_respuesta.setPlaceholderText("Escriba su respuesta aquí o use el micrófono...")
        self.txt_respuesta.setFixedHeight(350)
        # self.respuesta_widget.setFixedWidth(1600)
        self.txt_respuesta.setStyleSheet("""
            QTextEdit {
                border-radius: 10px;
                border: 1px solid #ccc;
                padding: 15px;
                background-color: #f7f7f7;
            }
            QTextEdit:hover { border: 1px solid #999; }
            QTextEdit:focus { border: 1px solid #0078d7; }
        """)
        
        # ------------------- 4. Área de Grabación (Mensaje + Botón) -------------------
        
        # Etiqueta de estado
        self.lbl_estado_grabacion = QLabel("Pulse para grabar")
        self.lbl_estado_grabacion.setAlignment(Qt.AlignCenter)
        self.lbl_estado_grabacion.setFont(QFont("Arial", 10))
        self.lbl_estado_grabacion.setStyleSheet("color: #666;")

        # Botón Micrófono
        self.boton_grabar = QPushButton()
        self.boton_grabar.setFocusPolicy(Qt.NoFocus)
        self.boton_grabar.setToolTip("Responder por voz")
        self.boton_grabar.setFixedSize(60, 60)
        self.boton_grabar.setIcon(QIcon("assets/micro.png"))
        self.boton_grabar.setIconSize(QSize(30, 30))
        self.boton_grabar.setProperty("grabando", False)
        self.boton_grabar.setCursor(Qt.PointingHandCursor)
        self.boton_grabar.setToolTip("Grabar respuesta")
        self.boton_grabar.setStyleSheet(ESTILO_BOTON_GRABAR)

        # ------------------- 5. Botones navegación -------------------
        self.botones_widget = QWidget()
        self.botones_layout = QHBoxLayout(self.botones_widget)
        self.botones_layout.addStretch(1)
       
        estilo_finalizar = ESTILO_BOTON_SIG_ATR.replace("black", "#1E5631").replace("rgba(71, 70, 70, 0.7)", "#3A9D5A")    

        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setFixedSize(150,50)
        self.boton_atras.hide()

        self.boton_siguiente = QPushButton("Siguiente")                 
        self.boton_siguiente.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_siguiente.setFixedSize(150,50)   

        self.boton_finalizar = QPushButton("Finalizar")       
        self.boton_finalizar.setStyleSheet(estilo_finalizar)
        self.boton_finalizar.setFont(QFont("Arial", 12))
        self.boton_finalizar.setFixedSize(150,50)
        self.boton_finalizar.hide()

        self.botones_layout.addWidget(self.boton_atras)
        self.botones_layout.addStretch(1)
        self.botones_layout.addWidget(self.boton_siguiente)
        self.botones_layout.addWidget(self.boton_finalizar)
        self.botones_layout.addStretch(1)                
        
        # ------------------- 6. Conexiones ------------------- 
        self.boton_grabar.clicked.connect(self.toggle_grabacion)
        
        # Conexiones de navegación
        #self.boton_siguiente.clicked.connect(self.ir_pregunta_siguiente)
        #self.boton_atras.clicked.connect(self.ir_pregunta_atras)
        #self.boton_finalizar.clicked.connect(self.finalizar_entrevista)

        # ------------------- 7. Añadir widgets -------------------
        principal_layout.addWidget(self.pregunta_widget)
        principal_layout.addSpacing(20)
        principal_layout.addWidget(self.texto_pregunta)
        principal_layout.addSpacing(10)
        principal_layout.addWidget(self.txt_respuesta)
        principal_layout.addSpacing(15)
        
        # Añadir mensaje y botón de grabar centrados
        principal_layout.addWidget(self.lbl_estado_grabacion, alignment=Qt.AlignCenter)
        principal_layout.addWidget(self.boton_grabar, alignment=Qt.AlignCenter)
    
        principal_layout.addStretch(1)
        principal_layout.addWidget(self.botones_widget)
        principal_layout.addSpacing(20)    

        self.cargar_pregunta(1)

    # ------------------- 8. Funciones Lógica -------------------

    def toggle_grabacion(self):          
        if not self.grabando:
            # INICIAR GRABACIÓN
            self.grabando = True

            # BLOQUEAR botones de navegación
            self.boton_atras.setEnabled(False)
            self.boton_siguiente.setEnabled(False)
            self.boton_finalizar.setEnabled(False)
            
            # Cambios visuales
            self.boton_grabar.setProperty("grabando", True)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/pausa.png"))
            self.boton_grabar.setIconSize((QSize(20, 20))) 

            #Archivo de salida
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_audio = f"audio_{timestamp}.wav"
            ruta_audio_salida = os.path.join(self.carpeta_audios, nombre_audio)

            if self.lista_audios[self.numero_pregunta - 1] == "":
                self.lista_audios[self.numero_pregunta - 1] = ruta_audio_salida
            
            #Hilo
            self.hilo_grabacion = HiloTranscripcion(self.ruta_modelo_vosk, ruta_audio_salida)
            
            #Señales
            self.hilo_grabacion.texto_signal.connect(self.actualizar_texto_final)
            self.hilo_grabacion.parcial_signal.connect(self.actualizar_texto_parcial)
            self.hilo_grabacion.error_signal.connect(self.mostrar_error_transcripcion)
            self.hilo_grabacion.start()        
            
            # Mensajes
            self.lbl_estado_grabacion.setText("🔴 Grabando... (Hable ahora)")
            self.lbl_estado_grabacion.setStyleSheet("color: #D32F2F; font-weight: bold;")
            self.txt_respuesta.setPlaceholderText("Escuchando...")
            self.txt_respuesta.clear()
            
        else:
            # DETENER GRABACIÓN
            self.grabando = False

            # Detener hilo
            if self.hilo_grabacion:
                self.hilo_grabacion.detener()
                self.hilo_grabacion.wait()
                self.hilo_grabacion = None
            
            # Cambios visuales
            self.boton_grabar.setProperty("grabando", False)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/micro.png")) # Volver a icono micro
            self.boton_grabar.setIconSize(QSize(30, 30))
            
            # Mensajes
            self.lbl_estado_grabacion.setText("✅ Audio listo")
            self.lbl_estado_grabacion.setStyleSheet("color: #388E3C; font-weight: bold;")
        
            #self.respuesta_widget.setPlaceholderText("Escriba su respuesta aquí o use el micrófono...")       

            # DESBLOQUEAR botones de navegación
            self.boton_atras.setEnabled(True)
            self.boton_siguiente.setEnabled(True)
            self.boton_finalizar.setEnabled(True)

    def actualizar_texto_final(self, texto):
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
        self.mostrar_validacion_error(f"Error de audio: {error}\n\nVerifique la carpeta del modelo: {self.ruta_modelo_vosk}")

    def cargar_pregunta(self, numero):
        self.numero_pregunta = numero
        # Resetear estado de grabación al cambiar de pregunta
        if self.grabando:
            self.detener_grabacion()

        self.grabando = False
        self.boton_grabar.setProperty("grabando", False)
        self.boton_grabar.style().polish(self.boton_grabar)
        self.boton_grabar.setIcon(QIcon("assets/micro.png"))
        self.boton_grabar.setIconSize(QSize(30, 30))
        self.lbl_estado_grabacion.setText("Pulse para grabar")
        self.lbl_estado_grabacion.setStyleSheet("color: #666;")    
        
        # Cargar datos JSON
        datos = self.PREGUNTAS_DATA.get(str(numero), {
            "titulo": "Error",
            "texto": f"Pregunta {numero} no encontrada en el JSON.",
            "ayuda": "No hay información disponible"
        })

        self.titulo_pregunta.setText(f"Pregunta {numero}")
        self.texto_pregunta.setText(datos['texto'])

        texto_ayuda = datos.get("ayuda", "Sin información adicional.")       
        self.popup_ayuda.setText(texto_ayuda)
        self.popup_ayuda.adjustSize() # Ajustar alto al contenido

        #Cargar respuesta si la hay
        if self.lista_respuestas[numero -1] != "":
            self.txt_respuesta.setText(self.lista_respuestas[numero -1])
        else:
            self.txt_respuesta.setText("")
            

        # Lógica de botones (Siguiente/Atrás)
        if self.numero_pregunta > 1:
            self.boton_atras.show()
        else:
            self.boton_atras.hide()

        if self.numero_pregunta == 10:
            self.boton_siguiente.hide()
            self.boton_finalizar.show()
        else:
            self.boton_siguiente.show()
            self.boton_finalizar.hide()

    def ir_pregunta_atras(self):
        self.lista_respuestas[self.numero_pregunta-1] = self.txt_respuesta.toPlainText()
        self.numero_pregunta -= 1
        self.restaurar_respuesta() # Refactorizado para no repetir código

    def ir_pregunta_siguiente(self):
        self.lista_respuestas[self.numero_pregunta-1] = self.txt_respuesta.toPlainText()
        self.numero_pregunta += 1
        self.restaurar_respuesta()

    def restaurar_respuesta(self):
        # Método auxiliar para cargar la respuesta y la pregunta
        if(self.lista_respuestas[self.numero_pregunta - 1] != ""):
            self.txt_respuesta.setText(self.lista_respuestas[self.numero_pregunta - 1]) 
        else:
            self.txt_respuesta.clear() 
        
        self.cargar_pregunta(self.numero_pregunta)

    def finalizar_entrevista(self):
        # Guardar la última respuesta
        self.lista_respuestas[self.numero_pregunta-1] = self.txt_respuesta.toPlainText()
        
        preguntas_sin_contestar = []
        for i, respuesta in enumerate(self.lista_respuestas):            
            if not respuesta or respuesta.strip() == "":
                preguntas_sin_contestar.append(str(i + 1))    
        
        if preguntas_sin_contestar:
            mensaje = f"Aún faltan por contestar las siguientes preguntas: {', '.join(preguntas_sin_contestar)}.\n\nPor favor, complete todas las respuestas antes de finalizar."
            self.mostrar_validacion_error(mensaje)
        else:
            # Todo correcto
            self.entrevista_finalizada.emit(self.lista_respuestas, self.lista_audios)

    def eventFilter(self, obj, event):
        if obj == self.boton_info:
            if event.type() == 10: 
    
                pos = self.boton_info.mapTo(self, self.boton_info.rect().bottomRight())
                self.popup_ayuda.move(pos.x(), pos.y())
                self.popup_ayuda.raise_() 
                self.popup_ayuda.show()
                return True
            elif event.type() == 11: 
                self.popup_ayuda.hide()
                return True
        return super().eventFilter(obj, event)
    
    def mostrar_validacion_error(self, mensaje):

        dialogo = QDialog(self)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) 
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        
        # Layout principal del diálogo
        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)
        
        # --- MARCO DE FONDO ---
        fondo = QFrame()
        fondo.setObjectName("FondoDialogo") 
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)
            
        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(5)
        
        # --- ICONO Y TÍTULO  ---
        layout_cabecera = QHBoxLayout()
        layout_cabecera.setSpacing(10)
        
        lbl_icono = QLabel()
        pixmap = QPixmap("assets/error.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
        lbl_icono.setPixmap(pixmap) 
        lbl_icono.setFixedSize(30, 30)
        lbl_icono.setStyleSheet("background: transparent; border: none;")

        titulo = QLabel("Atención")
        titulo.setObjectName("TituloError")
        
        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()
        
        # --- TEXTO DEL MENSAJE ---
        lbl_mensaje = QLabel(mensaje)
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(300) 
        
        # --- BOTÓN ---
        boton = QPushButton("Ok")
        boton.setCursor(Qt.PointingHandCursor)
        boton.setStyleSheet("""
            QPushButton { 
                background-color: black; 
                color: white; 
                border-radius: 10px; 
                padding: 8px 20px;
                font-family: 'Arial';
                font-weight: bold;
                font-size: 9pt;
            }
            QPushButton:hover { background-color: #333; }
        """)
        boton.clicked.connect(dialogo.accept)
     
        layout_boton = QHBoxLayout()
        layout_boton.addStretch()
        layout_boton.addWidget(boton)
                
        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(5)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(15)
        layout_interno.addLayout(layout_boton)
        
        layout_main.addWidget(fondo)
        
        dialogo.exec_()    


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.grabando:
                self.toggle_grabacion() # Si está grabando, lo para
            return # Evita que el evento se propague y haga otras cosas
        super().keyPressEvent(event)