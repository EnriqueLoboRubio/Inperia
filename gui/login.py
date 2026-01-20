from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QGraphicsOpacityEffect,
    QApplication 
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QParallelAnimationGroup, QEasingCurve, QPropertyAnimation, QRect, QTimer
from db.db import crear_bd, agregar_usuario, verificar_login, eliminar_usuario, encontrar_usuario
import re

#crear_bd()
#agregar_usuario("usuario1", "a@gmail.com", "1234", "usuario")
#agregar_usuario("profesional1", "b@gmail.com", "1234", "profesional")
#agregar_usuario("1", "1", "1", "usuario")
#agregar_usuario("2", "2", "2", "profesional")

class VentanaLogin(QMainWindow):

    def __init__(self):
        super().__init__()  
        self.setup_window()
        self.ANIMATION_DURATION = 250 #duracion para animacion de deslizador
        self.initUI()
        self.tipo_pantalla = "usuario" #pantalla inicial
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
        pixmap = QPixmap("assets/inicio_usuario.jpg")
        self.izq.setPixmap(pixmap)
        self.izq.setAlignment(Qt.AlignCenter)
        self.izq.setScaledContents(True)
        self.izq.setMaximumSize(800, 1000) 
        
        # Overlay      
        self.texto_over = QLabel("INPERIA\nINTERNO", self.izq)
        self.texto_over.setFont(QFont("Arial", 32, QFont.Bold))
        self.texto_over.setStyleSheet("""
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
        """)
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
        icono_usuario = QIcon("assets/usuario.png")
        icono_profesional = QIcon("assets/profesional.png")
        
        self.boton_usuario = QPushButton(self.contenedor_botones_iconos)
        self.boton_usuario.setIcon(icono_usuario)
        self.boton_usuario.setIconSize(QSize(50, 50))
        self.boton_usuario.setFixedSize(TAM_BOTON, TAM_BOTON)
        self.boton_usuario.move(0, 0)
        self.boton_usuario.setStyleSheet("""
            QPushButton { background: transparent; border: none; padding: 10px; }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 10px; }
        """) 
                
        self.boton_profesional = QPushButton(self.contenedor_botones_iconos)
        self.boton_profesional.setIcon(icono_profesional)          
        self.boton_profesional.setIconSize(QSize(50, 50))          
        self.boton_profesional.setFixedSize(TAM_BOTON, TAM_BOTON)
        self.boton_profesional.move(TAM_BOTON + ESPACIO, 0) 
        self.boton_profesional.setStyleSheet("""
            QPushButton { background: transparent; border: none; padding: 10px; }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 10px; }
        """)

        layout_der.setContentsMargins(1, 1, 1, 1)

        # Campos de entrada
        self.input_correo = QLineEdit()
        self.input_correo.setFont(QFont("Arial", 12))
        self.input_correo.setPlaceholderText("correo@gmail.com")
        self.input_correo.setFixedHeight(40)
        self.input_correo.setStyleSheet("padding-left: 10px; border-radius: 8px;")
        self.input_correo.setFixedWidth(500)

        self.input_contraseña = QLineEdit()
        self.input_contraseña.setFont(QFont("Arial", 12))
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setPlaceholderText("************")
        self.input_contraseña.setFixedHeight(40)
        self.input_contraseña.setStyleSheet("padding-left: 10px; border-radius: 8px;")
        self.input_contraseña.setFixedWidth(500)

        label_correo = QLabel("Correo")
        label_correo.setFont(QFont("Arial", 16))
        label_correo.setFixedWidth(500)
        label_contraseña = QLabel("Contraseña")
        label_contraseña.setFont(QFont("Arial", 16))
        label_contraseña.setFixedWidth(500)

        boton_entrar = QPushButton("Entrar")
        boton_entrar.setFont(QFont("Arial", 12))
        boton_entrar.setFixedHeight(50)
        boton_entrar.setFixedWidth(200)         
        boton_entrar.setStyleSheet("background-color: #222; color: white; border-radius: 8px;")
        boton_entrar.setCursor(Qt.PointingHandCursor)  
        boton_entrar.clicked.connect(self.verificar_usuario)      

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
        self.boton_usuario.clicked.connect(self.cambiar_usuario) 

    def ajustar_indicador_inicial(self):
        self.indicador_deslizante.setGeometry(self.boton_usuario.geometry())
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
        self.boton_usuario.setStyleSheet(style_base)
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
        if self.tipo_pantalla != "usuario":    
            self.intentos_fallidos = 0
            self.input_correo.clear()
            self.input_contraseña.clear()
            self.tipo_pantalla = "usuario"            
            
            self.animacion_cambio_panel(QPixmap("assets/inicio_usuario.jpg"), "INPERIA\nINTERNO")
            self.animar_indicador(self.boton_usuario)
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

    def verificar_usuario(self):

        def validar_formato_correo(correo):
            patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
            return re.match(patron, correo) is not None
            
        correo = self.input_correo.text()
        contrasena = self.input_contraseña.text()
        usuario = encontrar_usuario(correo)
        tipo_usuario = verificar_login(correo, contrasena)

        # verificar campos rellenos
        if not correo or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")
            return
        
        # verificar formato de correo y contraseña
        if not validar_formato_correo(correo):
            QMessageBox.warning(self, "Error", "Formato del correo electrónico no válido")        
            return
        
        if usuario is not None:
            if tipo_usuario is not None:           
                if self.tipo_pantalla == tipo_usuario:
                    QMessageBox.information(self, "Inicio de sesión", f"Bienvenido, {tipo_usuario.capitalize()}")

                    if tipo_usuario == "usuario":
                        from gui.usuario_inicio import VentanaUsuario
                        self.ventana_usuario = VentanaUsuario()                    
                        self.ventana_usuario.show()                    
                        self.close()
                    else:
                        from gui.profesional_inicio import VentanaProfesional
                        self.ventana_profesional = VentanaProfesional()
                        self.ventana_profesional.show()
                        self.close()
                else:
                    QMessageBox.warning(self, "Error", f"Tipo de usuario incorrecto.")          
            else:          
                QMessageBox.warning(self, "Error", f"Usuario o contraseña incorrectos. \n Tiene {3 - self.intentos_fallidos - 1} intentos restantes.")          
                self.intentos_fallidos += 1
            if self.intentos_fallidos >= 3:
                QMessageBox.critical(self, "Cuenta suprimida", "Ha superado el número máximo de intentos. La cuenta ha sido elimnaada.\n Contacte con el administrador.")
                eliminar_usuario(correo)
                self.input_correo.clear()
                self.input_contraseña.clear()
                self.intentos_fallidos = 0
        else:
            QMessageBox.warning(self, "Error", "El usuario no existe")
            self.input_correo.clear()
            self.input_contraseña.clear()
            self.intentos_fallidos = 0