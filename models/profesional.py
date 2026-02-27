from models.usuario import Usuario
from utils.enums import Tipo_rol

class Profesional(Usuario):
    def __init__(self, id_usuario, num_profesional, nombre, email, contrasena,):
        
        super().__init__(id_usuario, nombre, email, contrasena, Tipo_rol.PROFESIONAL.value)

           
        self.num_profesional = num_profesional
        self.solicitudes = []
    
    def add_solicitud(self, solicitud):
        self.solicitudes.append(solicitud)