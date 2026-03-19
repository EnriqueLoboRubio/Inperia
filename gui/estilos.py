# gui/estilos.py

from unicodedata import normalize

# --- PALETA DE COLORES ---
COLOR_FONDO_APP = "#F5F5F5"
COLOR_BLANCO = "white"
COLOR_GRIS_CLARO = "#E0E0E0"
COLOR_GRIS_TEXTO = "#666666"
COLOR_AZUL_CLARO = "#76bede"
COLOR_AZUL_OSCURO = "#2196F3"
COLOR_TEXTO_NEGRO = "#000000"
COLOR_IA_MORADO = "#7B2CBF"
COLOR_IA_MORADO_2 = "#9556cc"
COLOR_IA_MORADO_HOVER = "#6A1FB0"
COLOR_IA_MORADO_SUAVE = "#EFE6F8"

def color_texto_contraste(color_hex):
    """
    Devuelve color de texto oscuro o claro segun el fondo para mantener contraste.
    """
    color = str(color_hex or "").strip().lstrip("#")
    if len(color) == 3:
        color = "".join(ch * 2 for ch in color)
    if len(color) != 6:
        return "#111111"

    try:
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
    except ValueError:
        return "#111111"

    luminancia = (0.299 * r) + (0.587 * g) + (0.114 * b)
    return "#111111" if luminancia >= 160 else "#FFFFFF"


# --- ESTRUCTURA / CONTENEDORES ---
ESTILO_FRAME_BORDE = f"""
    QFrame {{
        background-color: transparent;
        border: 2px solid {COLOR_GRIS_CLARO};
        border-radius: 12px;
    }}
"""

ESTILO_APARTADO_FRAME = """
    #apartado {
        background-color: #f0f0f0;
        border: 2px solid #E0E0E0;
        border-radius: 12px;
        padding: 10px;
    }
"""


# --- LOGIN ---
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


# --- INPUTS ---
ESTILO_INPUT = f"""
    QLineEdit, QTextEdit, QDateEdit, QTimeEdit, QComboBox {{
        background-color: {COLOR_BLANCO};
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-size: 20px;
        min-height: 30px;
        font-family: 'Arial';
    }}
    QLineEdit:focus, QTextEdit:focus, QTimeEdit:focus, QDateEdit:focus {{
        border: 1px solid {COLOR_AZUL_OSCURO};
    }}

    /* --- DATE --- */
    QDateEdit {{
            padding-left: 45px;
            background-image: url(assets/calendario.png); 
            background-repeat: no-repeat;
            background-position: left 15px center;
        }}

    /* Contenedor de boton */
    QDateEdit::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: right center;
        width: 18px;
        border: none;        
    }}

    /* Flecha abajo */
    QDateEdit::down-arrow {{
        image: url(assets/flecha_abajo.png);
        width: 18px;
        height: 18px;
    }}  

    QDateEdit::down-arrow:hover {{
        background-color: #F0F0F0;
        border-radius: 4px;
    }}     

    /* --- CALENDARIO (Tema Claro y Moderno) --- */
    QCalendarWidget {{
        background-color: white;
        border: 1px solid #DFDFDF;
        border-radius: 8px;
    }}

    /* Barra superior (Mes y Año) */
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: white;
        border-bottom: 1px solid #E0E0E0;
    }}

    /* Botones de navegación (flechas mes anterior/siguiente) */
    QCalendarWidget QToolButton {{
        color: #333333;
        background-color: transparent;
        border: none;
        margin: 5px;
        font-weight: bold;
    }}

    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: white;
    }}

    QCalendarWidget QToolButton:hover {{
        background-color: #F2F2F2;
        border-radius: 6px;
    }}

    /* Menú desplegable de meses */
    QCalendarWidget QMenu {{
        background-color: white;
        border: 1px solid #DDD;
    }}

    QCalendarWidget QMenu::item:selected {{
        background-color: #E8F0FE;
    }}    


    /* Vista de los días */
    QCalendarWidget QAbstractItemView:enabled {{
        color: #333333; /* Números de días en gris oscuro */
        background-color: white;
        selection-background-color: {COLOR_AZUL_OSCURO};
        selection-color: white;
        outline: 0;
    }}

    /* Días de la semana (lu, ma, mi...) */
    QCalendarWidget QWidget {{ 
        alternate-background-color: #F7F7F7; 
    }}

    

    /* --- TIME --- */

    QTimeEdit {{
            padding-left: 45px;
            background-image: url(assets/reloj.png); 
            background-repeat: no-repeat;
            background-position: left 15px center;
        }}    

    /* Contenedor de botones ↑ ↓ */
    QTimeEdit::up-button,
    QTimeEdit::down-button {{
        subcontrol-origin: border;
        subcontrol-position: right;
        width: 18px;
        border: none;
        background: transparent;
    }}

    /* Flecha arriba */
    QTimeEdit::up-arrow {{
        image: url(assets/flecha_arriba.png);
        width: 20px;
        height: 20px;
    }}

    /* Flecha abajo */
    QTimeEdit::down-arrow {{
        image: url(assets/flecha_abajo.png);
        width: 20px;
        height: 20px;
    }}    

    /* Botón de Arriba */
    QTimeEdit::up-button {{
        subcontrol-origin: border;
        subcontrol-position: top right; 
        width: 30px;
        height: 20px;
        border: none;
        background: transparent;
        margin-right: 5px;
        margin-top: 2px;
    }}

    /* Botón de Abajo */
    QTimeEdit::down-button {{
        subcontrol-origin: border;
        subcontrol-position: bottom right; 
        width: 30px;
        height: 20px;
        border: none;
        background: transparent;
        margin-right: 5px;
        margin-bottom: 2px;
    }}

    QTimeEdit::up-arrow {{
        image: url(assets/flecha_arriba.png);
        width: 16px;
        height: 16px;
    }}

    QTimeEdit::down-arrow {{
        image: url(assets/flecha_abajo.png);
        width: 16px;
        height: 16px;
    }}
   
    QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {{
        background-color: #F0F0F0;
        border-radius: 4px;
    }}
"""

