from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

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
        pixmap = QPixmap("assets/error.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
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
        pixmap = QPixmap("assets/warning.png").scaled(
            30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        lbl_icono.setPixmap(pixmap)

        titulo = QLabel("Cerrar sesión")
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