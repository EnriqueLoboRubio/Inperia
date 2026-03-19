from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

from gui.estilos import *


class Mensajes:
    def __init__(self, parent=None):
        self.parent = parent

    def mostrar_advertencia(self, tit, mensaje):
        """
        Crea un diálogo personalizado para tener control total del espaciado
        """
        dialogo = QDialog(self.parent)
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


        titulo = QLabel(tit)
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

    def mostrar_mensaje(self, titulo, mensaje):

        dialogo = QDialog(self.parent)
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
        pixmap = QPixmap("assets/info.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
        lbl_icono.setPixmap(pixmap) 
        lbl_icono.setFixedSize(30, 30)
        lbl_icono.setStyleSheet("background: transparent; border: none;")

        titulo = QLabel(titulo)
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

    def mostrar_confirmacion(self, titulo, mensaje):
        dialogo = QDialog(self.parent)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        dialogo.setModal(True)

        # Layout principal
        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)

        # --- FONDO ---
        fondo = QFrame()
        fondo.setObjectName("FondoDialogo")
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)  # puedes usar otro estilo si quieres

        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(10)

        # --- CABECERA ---
        layout_cabecera = QHBoxLayout()

        lbl_icono = QLabel()
        pixmap = QPixmap("assets/info.png").scaled(
            30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        lbl_icono.setPixmap(pixmap)

        titulo = QLabel(titulo)
        titulo.setObjectName("TituloError")

        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()

        # --- MENSAJE ---
        lbl_mensaje = QLabel(mensaje)
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

    def mostrar_decision_eliminacion(self, titulo, mensaje, texto_confirmar, texto_secundario):
        dialogo = QDialog(self.parent)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        dialogo.setModal(True)

        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setObjectName("FondoDialogo")
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)

        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(10)

        layout_cabecera = QHBoxLayout()

        lbl_icono = QLabel()
        pixmap = QPixmap("assets/info.png").scaled(
            30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        lbl_icono.setPixmap(pixmap)

        titulo_lbl = QLabel(titulo)
        titulo_lbl.setObjectName("TituloError")

        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo_lbl)
        layout_cabecera.addStretch()

        lbl_mensaje = QLabel(mensaje)
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(340)

        btn_cancelar = QPushButton("Cancelar")
        btn_secundario = QPushButton(texto_secundario)
        btn_confirmar = QPushButton(texto_confirmar)

        for boton in (btn_cancelar, btn_secundario, btn_confirmar):
            boton.setCursor(Qt.PointingHandCursor)

        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #777; }
        """)

        btn_secundario.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #333; }
        """)

        btn_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #792A24;
                color: white;
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C03930; }
        """)

        btn_cancelar.clicked.connect(lambda: dialogo.done(0))
        btn_secundario.clicked.connect(lambda: dialogo.done(2))
        btn_confirmar.clicked.connect(lambda: dialogo.done(1))

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_secundario)
        layout_botones.addWidget(btn_confirmar)

        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(10)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(20)
        layout_interno.addLayout(layout_botones)

        layout_main.addWidget(fondo)

        resultado = dialogo.exec_()
        if resultado == 1:
            return "confirmar"
        if resultado == 2:
            return "secundario"
        return "cancelar"
    
    def mostrar_mensaje_error_login(self, mensaje):
        if "CRITICO" in mensaje:        
            imagen = "assets/borrado.png"
            tit = "Cuenta eliminada"
            self.input_correo.clear()
            self.input_contraseña.clear()
        else:            
            imagen = "assets/error.png"
            tit = "Atención"
            if "existe" in mensaje:
                self.input_correo.clear()
                self.input_contraseña.clear()
        
        dialogo = QDialog(self.parent)
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
                 
        pixmap = QPixmap(imagen).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        lbl_icono.setPixmap(pixmap) 
        lbl_icono.setFixedSize(30, 30)
        lbl_icono.setStyleSheet("background: transparent; border: none;")


        titulo = QLabel(tit)
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
        boton.setStyleSheet(ESTILO_BOTON_ERROR)
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

    # MENSAJES DE SOLICITUD
    def mostrar_confirmacion_solicitud(self, datos):
        """
        Muestra un diálogo de confirmación personalizado.
        Devuelve True si el usuario acepta, False si cancela.
        """
        dialogo = QDialog(self.parent)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        dialogo.setFixedSize(520, 420)
        
        # --- LAYOUT PRINCIPAL (Contenedor invisible) ---
        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)
        
        # --- MARCO DE FONDO (La "tarjeta" visible) ---
        fondo = QFrame()
        fondo.setObjectName("FondoDetalle")
        fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        
        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(30, 30, 30, 30)
        
        # ---CABECERA ---
        cabecera = QHBoxLayout()
        
        # Icono
        icono = QLabel()
        try:
            pixmap = QPixmap("assets/info.png").scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icono.setPixmap(pixmap)
        except:
            icono.setText("ℹ️")
        
        cabecera.addWidget(icono, alignment=Qt.AlignTop)
        
        # Títulos
        textos_cabecera = QVBoxLayout()
        titulo = QLabel("¿Desea enviar esta solicitud?")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: black;")
        
        textos_cabecera.addWidget(titulo)
        cabecera.addLayout(textos_cabecera)
        cabecera.addStretch()
        
        layout_interno.addLayout(cabecera)
        layout_interno.addSpacing(15)
        
        # --- 2. CUERPO (Datos) ---
        cuerpo = QVBoxLayout()

        def crear_fila(label_text, valor):
            fila = QHBoxLayout()
            l1 = QLabel(f"{label_text}:")
            l1.setFont(QFont("Arial", 10, QFont.Bold))
            l1.setStyleSheet("color: #333;")
            
            l2 = QLabel(str(valor))
            l2.setStyleSheet("color: #555;")
            
            fila.addWidget(l1)
            fila.addWidget(l2)
            fila.addStretch()
            cuerpo.addLayout(fila)

        # Insertamos los datos usando .get() para seguridad
        crear_fila("Tipo de Permiso", datos.get("tipo", "-"))
        crear_fila("Urgencia", datos.get("urgencia", "-"))
        crear_fila("Fecha Inicio", datos.get("fecha_inicio", "-"))
        crear_fila("Fecha Fin", datos.get("fecha_fin", "-"))
        crear_fila("Destino", datos.get("destino", "-"))
        crear_fila("Contacto Emergencia", datos.get("contacto", "-"))
        crear_fila("Teléfono", datos.get("telefono", "-"))
        
        layout_interno.addLayout(cuerpo)
        layout_interno.addStretch()
        
        # --- 3. BOTONES ---
        botones = QHBoxLayout()
        botones.addStretch()
        
        # Estilo común para botones
        estilo_btn = """
            QPushButton {
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """

        btn_no = QPushButton("No")
        btn_no.setFixedSize(90, 35)
        btn_no.setCursor(Qt.PointingHandCursor)
        btn_no.setStyleSheet(estilo_btn + """
            QPushButton { background-color: #333; }
            QPushButton:hover { background-color: #555; }
        """)
        btn_no.clicked.connect(dialogo.reject) # Devuelve False (0)

        btn_si = QPushButton("Sí, enviar")
        btn_si.setFixedSize(120, 35)
        btn_si.setCursor(Qt.PointingHandCursor)
        btn_si.setStyleSheet(estilo_btn + """
            QPushButton { background-color: #792A24; }
            QPushButton:hover { background-color: #C03930; }
        """)
        btn_si.clicked.connect(dialogo.accept) # Devuelve True (1)

        botones.addWidget(btn_no)
        botones.addSpacing(10)
        botones.addWidget(btn_si)
        
        layout_interno.addLayout(botones)
        
        # Añadir el fondo al diálogo
        layout_main.addWidget(fondo)
        
        # --- EJECUCIÓN ---
        # exec_() bloquea la ventana hasta que se cierre.
        # Devuelve QDialog.Accepted (1) si pulsaron "Sí" o QDialog.Rejected (0) si "No"
        resultado = dialogo.exec_()
        
        return resultado == QDialog.Accepted
