from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QScrollArea, QFrame, QSizePolicy, QButtonGroup
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
import json, os



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
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) # contenido se ajuste al ancho
        scroll_area.setFrameShape(QFrame.NoFrame) # Sin borde
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Sin scroll horizontal
        
        scroll_content_widget = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content_widget)       
        scroll_content_layout.setAlignment(Qt.AlignTop)
        scroll_content_layout.setSpacing(20) # Espacio entre tarjetas
        scroll_content_layout.setContentsMargins(50, 20, 50, 0)

        # --- crear 10 tarjetas ---
        for i in range(1, 11):
            clave = str(i)
            datos = self.PREGUNTAS_DATA.get(clave, {})
            titulo_json = datos.get("titulo", f"Pregunta {i}")

            # crear la tarjeta
            tarjeta = self.crear_tarjeta_pregunta(i, titulo_json)
            scroll_content_layout.addWidget(tarjeta) 

        scroll_area.setWidget(scroll_content_widget)                
        
        principal_layout.addWidget(scroll_area, 1) # máximo espacio posible 

        # ------------------- 3. Botón Atrás Inferior -------------------
        boton_layout = QHBoxLayout()
        
        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setFixedSize(150, 50)
        self.boton_atras.setCursor(Qt.PointingHandCursor)
        self.boton_atras.setStyleSheet("""                                   
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
        self.boton_atras.setToolTip("Volver a la pantalla de preguntas")
        
        boton_layout.addWidget(self.boton_atras)
        boton_layout.addStretch() # botón a la izquierda

        principal_layout.addLayout(boton_layout)


    # ------------------- Funciones Auxiliares -------------------
    
    def crear_tarjeta_pregunta(self, numero, titulo): #Cambiar a  objeto pregunta
        
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

        # Layout para titulo y nivel
        top_tarjeta_layout = QHBoxLayout()                

        # Título de la pregunta
        lbl_titulo = QLabel(f"Pregunta {numero}: {titulo}")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        top_tarjeta_layout.addWidget(lbl_titulo)
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)

        top_tarjeta_layout.addStretch() # Nivel a la derecha

        # Nivel de respuesta
        lbl_nivel = QLabel("Nivel: 0")
        lbl_nivel.setFont(QFont("Arial", 11, QFont.Bold))
        lbl_nivel.setAlignment(Qt.AlignCenter)
        lbl_nivel.setStyleSheet(("""
            background-color: transparent; 
            border: 1.5px solid #808080; 
            color: #555555;
            border-radius: 10px; 
            padding: 2px 12px;
        """))        
        top_tarjeta_layout.addWidget(lbl_nivel)

        tarjeta_layout.addLayout(top_tarjeta_layout)
                
        # Contenido (Respuesta, Nivel, Análisis)        
        lbl_respuesta = QLabel("<b>Respuesta:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        # lbl_respuesta.setText(f"<b>Respuesta:</b> {datos.get('respuesta', 'Sin datos')}")
        lbl_respuesta.setFont(QFont("Arial", 11))
        lbl_respuesta.setWordWrap(True) # texto salta de línea si es muy largo
        lbl_respuesta.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_respuesta.setAlignment(Qt.AlignJustify)
        tarjeta_layout.addWidget(lbl_respuesta)

        lbl_analisis = QLabel("<b>Análisis IA:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        lbl_analisis.setFont(QFont("Arial", 11))
        lbl_analisis.setWordWrap(True) 
        lbl_analisis.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_analisis.setAlignment(Qt.AlignJustify)
        tarjeta_layout.addWidget(lbl_analisis)

        # Botón de entrar
        boton_layout = QHBoxLayout()
        boton_layout.addStretch() #icono a la derecha
               
        icono_entrar = QIcon("assets/entrar.png")

        boton_entrar = QPushButton()
        boton_entrar.setFixedSize(45, 45)
        boton_entrar.setIcon(icono_entrar)
        boton_entrar.setIconSize(QSize(25, 25))
        boton_entrar.setCursor(Qt.PointingHandCursor)
        boton_entrar.setStyleSheet("""
            QPushButton {
                background-color: #B0B0B0; 
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #909090;
            }
        """)
        boton_entrar.setToolTip(f"Ver detalles de la respuesta {numero}")
        
        #Añadir el botón al grupo
        self.grupo_botones_entrar.addButton(boton_entrar, numero)

        boton_layout.addWidget(boton_entrar)
        
        tarjeta_layout.addLayout(boton_layout)

        return tarjeta_frame