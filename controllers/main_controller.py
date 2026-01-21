import sys
from PyQt5.QtWidgets import QApplication
# VISTAS
from gui.login import VentanaLogin
from gui.interno_inicio import VentanaInterno
from gui.profesional_inicio import VentanaProfesional 
from gui.pantalla_bienvenida_interno import PantallaBienvenidaInterno
from gui.pantalla_bienvenida_profesional import PantallaBienvenidaProfesional

# Importamos los CONTROLADORES ESPECÍFICOS
from controllers.login_controller import LoginController
from controllers.interno_controller import InternoController

class MainController:
    def __init__(self):
        # aplicación Qt
        self.app = QApplication(sys.argv)
        
        self.ventana_actual = None
        
        # Controladores secundarios
        self.login_controller = LoginController()

        self.mostrar_login()

    def mostrar_login(self):
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

        # Controlador Login -> MainController (éxito)
        self.login_controller.signal_login_exitoso.connect(
            self.manejar_login_exitoso
        )
            
        self.ventana_login.show()

    def manejar_login_exitoso(self, usuario_id, rol):
        """
        Esta función se ejecuta cuando el Login emite la señal de éxito.
        Recibe el ID del usuario y su rol
        """
        # Cerramos el login
        self.ventana_login.close()

        if rol == "interno":
            self.iniciar_sesion_interno(usuario_id)
        elif rol == "profesional":
            self.iniciar_sesion_profesional(usuario_id)
        elif rol == "administrador":
            # implementar la vista del administrador
            print("Inicio de sesión como Administrador - Funcionalidad no implementada")    
        else:
            print(f"Rol desconocido: {rol}")            

    def iniciar_sesion_interno(self, usuario_id):
        # vista del interno
        #self.ventana_actual = VentanaInterno()
        #self.ventana_actual.show()
        
        self.controlador_interno = InternoController(usuario_id)
        self.controlador_interno.inicio()

    def iniciar_sesion_profesional(self, usuario_id):
        self.ventana_actual = VentanaProfesional()
        self.ventana_actual.show()

    def ejecutar(self):
        sys.exit(self.app.exec_())