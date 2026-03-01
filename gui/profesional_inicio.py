from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget,
    QDialog, QFrame, QLabel
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap

from gui.pantalla_bienvenida_profesional import PantallaBienvenidaProfesional
from gui.pantalla_perfil import PantallaPerfil
from gui.pantalla_lista_solicitud import PantallaListaSolicitud
from gui.pantalla_lista_modificar_preguntas import PantallaListaModificarPreguntas
from gui.estilos import *


class VentanaProfesional(QMainWindow):
    
    # Ancho del menú cuando está cerrado y abierto
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
        self.setWindowTitle("INPERIA - Profesional")           
        
        # Estados iniciales del menú y submenús
        self.menu_abierto = False
        self.ajustes_abierto = False

        self.init_ui()

    def setup_window(self):      
        self.setWindowIcon(QIcon("assets/inperia.ico"))
        self.setMinimumSize(1200,700)
        self.showMaximized()        

    def init_ui(self):
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
        # --- Botones del Menú Principal ---

        # Botón Estadísticas
        self.boton_estadisticas = QPushButton("Estadísticas de entrevistas")
        self.boton_estadisticas.setToolTip("Ver estadísticas de entrevistas realizadas")
        self.boton_estadisticas.setStyleSheet(self.boton_estilo)
        self.boton_estadisticas.setFont(QFont("Arial", 10))
        self.boton_estadisticas.hide() # Ocultar por defecto

        # Botón nueva
        self.boton_nueva = QPushButton("Nueva solicitud")
        self.boton_nueva.setToolTip("Asignar nueva solicitud")
        self.boton_nueva.setStyleSheet(self.boton_estilo)
        self.boton_nueva.setFont(QFont("Arial", 10))
        self.boton_nueva.hide()

        # Botón pendiente
        self.boton_pendiente = QPushButton("Solicitudes por evaluar")
        self.boton_pendiente.setToolTip("Ver solicitudes por evaluar")
        self.boton_pendiente.setStyleSheet(self.boton_estilo)
        self.boton_pendiente.setFont(QFont("Arial", 10))
        self.boton_pendiente.hide()

        # Botón Historial
        self.boton_historial = QPushButton("Historial de solicitudes")
        self.boton_historial.setToolTip("Ver el historial de solicitudes")
        self.boton_historial.setStyleSheet(self.boton_estilo)
        self.boton_historial.setFont(QFont("Arial", 10))
        self.boton_historial.hide()

        # Botón Datos
        self.boton_datos = QPushButton("Datos de internos")
        self.boton_datos.setToolTip("Ver datos de internos asignados")
        self.boton_datos.setStyleSheet(self.boton_estilo)
        self.boton_datos.setFont(QFont("Arial", 10))
        self.boton_datos.hide()

        # Botón Modificar Preguntas
        self.boton_modificar = QPushButton("Modificar preguntas")
        self.boton_modificar.setToolTip("Editar el cuestionario de entrevistas")
        self.boton_modificar.setStyleSheet(self.boton_estilo)
        self.boton_modificar.setFont(QFont("Arial", 10))
        self.boton_modificar.hide()

        # Botón Ajustes del Modelo
        self.boton_ajustes_modelo = QPushButton("Ajustes del modelo")
        self.boton_ajustes_modelo.setToolTip("Configurar ajustes del modelo de IA")
        self.boton_ajustes_modelo.setStyleSheet(self.boton_estilo)
        self.boton_ajustes_modelo.setFont(QFont("Arial", 10))
        self.boton_ajustes_modelo.hide()

        # Botón Casos Críticos
        self.boton_casos_criticos = QPushButton("Casos críticos")
        self.boton_casos_criticos.setToolTip("Ver casos críticos detectados")
        self.boton_casos_criticos.setStyleSheet(self.boton_estilo)
        self.boton_casos_criticos.setFont(QFont("Arial", 10))
        self.boton_casos_criticos.hide()   

       
        # Lista de todos los elementos del menú principal (para mostrar/ocultar)
        self.main_menu_widgets = [
            self.boton_nueva,
            self.boton_pendiente,
            self.boton_historial,
            self.boton_datos,
            self.boton_estadisticas,
            self.boton_modificar,
            self.boton_ajustes_modelo,
            self.boton_casos_criticos
        ]
        self.menu_widgets_visibles = list(self.main_menu_widgets)

        # Añadir botones al layout del menú
        for boton in self.main_menu_widgets:
            menu_layout.addWidget(boton)           
        
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
        self.boton_usuario.setIcon(QIcon("assets/profesional.png"))
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

        self.pantalla_bienvenida = PantallaBienvenidaProfesional()        
        self.pantalla_perfil = PantallaPerfil()
        self.pantalla_lista_solicitud = PantallaListaSolicitud()
        self.pantalla_lista_modificar_preguntas = PantallaListaModificarPreguntas()

        self.stacked_widget.addWidget(self.pantalla_bienvenida)                                  
        self.stacked_widget.addWidget(self.pantalla_lista_solicitud)
        self.stacked_widget.addWidget(self.pantalla_lista_modificar_preguntas)
        self.stacked_widget.addWidget(self.pantalla_perfil)
        # Aquí se pueden añadir más pantallas al stacked_widget según sea necesario

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

        self.boton_cerrar_sesion = QPushButton("Cerrar Sesión")
        self.boton_cerrar_sesion.setToolTip("Cerrar sesión y volver a la pantalla de inicio")
        self.boton_cerrar_sesion.setFont(QFont("Arial", 10))
        self.boton_cerrar_sesion.setStyleSheet("""                                   
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: left;
                background-color: "#AC1F20";
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: "#F3292B"; 
            }""")

        # Añadir botones al layout de ajustes
        self.ajustes_menu_layout.addWidget(self.boton_perfil)
        self.ajustes_menu_layout.addWidget(self.boton_cerrar_sesion)

        # --- Añadir widgets al layout principal ---
        main_layout.addWidget(self.menu_frame)          # Añadir el menú lateral al layout principal    
        main_layout.addWidget(self.ajustes_menu_frame) # Añadir el menú de ajustes al layout principal     
        main_layout.addWidget(self.central_widget, 1)   # Añadir el contenido principal al layout principal        
               

        # ------------------- 4. Conexiones de botones -------------------
        self.boton_hamburguesa.clicked.connect(self.movimiento_menu)
        self.boton_ajustes.clicked.connect(self.movimiento_menu_ajustes)

    # ------------------- 5. Movimientos de Menú -------------------
    def obtener_widgets_menu_visibles(self):
        return [boton for boton in self.main_menu_widgets if boton in self.menu_widgets_visibles]

    def actualizar_interfaz_inicio(self, num_solicitudes_pendientes, num_solicitudes_completadas, num_historial=None):
        """
        Sincroniza la pantalla de bienvenida y las opciones visibles del menú
        según el estado de solicitudes del profesional.
        """
        self.pantalla_bienvenida.actualizar_interfaz(
            num_solicitudes_pendientes,
            num_solicitudes_completadas
        )

        if num_historial is None:
            num_historial = num_solicitudes_completadas

        if self.menu_abierto:
            self.boton_pendiente.setVisible(num_solicitudes_pendientes > 0)
            self.boton_historial.setVisible(num_historial > 0)
        else:
            self.boton_pendiente.hide()
            self.boton_historial.hide()

        self.menu_widgets_visibles = []
        for boton in self.main_menu_widgets:
            if boton == self.boton_pendiente and num_solicitudes_pendientes == 0:
                continue
            if boton == self.boton_historial and num_historial == 0:
                continue
            self.menu_widgets_visibles.append(boton)

    def movimiento_menu(self):   

        if self.ajustes_abierto:
            if self.ajustes_menu_frame.width() > self.AJUSTES_ANCHURA_CERRADO:
                self.movimiento_menu_ajustes()  # Cerrar el menú de ajustes si está abierto           
        
        if self.menu_abierto:
            # Estado A CERRAR (Actual: Abierto)
            anchura_final = self.MENU_ANCHURA_CERRADO
            color_menu = self.COLOR_CERRADO
            
            # Ocultar todos los botones de menú
            for widget in self.main_menu_widgets:
                widget.hide()
            self.pie_menu_widget.hide()             
            
        else:
            # Estado A ABRIR (Actual: Cerrado)
            anchura_final = self.MENU_ANCHURA_ABIERTO
            color_menu = self.COLOR_ABIERTO   
          
            # Mostrar botones con retardo para efecto escalonado
            for i, boton in enumerate(self.obtener_widgets_menu_visibles()):
                QTimer.singleShot(i * 100, boton.show)  # Muestra cada botón con un retardo
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

    def mostrar_confirmacion_logout(self):
        dialogo = QDialog(self)
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
        pixmap = QPixmap("assets/error.png").scaled(
            30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        lbl_icono.setPixmap(pixmap)

        titulo = QLabel("Cerrar sesión")
        titulo.setObjectName("TituloError")

        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()

        lbl_mensaje = QLabel(
            "¿Estás seguro de que quieres cerrar sesión?\n\n"
            "Perderá los datos no guardados."
        )
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(320)

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

        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(10)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(20)
        layout_interno.addLayout(layout_botones)

        layout_main.addWidget(fondo)

        resultado = dialogo.exec_()
        return resultado == QDialog.Accepted

    def mostrar_pantalla_perfil(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_perfil)

    def mostrar_pantalla_modificar_preguntas(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_lista_modificar_preguntas)
