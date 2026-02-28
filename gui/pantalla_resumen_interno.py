from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QScrollArea, QFrame, QSizePolicy, QButtonGroup
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from db.pregunta_db import obtener_preguntas_como_diccionario

from gui.estilos import *



def cargar_datos_preguntas():
    return obtener_preguntas_como_diccionario()



class PantallaResumen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        
        #Contenedor lógico para manejar botones de entrar
        self.grupo_botones_entrar = QButtonGroup(self)

        # --- Configuración del layout principal ---
        principal_layout = QVBoxLayout(self)       

        # ------------------- 1. Título Superior -------------------
        titulo_pantalla = QLabel("Entrevista de interno X")
        titulo_pantalla.setFont(QFont("Arial", 20, QFont.Bold))
        titulo_pantalla.setAlignment(Qt.AlignLeft)
        principal_layout.addWidget(titulo_pantalla)

        # ------------------- 2. Área de Scroll -------------------
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) # contenido se ajuste al ancho
        self.scroll_area.setFrameShape(QFrame.NoFrame) # Sin borde
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Sin scroll horizontal
        self.scroll_area.setStyleSheet(ESTILO_SCROLL)
        
        self.scroll_content_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content_widget)       
        self.scroll_content_layout.setAlignment(Qt.AlignTop)
        self.scroll_content_layout.setSpacing(20) # Espacio entre tarjetas
        self.scroll_content_layout.setContentsMargins(50, 20, 50, 0)

        self.scroll_area.setWidget(self.scroll_content_widget)                
        
        principal_layout.addWidget(self.scroll_area, 1) # máximo espacio posible 

        # ------------------- 3. Botón Atrás Inferior -------------------
        boton_layout = QHBoxLayout()
        
        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setFixedSize(150, 50)
        self.boton_atras.setCursor(Qt.PointingHandCursor)
        self.boton_atras.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_atras.setToolTip("Volver a la pantalla de preguntas")
        
        boton_layout.addWidget(self.boton_atras)
        boton_layout.addStretch() # botón a la izquierda

        principal_layout.addLayout(boton_layout)


    # ------------------- Funciones Auxiliares -------------------
    
    def crear_tarjeta_pregunta(self, numero, titulo, texto):
        
        tarjeta_frame = QFrame()        

        tarjeta_frame.setStyleSheet(ESTILO_TARJETA_RESUMEN)

        tarjeta_layout = QVBoxLayout(tarjeta_frame)
        tarjeta_layout.setContentsMargins(25, 20, 25, 10)
        tarjeta_layout.setSpacing(10)

        # Layout para titulo y nivel
        top_tarjeta_layout = QHBoxLayout()                

        # Título de la pregunta
        lbl_titulo = QLabel(f"Pregunta {numero}: {titulo}")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        top_tarjeta_layout.addWidget(lbl_titulo)
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)

        top_tarjeta_layout.addStretch() # Nivel a la derecha        

        tarjeta_layout.addLayout(top_tarjeta_layout)
                
        # Contenido (Respuesta, Nivel, Análisis)        
        lbl_respuesta = QLabel(f"<b>Respuesta:</b> {texto}")
        lbl_respuesta.setFont(QFont("Arial", 11))
        lbl_respuesta.setWordWrap(True) # texto salta de línea si es muy largo
        lbl_respuesta.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_respuesta.setAlignment(Qt.AlignJustify)
        tarjeta_layout.addWidget(lbl_respuesta)  

        # Botón de entrar
        boton_layout = QHBoxLayout()
        boton_layout.addStretch() #icono a la derecha
               
        icono_entrar = QIcon("assets/entrar.png")

        boton_entrar = QPushButton()
        boton_entrar.setFixedSize(45, 45)
        boton_entrar.setIcon(icono_entrar)
        boton_entrar.setIconSize(QSize(25, 25))
        boton_entrar.setCursor(Qt.PointingHandCursor)
        boton_entrar.setStyleSheet(ESTILO_BOTON_TARJETA)
        boton_entrar.setToolTip(f"Ver detalles de la respuesta {numero}")
        
        #Añadir el botón al grupo
        self.grupo_botones_entrar.addButton(boton_entrar, numero)

        boton_layout.addWidget(boton_entrar)
        
        tarjeta_layout.addLayout(boton_layout)

        return tarjeta_frame
    
    def cargar_datos_respuestas(self, entrevista):
        """
        Genera un contenedor NUEVO con las tarjetas.
        """
        while self.scroll_content_layout.count():
            item = self.scroll_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        respuestas = entrevista.respuestas

        for i in range(1, 11):
            clave = str(i)
            datos_json = self.PREGUNTAS_DATA.get(clave, {})
            titulo = datos_json.get("titulo", f"Pregunta {i}")
                
            if i <= len(respuestas):
                texto_respuesta = respuestas[i-1].respuesta
            else:
                texto_respuesta = "Sin respuesta"
            
            tarjeta = self.crear_tarjeta_pregunta(i, titulo, texto_respuesta)

            self.scroll_content_layout.addWidget(tarjeta)
