from models.usuario import Usuario
from utils.enums import Tipo_rol

class Profesional(Usuario):
    def __init__(self, id_usuario, nombre, contrasena, rol, tipo):
        
        super().__init__(id_usuario, nombre, contrasena, Tipo_rol.PROFESIONAL.value)

        self.tipo = tipo    
        self.entrevistas = []
    
    def add_entrevista(self, entrevista):
        self.entrevistas.append(entrevista)