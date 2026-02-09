from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QScrollArea, QFrame, QSizePolicy, QButtonGroup
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
import json, os

from gui.estilos import *


def cargar_datos_preguntas():
    #Carga las preguntas desde el archivo JSON        
    ruta_base = os.path.dirname(os.path.dirname(__file__)) # Sube un nivel de carpeta
    ruta_json = os.path.join(ruta_base, 'data', 'preguntas.json')

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            # Carga el JSON
            datos_preguntas = json.load(f)
            return datos_preguntas
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta_json}")
        # Devuelve datos de error para que la app no falle
        return {
            "1": {
                "titulo": "Error",
                "texto": "No se pudo cargar el archivo 'preguntas.json'."
            }
        }
    except json.JSONDecodeError:
        print(f"Error: El archivo {ruta_json} tiene un formato JSON inválido.")
        return {
            "1": {
                "titulo": "Error",
                "texto": "Error al leer el archivo 'preguntas.json'."
            }
        }



class PantallaResumen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        self.respuestas = []
        
        #Contenedor lógico para manejar botones de entrar
        self.grupo_botones_entrar = QButtonGroup(self)

        # --- Configuración del layout principal ---
        principal_layout = QVBoxLayout(self)       

        # ------------------- 1. Título Superior -------------------
        titulo_pantalla = QLabel("Resumen de Entrevista")
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

        principal_layout.addWidget(self.scroll_area, 1)
        
        # ------------------- 3. Botones Inferior -------------------
        boton_layout = QHBoxLayout()
        boton_layout.setContentsMargins(0, 0, 0, 0)        
        
        #Boton atrás
        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setFixedSize(150, 50)
        self.boton_atras.setCursor(Qt.PointingHandCursor)
        self.boton_atras.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_atras.setToolTip("Volver a la pantalla de preguntas")

        #Boton enviar
        self.boton_enviar = QPushButton("Enviar")
        self.boton_enviar.setFont(QFont("Arial", 12))
        self.boton_enviar.setFixedSize(150, 50)
        self.boton_enviar.setCursor(Qt.PointingHandCursor)       
        self.boton_enviar.setStyleSheet(ESTILO_BOTON_SIG_ATR.replace("black", "#792A24").replace("rgba(71, 70, 70, 0.7)", "#C03930"))
        self.boton_enviar.setToolTip("Enviar respuestas")

        
        boton_layout.addWidget(self.boton_atras)
        boton_layout.addStretch() # botón a la izquierda

        boton_layout.addWidget(self.boton_enviar)
       #boton_layout.addStretch(1) # botón a la derecha

        principal_layout.addLayout(boton_layout)


    # ------------------- Funciones Auxiliares -------------------
    
    def crear_tarjeta_pregunta(self, numero, titulo, texto): #Cambiar a  objeto pregunta
        
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
        if not texto:
            texto = "<i>Sin respuesta registrada</i>"

        lbl_respuesta = QLabel(texto)
        lbl_respuesta.setFont(QFont("Arial", 11))
        lbl_respuesta.setWordWrap(True) # texto salta de línea si es muy largo
        lbl_respuesta.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_respuesta.setAlignment(Qt.AlignJustify)
        tarjeta_layout.addWidget(lbl_respuesta)

        # Botón de entrar
        boton_layout = QHBoxLayout()
        boton_layout.addStretch() #icono a la derecha
               
        icono_editar = QIcon("assets/editar.png")

        boton_editar = QPushButton()
        boton_editar.setFixedSize(45, 45)
        boton_editar.setIcon(icono_editar)
        boton_editar.setIconSize(QSize(25, 25))
        boton_editar.setCursor(Qt.PointingHandCursor)
        boton_editar.setStyleSheet(ESTILO_BOTON_TARJETA)
        boton_editar.setToolTip(f"Ver detalles de la respuesta {numero}")
        
        #Añadir el botón al grupo
        self.grupo_botones_entrar.addButton(boton_editar, numero)

        boton_layout.addWidget(boton_editar)
        
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
            
            # Obtener respuesta segura (evitar error de índice)
            if i <= len(respuestas):
                texto_respuesta = respuestas[i-1]
            else:
                texto_respuesta = "Sin respuesta"
            
            tarjeta = self.crear_tarjeta_pregunta(i, titulo, texto_respuesta)

            self.scroll_content_layout.addWidget(tarjeta)