from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from gui.pantalla_bienvenida_interno import PantallaBienvenidaInterno
from gui.pantalla_preguntas import PantallaPreguntas
from gui.pantalla_resumen_profesional import PantallaResumen as PantallaResumenProfesional

class VentanaInterno(QMainWindow):
    
    # Constantes para el menú principal
    MENU_ANCHURA_CERRADO = 70
    MENU_ANCHURA_ABIERTO = 250
    COLOR_ABIERTO = "#2B2A2A"
    COLOR_CERRADO = "transparent"

    # Constantes para el menú de ajustes
    AJUSTES_ANCHURA_CERRADO = 0
    AJUSTES_ANCHURA_ABIERTO = 200
    AJUSTES_MENU_COLOR = "#3C3C3C"

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setWindowTitle("INPERIA - Interno")        
        
        # Estados iniciales del menú y submenús
        self.menu_abierto = False
        self.submenu_abierto = False # Estado del submenú de preguntas
        self.ajustes_abierto = False
        
        self.initUI()

    def setup_window(self):      
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.setMinimumSize(1200,700)
        self.showMaximized()      

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal horizontal (Menú Lateral + Contenido Principal)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ------------------- 1. Panel del Menú Lateral -------------------
        self.menu_frame = QWidget()
        self.menu_frame.setFixedWidth(self.MENU_ANCHURA_CERRADO)
        self.menu_frame.setStyleSheet(f"background-color: {self.COLOR_CERRADO};") 
        
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setContentsMargins(5, 5, 5, 5)    
        menu_layout.setSpacing(10)                
        
        # Botón Hamburguesa
        self.boton_hamburguesa = QPushButton("☰")
        self.boton_hamburguesa.setToolTip("Ver menú")
        self.boton_hamburguesa.setFixedSize(self.MENU_ANCHURA_CERRADO - 10, self.MENU_ANCHURA_CERRADO - 10) 
        self.boton_hamburguesa.setFont(QFont("Arial", 20, QFont.Bold))
        self.boton_hamburguesa.setStyleSheet("""
            QPushButton { 
                background-color: #444444; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #555555; }
        """)                                
        
        menu_layout.addWidget(self.boton_hamburguesa)
        menu_layout.addSpacing(10)

        # --- Estilos de Botones ---
        
        # Estilo base para botones del menú principal
        self.boton_estilo = """
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: left;
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: rgba(85, 85, 85, 0.5); 
            }
        """
        # Estilo para el botón de preguntas cuando está activo
        self.boton_activo_estilo = """
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: left;
                background-color: rgba(85, 85, 85, 0.5); 
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: rgba(85, 85, 85, 0.7); 
            }
        """

        # --- Botones del Menú Principal ---
        
        # Botón Preguntas
        self.boton_preguntas = QPushButton("Preguntas")
        self.boton_preguntas.setToolTip("Ver preguntas")
        self.boton_preguntas.setStyleSheet(self.boton_estilo)
        self.boton_preguntas.setFont(QFont("Arial", 10))
        self.boton_preguntas.hide()
        self.boton_preguntas.clicked.connect(self.movimiento_submenu_preguntas)

        # Contenedor para el submenú de preguntas
        self.submenu_preguntas_widget = QWidget()
        self.submenu_preguntas_layout = QVBoxLayout(self.submenu_preguntas_widget)
        self.submenu_preguntas_layout.setContentsMargins(10, 0, 0, 0) # Sangría
        self.submenu_preguntas_layout.setSpacing(5)

        # Preguntas del submenú
        self.botones_sub = [] #array de preguntas
        for i in range(1, 11): # De 1 a 10
            self.sub_boton = QPushButton(f"Pregunta {i}")
            self.sub_boton.setStyleSheet("""
                QPushButton { 
                    color: white; 
                    border: none; 
                    padding: 5px 10px; 
                    text-align: left;
                    background-color: rgba(0, 0, 0, 0.1); 
                    border-radius: 8px;
                }
                QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
            """)
            self.sub_boton.setFont(QFont("Arial", 9))
            self.botones_sub.append(self.sub_boton)
            self.submenu_preguntas_layout.addWidget(self.sub_boton)
            
        self.submenu_preguntas_widget.hide() # Ocultar el submenú contenedor

        # Otros botones del menú principal
        self.boton_progreso = QPushButton("Progreso")
        self.boton_progreso.setToolTip("Ver progreso")
        self.boton_progreso.setStyleSheet(self.boton_estilo)
        self.boton_progreso.setFont(QFont("Arial", 10))
        self.boton_progreso.hide()
        
        self.boton_mensajes = QPushButton("Mensajes")
        self.boton_mensajes.setToolTip("Ver mensajes")
        self.boton_mensajes.setStyleSheet(self.boton_estilo)
        self.boton_mensajes.setFont(QFont("Arial", 10))
        self.boton_mensajes.hide()

        self.boton_solicitud = QPushButton("Solicitar evaluación")
        self.boton_solicitud.setToolTip("Solicitar evaluación profesional")
        self.boton_solicitud.setStyleSheet(self.boton_estilo)
        self.boton_solicitud.setFont(QFont("Arial", 10))
        self.boton_solicitud.hide()        
        
        # Lista de todos los elementos del menú principal (para mostrar/ocultar)
        self.main_menu_widgets = [self.boton_preguntas, self.submenu_preguntas_widget, self.boton_progreso, self.boton_mensajes, self.boton_solicitud]
        
        menu_layout.addWidget(self.boton_preguntas)
        menu_layout.addWidget(self.submenu_preguntas_widget) 
        menu_layout.addWidget(self.boton_progreso)
        menu_layout.addWidget(self.boton_mensajes)
        menu_layout.addWidget(self.boton_solicitud)
        
        # Separador para empujar los botones hacia arriba
        menu_layout.addStretch(1) 

        # --- Botón de Ajustes (Abajo a la derecha) ---
        
        self.pie_menu_widget = QWidget()
        self.pie_menu_layout = QHBoxLayout(self.pie_menu_widget)
        self.pie_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.pie_menu_layout.setAlignment(Qt.AlignRight)
        self.pie_menu_widget.hide() 

        self.boton_ajustes = QPushButton() 
        self.boton_ajustes.setToolTip("Ver ajustes")
        self.boton_ajustes.setFixedSize(50,50) 
        self.boton_ajustes.setIcon(QIcon("assets/ajustes.png")) 
        self.boton_ajustes.setIconSize(QSize(40,40))
        self.boton_ajustes.setStyleSheet("""
            QPushButton { 
                background-color: transparent; 
                color: white; 
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
        """)
        
        self.pie_menu_layout.addWidget(self.boton_ajustes)
        menu_layout.addWidget(self.pie_menu_widget)

        # ------------------- 2. Contenido Principal -------------------   

        # BOTÓN DE USUARIO (Arriba a la derecha)
        self.usuario_widget = QWidget()
        self.usuario_layout = QHBoxLayout(self.usuario_widget)
        self.usuario_layout.setContentsMargins(0, 0, 10, 0)        

        self.boton_usuario = QPushButton()
        self.boton_usuario.setToolTip("Perfil de usuario")
        self.boton_usuario.setFixedSize(50, 50)
        self.boton_usuario.setIcon(QIcon("assets/interno.png"))
        self.boton_usuario.setIconSize(QSize(40, 40))
        self.boton_usuario.setStyleSheet("""
            QPushButton { 
                background-color: transparent;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
        """)

        # Añadir botón al layout de usuario
        self.usuario_layout.addStretch(1)
        self.usuario_layout.addWidget(self.boton_usuario)    

        # PANTALLAS
        self.stacked_widget = QStackedWidget()

        self.pantalla_bienvenida = PantallaBienvenidaInterno()
        self.pantalla_preguntas = PantallaPreguntas()
        self.pantalla_resumen_profesional = PantallaResumenProfesional()

        self.stacked_widget.addWidget(self.pantalla_bienvenida)                          
        self.stacked_widget.addWidget(self.pantalla_preguntas)
        self.stacked_widget.addWidget(self.pantalla_resumen_profesional)
        # añadir más pantallas 

        # pantalla inicial
        self.stacked_widget.setCurrentWidget(self.pantalla_bienvenida)

        # Contenedor central
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.central_layout.addWidget(self.usuario_widget)
        self.central_layout.addWidget(self.stacked_widget, 1)
       
        # ------------------- 3. Menu de Ajustes (Panel Deslizante Derecha) -------------------
        self.ajustes_menu_frame = QWidget()
        self.ajustes_menu_frame.setFixedWidth(self.AJUSTES_ANCHURA_CERRADO)
        self.ajustes_menu_frame.setStyleSheet(f"""
            QWidget {{ background-color: {self.AJUSTES_MENU_COLOR}; border-left: 1px solid #1C1C1C; }}
            QAbstractButton {{ color: white; border: none; padding: 10px; text-align: left; }}
            QAbstractButton:hover {{ background-color: rgba(255, 255, 255, 0.2); }}
        """)

        self.ajustes_menu_layout = QVBoxLayout(self.ajustes_menu_frame)
        self.ajustes_menu_layout.setContentsMargins(10, 20, 10, 10)
        self.ajustes_menu_layout.setAlignment(Qt.AlignTop)

        # Botones de Ajustes
        self.boton_perfil = QPushButton("Perfil")
        self.boton_perfil.setToolTip("Ver y editar perfil")
        self.boton_perfil.setFont(QFont("Arial", 10))
        self.boton_perfil.setStyleSheet(self.boton_estilo)  

        self.boton_cambiar_idioma = QPushButton("Cambiar Idioma")    
        self.boton_cambiar_idioma.setToolTip("Cambiar el idioma de la aplicación")
        self.boton_cambiar_idioma.setFont(QFont("Arial", 10))    
        self.boton_cambiar_idioma.setStyleSheet(self.boton_estilo)

        self.boton_cambiar_tema = QPushButton("Cambiar Tema")
        self.boton_cambiar_tema.setToolTip("Cambiar el tema de la aplicación")
        self.boton_cambiar_tema.setFont(QFont("Arial", 10))    
        self.boton_cambiar_tema.setStyleSheet(self.boton_estilo)

        self.boton_cerrar_sesion = QPushButton("Cerrar Sesión")
        self.boton_cerrar_sesion.setToolTip("Cerrar sesión y volver a la pantalla de inicio")
        self.boton_cerrar_sesion.setFont(QFont("Arial", 10))
        self.boton_cerrar_sesion.setStyleSheet("""                                   
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: center;
                background-color: "#AC1F20";
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: "#F3292B"; 
            }""")

        # Añadir botones al layout de ajustes
        self.ajustes_menu_layout.addWidget(self.boton_perfil)
        self.ajustes_menu_layout.addWidget(self.boton_cambiar_idioma)
        self.ajustes_menu_layout.addWidget(self.boton_cambiar_tema)
        self.ajustes_menu_layout.addWidget(self.boton_cerrar_sesion)

        # --- Añadir widgets al layout principal ---
        main_layout.addWidget(self.menu_frame)          # Añadir el menú lateral al layout principal    
        main_layout.addWidget(self.ajustes_menu_frame) # Añadir el menú de ajustes al layout principal             
        main_layout.addWidget(self.central_widget, 1)   # Añadir el contenido principal al layout principal        
               
        # ------------------- 4. Conexiones de botones -------------------
        self.boton_hamburguesa.clicked.connect(self.movimiento_menu)
        self.boton_ajustes.clicked.connect(self.movimiento_menu_ajustes)
        for i, boton in enumerate(self.botones_sub):
            boton.clicked.connect(lambda checked, num=i+1: self.abrir_pregunta(num))                       

    # ------------------- 5. Movimientos de Menú y Submenú -------------------    
    def movimiento_menu(self):

        if self.ajustes_abierto:
            if self.ajustes_menu_frame.width() > self.AJUSTES_ANCHURA_CERRADO:
                self.movimiento_menu_ajustes()  # Cerrar el menú de ajustes si está abierto           
        
        if self.menu_abierto:
            # Estado A CERRAR (Actual: Abierto)
            anchura_final = self.MENU_ANCHURA_CERRADO
            color_menu = self.COLOR_CERRADO
            
            # Ocultar todos los botones de menú
            for boton in self.main_menu_widgets:
                boton.hide()
            self.pie_menu_widget.hide() 
            
            # Asegurarse de que el submenú esté cerrado y restablecer estilo del botón
            self.submenu_preguntas_widget.hide()
            self.submenu_abierto = False
            self.boton_preguntas.setStyleSheet(self.boton_estilo)        
            
        else:
            # Estado A ABRIR (Actual: Cerrado)
            anchura_final = self.MENU_ANCHURA_ABIERTO
            color_menu = self.COLOR_ABIERTO
            
            # Mostrar botones principales y el footer
            for i, boton in enumerate(self.main_menu_widgets):
                # Ocultar el widget del submenú, solo se muestra al hacer clic en "Preguntas"
                if boton != self.submenu_preguntas_widget:
                    QTimer.singleShot(i * 100, boton.show)  # Muestra cada botón con un retardo
                else:
                    boton.hide()
                    
            self.pie_menu_widget.show()

        # Invertir el estado para el próximo clic
        self.menu_abierto = not self.menu_abierto
        
        # Aplicar el cambio de color
        self.menu_frame.setStyleSheet(f"background-color: {color_menu};")

        # Animación del ancho MÍNIMO y MÁXIMO
        self.animacion_min = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animacion_min.setDuration(300)
        self.animacion_min.setStartValue(self.menu_frame.width())
        self.animacion_min.setEndValue(anchura_final)
        self.animacion_min.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_min.start()
        
        self.animacion_max = QPropertyAnimation(self.menu_frame, b"maximumWidth")
        self.animacion_max.setDuration(300)
        self.animacion_max.setStartValue(self.menu_frame.width())
        self.animacion_max.setEndValue(anchura_final)
        self.animacion_max.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_max.start()

    def movimiento_submenu_preguntas(self):       

        if self.submenu_abierto:
            self.submenu_preguntas_widget.hide()
            self.submenu_abierto = False
            self.boton_preguntas.setStyleSheet(self.boton_estilo) # Desactivar estilo
        else:
            self.submenu_preguntas_widget.show()
            self.submenu_abierto = True
            self.boton_preguntas.setStyleSheet(self.boton_activo_estilo) # Activar estilo

    def movimiento_menu_ajustes(self):        

        if self.ajustes_abierto:
            # Estado A CERRAR (Actual: Abierto)
            anchura_final = self.AJUSTES_ANCHURA_CERRADO
            self.ajustes_abierto = False
        else:
            # Estado A ABRIR (Actual: Cerrado)
            anchura_final = self.AJUSTES_ANCHURA_ABIERTO
            self.ajustes_abierto = True
        
        # Animación del ancho MÍNIMO y MÁXIMO
        self.animacion_ajustes_min = QPropertyAnimation(self.ajustes_menu_frame, b"minimumWidth")
        self.animacion_ajustes_min.setDuration(300)
        self.animacion_ajustes_min.setStartValue(self.ajustes_menu_frame.width())
        self.animacion_ajustes_min.setEndValue(anchura_final)
        self.animacion_ajustes_min.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_ajustes_min.start()
        
        self.animacion_ajustes_max = QPropertyAnimation(self.ajustes_menu_frame, b"maximumWidth")
        self.animacion_ajustes_max.setDuration(300)
        self.animacion_ajustes_max.setStartValue(self.ajustes_menu_frame.width())
        self.animacion_ajustes_max.setEndValue(anchura_final)
        self.animacion_ajustes_max.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_ajustes_max.start()        

    # ------------------- 6. Funciones para cambiar pantallas -------------------
    def mostrar_pantalla_preguntas(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_preguntas)  
        self.pantalla_preguntas.cargar_pregunta(1)   

    def abrir_pregunta(self, numero):
        self.stacked_widget.setCurrentWidget(self.pantalla_preguntas)  
        self.pantalla_preguntas.numero_pregunta = numero
        self.pantalla_preguntas.cargar_pregunta(numero)       

    def mostrar_pantalla_resumen(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_resumen_profesional)

    # ------------------- 7. Método para pasar datos -------------------
    def cargar_datos_interno(self, interno):
        """
        Recibe el objeto interno desde el controlador y se distriuye a las pantallas necesarias
        """
        
        self.pantalla_bienvenida.set_interno(interno)