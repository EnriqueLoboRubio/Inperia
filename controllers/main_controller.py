import sys
import ctypes
from pathlib import Path
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from gui.login import VentanaLogin
from db.data_seeding import ejecutar_data_seeding_inicial

# CONTROLADORES ESPECIFICOS
from controllers.login_controller import LoginController
from controllers.administrador_controller import AdministradorController
from controllers.interno_controller import InternoController
from controllers.profesional_controller import ProfesionalController

class MainController:
    def __init__(self):
        ejecutar_data_seeding_inicial()

        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Inperia.App")

        # aplicacion Qt
        self.app = QApplication(sys.argv)
        ruta_icono = Path(__file__).resolve().parent.parent / "assets" / "inperia.ico"
        self.app.setWindowIcon(QIcon(str(ruta_icono)))
        self.splash_widget = None
        self.splash_animacion = None
        
        self.ventana_actual = None
        self.controlador_interno = None
        self.controlador_administrador = None
        self.login_controller = None                 

        self.mostrar_splash_inicio()

    def mostrar_splash_inicio(self):
        ruta_imagen = Path(__file__).resolve().parent.parent / "assets" / "inperiaBlanco.png"

        self.splash_widget = QWidget()
        self.splash_widget.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen
        )
        self.splash_widget.setAttribute(Qt.WA_TranslucentBackground, True)

        layout = QVBoxLayout(self.splash_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        etiqueta_imagen = QLabel()
        pixmap = QPixmap(str(ruta_imagen))
        etiqueta_imagen.setPixmap(pixmap)
        etiqueta_imagen.setAlignment(Qt.AlignCenter)
        layout.addWidget(etiqueta_imagen)

        self.splash_widget.setWindowOpacity(0.0)
        self.splash_widget.adjustSize()
        pantalla = QApplication.primaryScreen()
        if pantalla:
            rect_pantalla = pantalla.availableGeometry()
            x = rect_pantalla.x() + (rect_pantalla.width() - self.splash_widget.width()) // 2
            y = rect_pantalla.y() + (rect_pantalla.height() - self.splash_widget.height()) // 2
            self.splash_widget.move(x, y)
        self.splash_widget.show()

        self.splash_animacion = QPropertyAnimation(self.splash_widget, b"windowOpacity")
        self.splash_animacion.setDuration(900)
        self.splash_animacion.setStartValue(0.0)
        self.splash_animacion.setEndValue(1.0)
        self.splash_animacion.setEasingCurve(QEasingCurve.InOutQuad)
        self.splash_animacion.finished.connect(self.cerrar_splash_y_mostrar_login)
        self.splash_animacion.start()

    def cerrar_splash_y_mostrar_login(self):
        if self.splash_widget:
            self.splash_widget.close()
            self.splash_widget = None
        self.splash_animacion = None
        self.mostrar_login()

    def mostrar_login(self):
        self.login_controller = LoginController()
        self.ventana_login = VentanaLogin()

        # -------- CONEXIONES MVC --------        

        # Login Vista -> Controlador Login (boton entrar)
        self.ventana_login.signal_solicitar_login.connect(
            self.login_controller.procesar_login
        )

        # Controlador Login -> Login Vista (error)
        self.login_controller.signal_login_fallido.connect(
            self.ventana_login.mostrar_mensaje_error
        )

        # Controlador Login -> MainController (Ã©xito)
        self.login_controller.signal_login_exitoso.connect(
            self.manejar_login_exitoso
        )
            
        self.ventana_login.show()

    def manejar_login_exitoso(self, usuario, rol):
        """
        Esta funciÃ³n se ejecuta cuando el Login emite la seÃ±al de Ã©xito.
        Recibe el ID del usuario y su rol
        """
        # Cerramos el login
        self.ventana_login.close()
        self.login_controller = None

        if rol == "interno":
            self.iniciar_sesion_interno(usuario)
        elif rol == "profesional":
            self.iniciar_sesion_profesional(usuario)
        elif rol == "administrador":
            self.iniciar_sesion_administrador(usuario)
        else:
            print(f"Rol desconocido: {rol}")            

    def iniciar_sesion_interno(self, usuario):       
        self.controlador_interno = InternoController(usuario)
        self.controlador_interno.logout_signal.connect(self.regresar_login)    

    def iniciar_sesion_profesional(self, usuario):
        self.controlador_profesional = ProfesionalController(usuario)
        self.controlador_profesional.logout_signal.connect(self.regresar_login)    

    def iniciar_sesion_administrador(self, usuario):
        self.controlador_administrador = AdministradorController(usuario)
        self.controlador_administrador.logout_signal.connect(self.regresar_login)

    def ejecutar(self):
        sys.exit(self.app.exec_())

    def regresar_login(self):
        if self.controlador_interno:
            try:                       
                self.controlador_interno.logout_signal.disconnect()                      
                self.controlador_interno.ventana_interno.close()
            except:
                pass
                self.controlador_interno = None

        if getattr(self, "controlador_profesional", None):
            try:
                self.controlador_profesional.logout_signal.disconnect()
                self.controlador_profesional.ventana_profesional.close()
            except:
                pass
            self.controlador_profesional = None

        if self.controlador_administrador:
            try:
                self.controlador_administrador.logout_signal.disconnect()
                self.controlador_administrador.ventana_administrador.close()
            except:
                pass
            self.controlador_administrador = None

        # crear el entorno de login
        self.mostrar_login()