ESTILO_COMBOBOX = """
            QComboBox {
                background-color: #ECECEC;
                border: 1px solid #BEBEBE;
                border-radius: 20px;
                padding: 0 14px;
                font-size: 11pt;
                color: #555555;
            }
            QComboBox::drop-down {
                width: 28px;
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: url(assets/flecha_abajo.png);
                width: 14px;
                height: 14px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                selection-background-color: #2B2A2A;
                selection-color: white;
                background-color: white;
            }
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
                font-family: 'Arial';
                font-size: 10pt;
            }
            QPushButton:hover { 
                background-color: rgba(71, 70, 70, 0.7); 
            }
            QPushButton:disabled { background-color: #E0E0E0; opacity: 0.5; }
        """

ESTILO_BOTON_TARJETA = """
            QPushButton {
                background-color: #B0B0B0; 
                border: none;
                border-radius: 22px;
                font-family: 'Arial';
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
                font-family: 'Arial';
            }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); }
            QPushButton:disabled { background-color: #E0E0E0; opacity: 0.5; }
        """

ESTILO_BOTON_GRABAR = """
            QPushButton { 
                background: #FFFFFF; 
                border: 2px solid #D32F2F;
                border-radius: 25px;
                font-family: 'Arial';
            }
            QPushButton:hover { background-color: #FFEBEE; }
            QPushButton[grabando="true"] { 
                background-color: #D32F2F; 
                border: none;
            }
        """

ESTILO_BOTON_ERROR = """
            QPushButton { 
                background-color: black; 
                color: white; 
                border-radius: 10px; 
                padding: 8px 20px;
                font-family: 'Arial';              
                font-size: 9pt;
            }
            QPushButton:hover { background-color: #333; }
        """

ESTILO_BOTON_PERFIL =  """
            
            QLabel, QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 26px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #333333; }
        """

ESTILO_BOTON_SOLICITUD = """
            QPushButton {
                color: white;
                border: none;
                padding: 6px 14px;
                text-align: center;
                background-color: #2B2A2A;
                border-radius: 10px;
                font-family: 'Arial';
                font-size: 10pt;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #464545; }
            """

ESTILO_BOTON_IA = f"""
            QPushButton {{
                color: white;
                border: none;
                padding: 6px 14px;
                text-align: center;
                background-color: {COLOR_IA_MORADO};
                border-radius: 10px;
                font-family: 'Arial';
                font-size: 10pt;
                font-weight: 600;
            }}
            QPushButton:hover {{ background-color: {COLOR_IA_MORADO_HOVER}; }}
            QPushButton:disabled {{
                background-color: #CDB8DF;
                color: #F7F2FB;
            }}
            """


