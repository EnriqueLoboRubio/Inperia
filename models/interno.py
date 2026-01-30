from models.usuario import Usuario
from utils.enums import Tipo_rol

class Interno(Usuario):
    def __init__(self, id_usuario, nombre, email, contrasena, rol, num_RC, situacion_legal, delito, fecha_nac, condena, fecha_ingreso, modulo):
        
        super().__init__(id_usuario, nombre, email, contrasena, Tipo_rol.INTERNO)

        self.num_RC = num_RC
        self.situacion_legal = situacion_legal
        self.delito = delito
        self.fecha_nac = fecha_nac
        self.condena = condena
        self.fecha_ingreso = fecha_ingreso
        self.modulo = modulo
        self.solicitudes = []
        self.entrevistas = []        
    
    def add_solicitud(self, solicitud):
        self.solicitudes.append(solicitud)   
    
    def add_entrevista(self, entrevista):
        self.entrevistas.append(entrevista)
