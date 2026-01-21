from PyQt5.QtCore import QObject, pyqtSignal

from utils.encriptar import verificar_contrasena
from db.usuario_db import crear_usuario, agregar_usuario, verificar_login, eliminar_usuario, encontrar_usuario
import re

class LoginController(QObject):

    # Señales
    signal_login_exitoso = pyqtSignal(str, str)  # ID del usuario y rol
    signal_login_fallido = pyqtSignal(str)       # Mensaje de error

    def __init__(self):
        super().__init__()
        self.intentos_fallidos = 0

    def validar_formato_correo(self, correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        return re.match(patron, correo) is not None
    
    def procesar_login(self, correo, contrasena, tipo_pantalla_seleccionada):

        # Validar campos vacíos
        if not correo or not contrasena:
            self.signal_login_fallido.emit("Por favor, complete todos los campos.")
            return
        
        # Validar formato correo
        if not self.validar_formato_correo(correo):
            self.signal_login_fallido.emit("Formato de correo inválido.")
            return
        
        # Consultar en la base de datos
        usuario_existe = encontrar_usuario(correo)
        rol_detectado =  verificar_login(correo, contrasena)

        if usuario_existe:
            if rol_detectado:
                # Verificar que el rol coincida con la pantalla seleccionada
                if (rol_detectado == tipo_pantalla_seleccionada):
                    self.intentos_fallidos = 0  # Resetear contador de intentos fallidos
                    self.signal_login_exitoso.emit(correo, rol_detectado)
                    return
                else:
                    self.signal_login_fallido.emit("Tipo de usuario incorrecto para la pantalla seleccionada.")
                    return
            else:
                #Contraseña incorrecta
                self.intentos_fallidos += 1
                intentos_restantes = 3 - self.intentos_fallidos
                
                if self.intentos_fallidos >= 3:
                    eliminar_usuario(correo)
                    self.signal_login_fallido.emit("CRITICO: Ha superado el número máximo de intentos. La cuenta ha sido eliminada. Contacte con el administrador.")
                    return
                else:
                    self.signal_login_fallido.emit(f"Usuario o contraseña incorrectos. Le quedan {intentos_restantes} intentos.")
                    return
        else:
            #Usuario no existe
            self.signal_login_fallido.emit("El usuario no existe.")
            self.intentos_fallidos = 0  # Resetear contador de intentos fallidos
            return