# --- TEXTOS Y ETIQUETAS ---
ESTILO_TITULO_PASO_ENCA = """
    QLabel {
    font-family: 'Arial';
    font-size: 18pt; 
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_DES_PASO_ENCA = """
    QLabel {
    font-family: 'Arial';
    color: #666;    
    font-size: 18px; 
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_SUBTITULO_PASO_ENCA = """
    QLabel {
    font-family: 'Arial';
    color: #666;
    font-size: 16px;
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_SUBTITULO_SOLICITUD = """
    QLabel {
    font-family: 'Arial';
    color: #666;
    font-size: 13pt;
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_TITULO_PASO = """
    QLabel {
    font-family: 'Arial';
    font-size: 14pt; 
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_SUBTITULO_PASO = """
    QLabel {
    font-family: 'Arial';
    color: #999
    font-size: 12pt;    
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_TITULO_APARTADO = """
    QLabel {
    font-family: 'Arial';
    font-size: 20px; 
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_TITULO_APARTADO_SOLICITUD = """
    QLabel {
    font-family: 'Arial';
    font-size: 14pt; 
    font-weight: bold; 
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_TITULO_PERMISO = """
    QLabel {
    font-family: 'Arial';
    font-size: 10pt;  
    font-weight: bold;   
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_SUBTITULO_PERMISO = """
    QLabel {
    color: #666;
    font-family: 'Arial';
    font-size: 8pt;    
    border: none; 
    background-color: transparent;
    }
"""

ESTILO_TITULO_DETALLE_SOLICITUD = "color: #9E9E9E; font-size: 12pt; font-weight: 500;"
ESTILO_DATO_PRINCIPAL_SOLICITUD = "color: black; font-size: 11pt; font-weight: bold;"
ESTILO_DATO_SECUNDARIO_SOLICITUD = "color: #757575; font-size: 10pt; font-weight: 500;"

ESTILO_TITULO_DETALLE_PERFIL = "color: #9A9A9A; font-size: 10pt; font-weight: 500;"
ESTILO_DATO_PERFIL = "color: #6A6A6A; font-size: 12pt; font-weight: 500;"
ESTILO_DATO_SECUNDARIO_PERFIL = "color: #808080; font-size: 10pt; font-weight: 500;"  


ESTILO_TEXTO = "color: black; font-size: 20px;"

ESTILO_CHECKBOX = """
    QCheckBox{
        font-family: 'Arial';
        font-size: 20px;
        spacing: 8px;
        background-color: transparent;
    }

"""


# --- PASOS / ESTADOS DE SOLICITUD ---
ESTILO_CIRCULO_ACTUAL = """
    QLabel {
            background-color: #000;
            color: #FFF;
            border-radius: 30px;
            font-weight: bold;
            font-size: 12pt;
            font-family: 'Arial';
        }
"""

ESTILO_CIRCULO_COMPLETADO = """
    QLabel {
            background-color: #4CAF50;
            color: #FFF;
            border-radius: 30px;
            font-weight: bold;
            font-size: 12pt;
            font-family: 'Arial';
        }
"""

ESTILO_CIRCULO_INACTIVO = """
    QLabel {
            background-color: #E0E0E0;
            color: #666;
            border-radius: 30px;
            font-weight: bold;
            font-size: 12pt;
            font-family: 'Arial';
        }
"""

ESTILO_ESTADO = """
    QLabel {
        background-color: #D3D3D3;
        color: #1A1A1A;          
        border-radius: 15px;       
        padding: 4px 12px;         
        border: none;         
        font-weight: 500;        
        font-size: 8pt;
    }
"""

COLOR_RIESGO = {
    "Riesgo muy bajo": "#DFF3C8",
    "Riesgo bajo": "#CBE8B5",
    "Riesgo normal": "#F4E29A",
    "Riesgo elevado": "#F2C1C1",
    "Riesgo bastante elevado": "#EEA8A8",
    "Riesgo muy elevado": "#E98E8E",
    "Riesgo maximo": "#D77272",
}

ESTADOS_SOLICITUD_COLOR = {
    "iniciada": ("Iniciada", "#D6EBFA"),
    "pendiente": ("Pendiente", "#F4E29A"),
    "aceptada": ("Aceptada", "#CBE8B5"),
    "rechazada": ("Rechazada", "#F2C1C1"),
    "cancelada": ("Cancelada", "#E0E0E0"),
}

ESTADOS_PREGUNTA_IA_COLOR = {
    "sin_analizar": ESTADOS_SOLICITUD_COLOR["cancelada"][1],
    "analizando": ESTADOS_SOLICITUD_COLOR["pendiente"][1],
    "analizada": ESTADOS_SOLICITUD_COLOR["aceptada"][1],
    "error": ESTADOS_SOLICITUD_COLOR["rechazada"][1],
}

ESTADOS_ENTREVISTA_IA_COLOR = {
    "sin analizar": ("Sin analizar", ESTADOS_PREGUNTA_IA_COLOR["sin_analizar"]),
    "analizada": ("Analizada", ESTADOS_PREGUNTA_IA_COLOR["analizada"]),
    "en cola": ("En cola", ESTADOS_PREGUNTA_IA_COLOR["analizando"]),
    "preparando": ("Preparando", ESTADOS_PREGUNTA_IA_COLOR["analizando"]),
    "error": ("Error", ESTADOS_PREGUNTA_IA_COLOR["error"]),
    "evaluada": ("Analizada", ESTADOS_PREGUNTA_IA_COLOR["analizada"]),
    "sin evaluación": ("Sin analizar", "#EFE6F8"),
    "sin evaluacion": ("Sin analizar", ESTADOS_PREGUNTA_IA_COLOR["sin_analizar"]),
    "evaluando": ("Analizando", ESTADOS_PREGUNTA_IA_COLOR["analizando"]),
    "analizando": ("Analizando", ESTADOS_PREGUNTA_IA_COLOR["analizando"]),
    "en cola...": ("En cola", ESTADOS_PREGUNTA_IA_COLOR["analizando"]),
    "preparando analisis...": ("Preparando", ESTADOS_PREGUNTA_IA_COLOR["analizando"]),
    "análisis completado.": ("Analizada", "#D9C4F1"),
    "analisis completado.": ("Analizada", ESTADOS_PREGUNTA_IA_COLOR["analizada"]),
    "error en el análisis.": ("Error", "#F2C1C1"),
    "error en el analisis.": ("Error", ESTADOS_PREGUNTA_IA_COLOR["error"]),
}


def obtener_estado_ia_visual(estado):
    clave = normalize("NFKD", str(estado or "")).encode("ascii", "ignore").decode("ascii")
    clave = " ".join(clave.strip().lower().split())
    if not clave:
        clave = "sin evaluacion"
    if clave in ESTADOS_ENTREVISTA_IA_COLOR:
        return ESTADOS_ENTREVISTA_IA_COLOR[clave]
    return str(estado or "").strip(), "#E0E0E0"


def estilo_chip_estado(color_fondo, font_size="10pt", border_radius="10px", padding="3px 10px"):
    return (
        f"background-color: {color_fondo}; "
        f"color: {color_texto_contraste(color_fondo)}; "
        f"border-radius: {border_radius}; "
        f"padding: {padding}; "
        f"font-size: {font_size}; "
        "font-weight: 500; "
        "border: none;"
    )

# --- TARJETAS ---
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

ESTILO_NIVEL_IA = f"""
            background-color: {COLOR_IA_MORADO_SUAVE};
            border: 1.5px solid {COLOR_IA_MORADO};
            color: {COLOR_IA_MORADO};
            border-radius: 10px;
            padding: 2px 12px;
        """

ESTILO_TARJETA_PERMISO_SEL = """
                QWidget {
                    background-color: #E3F2FD;
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                }
                QLabel { background: transparent; border: none; }
"""

ESTILO_TARJETA_PERMISO_NO ="""
                QWidget {
                    background-color: white;
                    border: 2px solid #E0E0E0;
                    border-radius: 8px;
                }
                QLabel { background: transparent; border: none; }
"""

# --- TARJETA ENTREVISTA (perfil interno/profesional) ---
ESTILO_TITULO_ENTREVISTA = "color: black; font-size: 12pt; font-weight: bold; border: none; background: transparent;"
ESTILO_FECHA_ENTREVISTA = "color: black; font-size: 10pt; font-weight: 400; border: none; background: transparent;"
ESTILO_AUTOR_ENTREVISTA = "color: #757575; font-size: 9pt; font-weight: 500; border: none; background: transparent;"
ESTILO_COMENTARIO_ENTREVISTA = "color: #8A8A8A; font-size: 11pt; font-weight: 600; border: none; background: transparent;"
ESTILO_PUNTUACION_ENTREVISTA = "color: #757575; font-size: 11pt; font-weight: 600; border: none; background: transparent;"


# --- SCROLL / SLIDER ---
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


# --- VENTANAS / DIALOGOS ---
ESTILO_VENTANA_DETALLE ="""
    QFrame#FondoDetalle {
        background-color: #E0E0E0;
        border: 2px solid #444444;
        border-radius: 15px;
    }
    QLabel {
        border: none;
        background: transparent;
        color: #333;
    }
"""

ESTILO_DIALOGO_ERROR = """
    QDialog {
        background-color: transparent;
    }
    QFrame#FondoDialogo {
        background-color: white;
        border: 2px solid #333;
        border-radius: 15px;
    }
    QLabel#TituloError {
        font-family: 'Arial';
        font-size: 14pt;
        font-weight: bold;
        color: #D32F2F;
        margin-bottom: 0px;
        background-color: white;
    }
    QLabel#TextoError {
        font-family: 'Arial';
        font-size: 10pt;
        color: #333333;
        margin-top: 0px;
        background-color: white;
    }
"""

# --- VENTANA DE LISTA DE SOLICITUDES ---
ESTILO_NOMBRE_INTERNO = "color: black; font-size: 20px; font-weight: bold;"

ESTILO_NUM_RC = "color: #666666; font-size: 11pt;"

