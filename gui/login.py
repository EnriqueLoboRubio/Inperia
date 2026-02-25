from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QGraphicsOpacityEffect, QFrame, QDialog,
    QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QParallelAnimationGroup, QEasingCurve, QPropertyAnimation, QRect, QTimer, pyqtSignal, QEvent
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
        # Evita mostrar la ventana antes de construir la UI completa.
        self.setWindowState(self.windowState() | Qt.WindowMaximized)

    def initUI(self):        
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        central.setLayout(layout_principal)    

        #----Panel Izquierdo----
        self.izq = QLabel()
        pixmap = QPixmap("assets/inicio_interno.jpg")
        self.izq.setPixmap(pixmap)
        self.izq.setAlignment(Qt.AlignCenter)
        self.izq.setScaledContents(True)
        self.izq.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.izq.installEventFilter(self)
        
        # Overlay      
        self.texto_over = QLabel("INPERIA\nINTERNO", self.izq)
        self.texto_over.setFont(QFont("Arial", 25, QFont.Bold))
        self.texto_over.setAlignment(Qt.AlignCenter)
        self.texto_over.setFixedSize(440, 165)
        self._aplicar_estilo_overlay(es_profesional=False)

        sombra = QGraphicsDropShadowEffect(self.texto_over)
        sombra.setBlurRadius(52)
        sombra.setOffset(0, 12)
        sombra.setColor(QColor(0, 0, 0, 130))
        self.texto_over.setGraphicsEffect(sombra)
        self._posicionar_texto_overlay()

        #----Panel Derecho----
        der = QWidget()
        layout_der = QVBoxLayout()       
        layout_der.setContentsMargins(0, 0, 0, 0)
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

    def _posicionar_texto_overlay(self):
        if not hasattr(self, "izq") or not hasattr(self, "texto_over"):
            return
        x = (self.izq.width() - self.texto_over.width()) // 2
        y = (self.izq.height() - self.texto_over.height()) // 2
        self.texto_over.move(max(0, x), max(0, y))

    def _aplicar_estilo_overlay(self, es_profesional: bool):
        if es_profesional:
            self.texto_over.setStyleSheet("""
                QLabel {
                    color: #111111;
                    background-color: rgba(105, 105, 105, 182);
                    border: 1px solid rgba(255, 255, 255, 45);
                    border-radius: 22px;
                    padding: 16px 28px;
                }
            """)
        else:
            self.texto_over.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: rgba(78, 78, 78, 176);
                    border: 1px solid rgba(255, 255, 255, 38);
                    border-radius: 22px;
                    padding: 16px 28px;
                }
            """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._posicionar_texto_overlay()

    def showEvent(self, event):
        super().showEvent(event)
        # Recalcula cuando la ventana ya está mostrada y el layout aplicado.
        QTimer.singleShot(0, self._posicionar_texto_overlay)
        QTimer.singleShot(0, self.ajustar_indicador_inicial)
        QTimer.singleShot(60, self._posicionar_texto_overlay)

    def eventFilter(self, obj, event):
        if obj is self.izq and event.type() in (QEvent.Resize, QEvent.Show, QEvent.Move):
            QTimer.singleShot(0, self._posicionar_texto_overlay)
        return super().eventFilter(obj, event)

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
            
            self.animacion_cambio_panel(
                QPixmap("assets/inicio_profesional.jpg"),
                "INPERIA\nPROFESIONAL",
                es_profesional=True
            )
            self.animar_indicador(self.boton_profesional)
            self.actualizar_estilos_botones(es_usuario=False)
            
    def cambiar_usuario(self):  
        if self.tipo_pantalla != "interno":    
            self.intentos_fallidos = 0
            self.input_correo.clear()
            self.input_contraseña.clear()
            self.tipo_pantalla = "interno"            
            
            self.animacion_cambio_panel(
                QPixmap("assets/inicio_interno.jpg"),
                "INPERIA\nINTERNO",
                es_profesional=False
            )
            self.animar_indicador(self.boton_interno)
            self.actualizar_estilos_botones(es_usuario=True)

    def animacion_cambio_panel(self, nuevo_pixmap, nuevo_texto, es_profesional):
        # Evitar solape de animaciones/effects al cambiar rápido de perfil.
        if hasattr(self, "grupo_salida") and self.grupo_salida.state() != self.grupo_salida.Stopped:
            self.grupo_salida.stop()
        if hasattr(self, "grupo_entrada") and self.grupo_entrada.state() != self.grupo_entrada.Stopped:
            self.grupo_entrada.stop()

        self.izq.setGraphicsEffect(None)
        self.texto_over.setGraphicsEffect(None)

        # Solo animamos el panel izquierdo. El texto overlay (hijo) se desvanece junto al panel.
        efecto_img = QGraphicsOpacityEffect()
        self.izq.setGraphicsEffect(efecto_img)

        animacion_salida_img = QPropertyAnimation(efecto_img, b"opacity")
        animacion_salida_img.setDuration(360)
        animacion_salida_img.setStartValue(1.0)
        animacion_salida_img.setEndValue(0.0)
        animacion_salida_img.setEasingCurve(QEasingCurve.InOutCubic)

        self.grupo_salida = QParallelAnimationGroup()
        self.grupo_salida.addAnimation(animacion_salida_img)

        def cambiar_y_animar_entrada():
            # Cambiar todo junto para que no haya desfase visual entre imagen/titulo/estilo.
            self._aplicar_estilo_overlay(es_profesional=es_profesional)
            self.izq.setPixmap(nuevo_pixmap)
            self.texto_over.setText(nuevo_texto)
            self._posicionar_texto_overlay()

            animacion_entrada_img = QPropertyAnimation(efecto_img, b"opacity")
            animacion_entrada_img.setDuration(420)
            animacion_entrada_img.setStartValue(0.0)
            animacion_entrada_img.setEndValue(1.0)
            animacion_entrada_img.setEasingCurve(QEasingCurve.InOutCubic)

            self.grupo_entrada = QParallelAnimationGroup()
            self.grupo_entrada.addAnimation(animacion_entrada_img)

            def limpiar_efectos():
                self.izq.setGraphicsEffect(None)

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
        dialogo = QDialog(self)
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
