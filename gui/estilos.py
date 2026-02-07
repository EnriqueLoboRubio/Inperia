# gui/estilos.py

# --- PALETA DE COLORES ---
COLOR_FONDO_APP = "#F5F5F5"
COLOR_BLANCO = "white"
COLOR_GRIS_CLARO = "#E0E0E0"
COLOR_GRIS_TEXTO = "#666666"
COLOR_AZUL_CLARO = "#76bede"
COLOR_AZUL_OSCURO = "#2196F3"
COLOR_TEXTO_NEGRO = "#000000"

# ----- ESTILOS COMUNES -----

# --- LOGIN ---

#Estilo para Qlabel login
ESTILO_TEXTO_LOGIN = """
    QLabel {
        background-color: rgba(0, 0, 0, 0.4);
        color: white;
        font-size: 32px;
        font-weight: bold;
        border-radius: 18px;
        padding: 18px;
        padding-top: 10px;
        padding-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
"""

BOTON_PERFIL_LOGIN = """
    QPushButton { background: transparent; border: none; padding: 10px; }
    QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 10px; }
"""

# Estilo para contenedores con borde (como el encabezado y contenido)
ESTILO_FRAME_BORDE = f"""
    QFrame {{
        background-color: transparent;
        border: 2px solid {COLOR_GRIS_CLARO};
        border-radius: 12px;
    }}
"""

# Estilo para inputs
ESTILO_INPUT = f"""
    QLineEdit, QTextEdit, QDateEdit, QTimeEdit, QComboBox {{
        background-color: {COLOR_BLANCO};
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-size: 20px;
        min-height: 30px;
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 1px solid {COLOR_AZUL_OSCURO};
    }}
"""

# --- BOTONES ---
ESTILO_BOTON_NEGRO = """                                   
    QPushButton { 
        color: white; 
        border: 1px solid rgba(255, 255, 255, 0.4); 
        padding: 10px 15px; 
        text-align: center;
        background-color: black; 
        border-radius: 15px;

        font-family: 'Arial';
        font-size: 14pt;        
    }
    QPushButton:hover { 
        background-color: rgba(71, 70, 70, 0.7); 
    }
"""

ESTILO_BOTON_SIG_ATR = """                                   
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
        """

ESTILO_BOTON_TARJETA = """
            QPushButton {
                background-color: #B0B0B0; 
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #909090;
            }
"""

ESTILO_BOTON_PLAY = """
            QPushButton { 
                background: rgba(200, 200, 200, 0.6); 
                border-radius: 25px;
                padding: 10px; 
            }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); }
            QPushButton:disabled { background-color: #E0E0E0; opacity: 0.5; }
        """

ESTILO_BOTON_GRABAR = """
            QPushButton { 
                background: #FFFFFF; 
                border: 2px solid #D32F2F;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: #FFEBEE; }
            QPushButton[grabando="true"] { 
                background-color: #D32F2F; 
                border: none;
            }
        """

# --- ESTILOS DE PASOS SOLICITUD ---
#Circulo
ESTILO_CIRCULO = """
    QLabel {
            background-color: #E0E0E0;
            color: #666;
            border-radius: 30px;
            font-weight: bold;
            font-size: 20px;
        }
"""

# Título paso
ESTILO_TITULO_ = """
    font-size: 24px; 
    font-weight: bold; 
    border: none; 
    background-color: transparent;
"""

# ---  TARJETAS ---
ESTILO_TARJETA_RESUMEN = """
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
        """
ESTILO_NIVEL = """
            background-color: transparent; 
            border: 1.5px solid #808080; 
            color: #555555;
            border-radius: 10px; 
            padding: 2px 12px;
        """
# --- SCROLL ---
ESTILO_SCROLL = """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            /* barra vertical completa */
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;    
                width: 8px;            
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
            }
            /* El "mando" que se arrastra */
            QScrollBar::handle:vertical {
                background: #B0B0B0;   
                min-height: 20px;       
                border-radius: 4px;     
            }
            /* Efecto al pasar el mouse por encima del mando */
            QScrollBar::handle:vertical:hover {
                background: #909090;    
            }
            /* Ocultar las flechas de arriba y abajo */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            /* Ocultar el fondo de la pista de las flechas */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """

#SLIDER AUDIO
ESTILO_SLIDER = """
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
        """