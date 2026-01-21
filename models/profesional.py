from models.usuario import Usuario
from utils.enums import tipo_rol

class Profesional(Usuario):
    def __init__(self, id_usuario, nombre, contrasena, rol, tipo):
        
        super().__init__(id_usuario, nombre, contrasena, tipo_rol.PROFESIONAL)

        self.tipo = tipo    