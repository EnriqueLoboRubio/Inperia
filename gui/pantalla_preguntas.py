from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QTimer 
import json, os

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
    def __init__(self, parent=None):
        super().__init__(parent)

        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        self.grabando = False # Estado inicial de la grabación
            
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

        # Variable para el número de pregunta
        self.numero_pregunta = 1
        
        # Título de la pregunta
        self.titulo_pregunta = QLabel("Pregunta "+ str(self.numero_pregunta) + " :")
        self.titulo_pregunta.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo_pregunta.setAlignment(Qt.AlignLeft)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        self.pregunta_layout.addWidget(self.boton_info)
        self.pregunta_layout.setSpacing(10)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        # ------------------- 2. Texto con la pregunta -------------------        
        self.lista_respuestas = [""] * 10 

        self.texto_pregunta = QLabel()
        self.texto_pregunta.setFont(QFont("Arial", 14))
        self.texto_pregunta.setAlignment(Qt.AlignCenter)
        self.texto_pregunta.setWordWrap(True) # Para que el texto no se corte si es largo

        # ------------------- 3. Entrada de la pregunta -------------------  
        self.respuesta_widget = QTextEdit()
        self.respuesta_widget.setFont(QFont("Arial", 12))
        self.respuesta_widget.setPlaceholderText("Escriba su respuesta aquí o use el micrófono...")
        self.respuesta_widget.setFixedHeight(350)
        # self.respuesta_widget.setFixedWidth(1600)
        self.respuesta_widget.setStyleSheet("""
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
        self.boton_grabar.setToolTip("Responder por voz")
        self.boton_grabar.setFixedSize(60, 60)
        self.boton_grabar.setIcon(QIcon("assets/micro.png"))
        self.boton_grabar.setIconSize(QSize(30, 30))
        self.boton_grabar.setProperty("grabando", False)
        self.boton_grabar.setCursor(Qt.PointingHandCursor)
        self.boton_grabar.setToolTip("Grabar respuesta")
        self.boton_grabar.setStyleSheet("""
            QPushButton { 
                background: #FFFFFF; 
                border: 2px solid #D32F2F;
                border-radius: 30px;
            }
            QPushButton:hover { background-color: #FFEBEE; }
            QPushButton[grabando="true"] { 
                background-color: #D32F2F; 
                border: none;
            }
        """)

        # ------------------- 5. Botones navegación -------------------
        self.botones_widget = QWidget()
        self.botones_layout = QHBoxLayout(self.botones_widget)
        self.botones_layout.addStretch(1)

        estilo_boton = """                                   
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: center;
                background-color: black; 
                border-radius: 15px;
            }
            QPushButton:hover { background-color: rgba(71, 70, 70, 0.7); }
        """
        estilo_finalizar = estilo_boton.replace("black", "#1E5631").replace("rgba(71, 70, 70, 0.7)", "#3A9D5A")    

        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setStyleSheet(estilo_boton)
        self.boton_atras.setFixedSize(150,50)
        self.boton_atras.hide()

        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setFont(QFont("Arial", 12))
        self.boton_siguiente.setStyleSheet(estilo_boton)    
        self.boton_siguiente.setFixedSize(150,50)   

        self.boton_finalizar = QPushButton("Finalizar")
        self.boton_finalizar.setFont(QFont("Arial", 12))
        self.boton_finalizar.setStyleSheet(estilo_finalizar)
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
        principal_layout.addWidget(self.respuesta_widget)
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
            
            # Cambios visuales
            self.boton_grabar.setProperty("grabando", True)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/pausa.png"))
            self.boton_grabar.setIconSize((QSize(20, 20))) 
            
            # Mensajes
            self.lbl_estado_grabacion.setText("🔴 Grabando... (Hable ahora)")
            self.lbl_estado_grabacion.setStyleSheet("color: #D32F2F; font-weight: bold;")
            self.respuesta_widget.setPlaceholderText("Escuchando...")
            self.respuesta_widget.clear()
            
        else:
            # DETENER GRABACIÓN
            self.grabando = False
            
            # Cambios visuales
            self.boton_grabar.setProperty("grabando", False)
            self.boton_grabar.style().polish(self.boton_grabar)
            self.boton_grabar.setIcon(QIcon("assets/micro.png")) # Volver a icono micro
            self.boton_grabar.setIconSize(QSize(30, 30))
            
            # Mensajes
            self.lbl_estado_grabacion.setText("⏳ Procesando audio...")
            self.lbl_estado_grabacion.setStyleSheet("color: #F57C00; font-weight: bold;")
            
            # Simular espera de transcripción (1.5 segundos)
            QTimer.singleShot(1500, self.simular_transcripcion)

    def simular_transcripcion(self):
        # Esta función se ejecuta tras el delay
        texto_simulado = f"Respuesta transcrita automáticamente para la pregunta {self.numero_pregunta}. El usuario ha hablado sobre su situación familiar y expectativas."
        
        self.respuesta_widget.setText(texto_simulado)
        self.lbl_estado_grabacion.setText("✅ Transcripción completada")
        self.lbl_estado_grabacion.setStyleSheet("color: #388E3C; font-weight: bold;")

    def cargar_pregunta(self, numero):
        # Resetear estado de grabación al cambiar de pregunta
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
            "texto": f"Pregunta {numero} no encontrada en el JSON."
        })

        self.titulo_pregunta.setText(f"Pregunta {numero}")
        self.texto_pregunta.setText(datos['texto'])

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
        self.lista_respuestas[self.numero_pregunta-1] = self.respuesta_widget.toPlainText()
        self.numero_pregunta -= 1
        self.restaurar_respuesta() # Refactorizado para no repetir código

    def ir_pregunta_siguiente(self):
        self.lista_respuestas[self.numero_pregunta-1] = self.respuesta_widget.toPlainText()
        self.numero_pregunta += 1
        self.restaurar_respuesta()

    def restaurar_respuesta(self):
        # Método auxiliar para cargar la respuesta y la pregunta
        if(self.lista_respuestas[self.numero_pregunta - 1] != ""):
            self.respuesta_widget.setText(self.lista_respuestas[self.numero_pregunta - 1]) 
        else:
            self.respuesta_widget.clear() 
        
        self.cargar_pregunta(self.numero_pregunta)

    def finalizar_entrevista(self):
        # Guardar la última respuesta
        self.lista_respuestas[self.numero_pregunta-1] = self.respuesta_widget.toPlainText()
        print("Entrevista finalizada. Respuestas:", self.lista_respuestas)
        # Aquí emitirías la señal