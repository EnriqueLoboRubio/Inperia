from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QGraphicsOpacityEffect 
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QParallelAnimationGroup, QEasingCurve, QPropertyAnimation, QRect, QTimer, pyqtSignal
from gui.estilos import *

class VentanaLogin(QMainWindow):

    # Señal de login exitoso
    signal_solicitar_login = pyqtSignal(str, str, str)  # correo, rol, tipo de pantalla actual

    def __init__(self):
        super().__init__()  
        self.setup_window()
        self.ANIMATION_DURATION = 250 #duracion para animacion de deslizador
        self.initUI()
        self.tipo_pantalla = "interno" #pantalla inicial
        self.intentos_fallidos = 0
        
        QTimer.singleShot(0, self.ajustar_indicador_inicial) 

    def setup_window(self):
        self.setWindowTitle("INPERIA")
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.setMinimumSize(1200,700)
        self.showMaximized()

    def initUI(self):        
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout()
        central.setLayout(layout_principal)    

        #----Panel Izquierdo----
        self.izq = QLabel()
        pixmap = QPixmap("assets/inicio_interno.jpg")
        self.izq.setPixmap(pixmap)
        self.izq.setAlignment(Qt.AlignCenter)
        self.izq.setScaledContents(True)
        self.izq.setMaximumSize(800, 1000) 
        
        # Overlay      
        self.texto_over = QLabel("INPERIA\nINTERNO", self.izq)
        self.texto_over.setFont(QFont("Arial", 32, QFont.Bold))
        self.texto_over.setStyleSheet(ESTILO_TEXTO_LOGIN)
        self.texto_over.setAlignment(Qt.AlignCenter)
        self.texto_over.setFixedSize(300, 100)
        self.texto_over.move(255,350)             

        #----Panel Derecho----
        der = QWidget()
        layout_der = QVBoxLayout()       
        layout_der.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        der.setLayout(layout_der)

        # Contenedor principal para los iconos
        self.contenedor_botones_iconos = QWidget()
        layout_iconos = QHBoxLayout()      
        layout_iconos.addStretch() 
        layout_iconos.addWidget(self.contenedor_botones_iconos)         
        
        layout_der.addLayout(layout_iconos)
        layout_der.addSpacing(200) # Espacio entre los iconos y el formulario

        TAM_BOTON = 70
        ESPACIO = 30
        ANCHURA = TAM_BOTON * 2 + ESPACIO
        ALTURA = TAM_BOTON
        self.contenedor_botones_iconos.setFixedSize(ANCHURA, ALTURA)

        # Indicador Deslizante
        self.indicador_deslizante = QWidget(self.contenedor_botones_iconos)
        self.indicador_deslizante.setStyleSheet("background-color: rgba(128, 128, 128, 0.4); border-radius: 10px;")
        self.indicador_deslizante.setFixedSize(TAM_BOTON, TAM_BOTON)
        self.indicador_deslizante.lower() 

        # Botones
        icono_interno = QIcon("assets/interno.png")
        icono_profesional = QIcon("assets/profesional.png")
        
        self.boton_interno = QPushButton(self.contenedor_botones_iconos)
        self.boton_interno.setIcon(icono_interno)
        self.boton_interno.setIconSize(QSize(50, 50))
        self.boton_interno.setFixedSize(TAM_BOTON, TAM_BOTON)
        self.boton_interno.move(0, 0)
        self.boton_interno.setStyleSheet(BOTON_PERFIL_LOGIN) 
                
        self.boton_profesional = QPushButton(self.contenedor_botones_iconos)
        self.boton_profesional.setIcon(icono_profesional)          
        self.boton_profesional.setIconSize(QSize(50, 50))          
        self.boton_profesional.setFixedSize(TAM_BOTON, TAM_BOTON)
        self.boton_profesional.move(TAM_BOTON + ESPACIO, 0) 
        self.boton_profesional.setStyleSheet(BOTON_PERFIL_LOGIN)

        layout_der.setContentsMargins(1, 1, 1, 1)

        # Campos de entrada
        self.input_correo = QLineEdit()        
        self.input_correo.setPlaceholderText("correo@gmail.com")
        self.input_correo.setFixedHeight(40)
        self.input_correo.setStyleSheet(ESTILO_INPUT)
        self.input_correo.setFixedWidth(500)

        self.input_contraseña = QLineEdit()       
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setPlaceholderText("************")
        self.input_contraseña.setFixedHeight(40)
        self.input_contraseña.setStyleSheet(ESTILO_INPUT)
        self.input_contraseña.setFixedWidth(500)

        label_correo = QLabel("Correo")
        label_correo.setFont(QFont("Arial", 16))
        label_correo.setFixedWidth(500)
        label_contraseña = QLabel("Contraseña")
        label_contraseña.setFont(QFont("Arial", 16))
        label_contraseña.setFixedWidth(500)

        boton_entrar = QPushButton("Entrar")        
        boton_entrar.setFixedHeight(50)
        boton_entrar.setFixedWidth(200)         
        boton_entrar.setStyleSheet(ESTILO_BOTON_NEGRO)
        boton_entrar.setCursor(Qt.PointingHandCursor)  
        boton_entrar.clicked.connect(self.click_entrar)      

        formulario = QVBoxLayout()
        formulario.setSpacing(20) 
        
        formulario.addWidget(label_correo, alignment=Qt.AlignCenter)
        formulario.addWidget(self.input_correo, alignment=Qt.AlignCenter)
        formulario.addWidget(label_contraseña, alignment=Qt.AlignCenter)
        formulario.addWidget(self.input_contraseña, alignment=Qt.AlignCenter)
        formulario.addWidget(boton_entrar, alignment=Qt.AlignCenter)
        
        contenedor_formulario = QWidget()
        contenedor_formulario.setLayout(formulario)
        contenedor_formulario.setMaximumWidth(1100)
        contenedor_formulario.setMinimumWidth(1050)
            
        layout_der.addWidget(contenedor_formulario, alignment=Qt.AlignHCenter)                
        layout_der.addStretch(1) 

        layout_principal.addWidget(self.izq, 1)
        layout_principal.addWidget(der, 2)
        
        self.boton_profesional.clicked.connect(self.cambiar_profesional)
        self.boton_interno.clicked.connect(self.cambiar_usuario) 

    def ajustar_indicador_inicial(self):
        self.indicador_deslizante.setGeometry(self.boton_interno.geometry())
        self.indicador_deslizante.raise_()
        self.indicador_deslizante.lower()

    def animar_indicador(self, boton_destino: QPushButton):
        
        destino_rect = boton_destino.geometry()
        
        self.animacion_indicador = QPropertyAnimation(self.indicador_deslizante, b"geometry")
        self.animacion_indicador.setDuration(self.ANIMATION_DURATION)
        self.animacion_indicador.setEndValue(QRect(destino_rect))
        self.animacion_indicador.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_indicador.start()

    def actualizar_estilos_botones(self, es_usuario):
        style_base = """
            QPushButton { background: transparent; border: none; padding: 10px; }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 10px; }
        """
        self.boton_interno.setStyleSheet(style_base)
        self.boton_profesional.setStyleSheet(style_base)


    def cambiar_profesional(self):
        if self.tipo_pantalla != "profesional":
            self.intentos_fallidos = 0
            self.input_correo.clear()
            self.input_contraseña.clear()             
            self.tipo_pantalla = "profesional"             
            
            self.animacion_cambio_panel(QPixmap("assets/inicio_profesional.jpg"), "INPERIA\nPROFESIONAL")
            self.animar_indicador(self.boton_profesional)
            self.actualizar_estilos_botones(es_usuario=False)
            
    def cambiar_usuario(self):  
        if self.tipo_pantalla != "interno":    
            self.intentos_fallidos = 0
            self.input_correo.clear()
            self.input_contraseña.clear()
            self.tipo_pantalla = "interno"            
            
            self.animacion_cambio_panel(QPixmap("assets/inicio_interno.jpg"), "INPERIA\nINTERNO")
            self.animar_indicador(self.boton_interno)
            self.actualizar_estilos_botones(es_usuario=True)

    def animacion_cambio_panel(self, nuevo_pixmap, nuevo_texto):
            
            #Crear efectos de opacidad
            efecto_img = QGraphicsOpacityEffect()
            self.izq.setGraphicsEffect(efecto_img)

            efecto_txt = QGraphicsOpacityEffect()
            self.texto_over.setGraphicsEffect(efecto_txt)

            #Animación desvacenimiento
            animacion_salida_img = QPropertyAnimation(efecto_img, b"opacity")
            animacion_salida_img.setDuration(300)
            animacion_salida_img.setStartValue(1.0)
            animacion_salida_img.setEndValue(0.0)
            animacion_salida_img.setEasingCurve(QEasingCurve.InOutQuad)


            animacion_salida_txt = QPropertyAnimation(efecto_txt, b"opacity")
            animacion_salida_txt.setDuration(300)
            animacion_salida_txt.setStartValue(1.0)
            animacion_salida_txt.setEndValue(0.0)
            animacion_salida_txt.setEasingCurve(QEasingCurve.InOutQuad)  

            # Grupo de animaciones de salida
            self.grupo_salida = QParallelAnimationGroup()
            self.grupo_salida.addAnimation(animacion_salida_img)
            self.grupo_salida.addAnimation(animacion_salida_txt)                 
            
            # Cuando termina la animación de salida, cambiar contenido y animar entrada
            def cambiar_y_animar_entrada():
                # Cambiar el contenido
                self.izq.setPixmap(nuevo_pixmap)
                self.texto_over.setText(nuevo_texto)
                
                # Animación de entrada
                animacion_entrada_img = QPropertyAnimation(efecto_img, b"opacity")
                animacion_entrada_img.setDuration(300)
                animacion_entrada_img.setStartValue(0.0)
                animacion_entrada_img.setEndValue(1.0)
                animacion_entrada_img.setEasingCurve(QEasingCurve.InOutQuad)

                animacion_entrada_txt = QPropertyAnimation(efecto_txt, b"opacity")
                animacion_entrada_txt.setDuration(300)
                animacion_entrada_txt.setStartValue(0.0)
                animacion_entrada_txt.setEndValue(1.0)
                animacion_entrada_txt.setEasingCurve(QEasingCurve.InOutQuad)
                
                # Grupo de animaciones de entrada
                self.grupo_entrada = QParallelAnimationGroup()
                self.grupo_entrada.addAnimation(animacion_entrada_img)
                self.grupo_entrada.addAnimation(animacion_entrada_txt)
                
                # Limpiar efectos cuando termine la animación de entrada
                def limpiar_efectos():
                    self.izq.setGraphicsEffect(None)
                    self.texto_over.setGraphicsEffect(None)
                
                self.grupo_entrada.finished.connect(limpiar_efectos)
                self.grupo_entrada.start()
            
            self.grupo_salida.finished.connect(cambiar_y_animar_entrada)
            self.grupo_salida.start()         

    def click_entrar(self):
        """
        Recoge los datos y manda señal al controlador de login
        """
        correo = self.input_correo.text().strip()
        contrasena = self.input_contraseña.text().strip()
        tipo = "interno" if self.tipo_pantalla == "interno" else "profesional"
        
        self.signal_solicitar_login.emit(correo, contrasena, self.tipo_pantalla)

    def mostrar_mensaje_error(self, mensaje):
        if "CRITICO" in mensaje:
            QMessageBox.critical(self, "Cuenta Suprimida", mensaje.replace("CRITICO: ", ""))
            self.input_correo.clear()
            self.input_contraseña.clear()
        else:
            QMessageBox.warning(self, "Error de acceso", mensaje)
            if "existe" in mensaje:
                self.input_correo.clear()
                self.input_contraseña.clear()
