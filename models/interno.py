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

    def set_num_RC(self, num_RC):
        self.num_RC = num_RC
        
    def get_num_RC(self):
        return self.num_RC    
    
    def set_situacion_legal(self, situacion_legal):
        self.situacion_legal = situacion_legal

    def get_situacion_legal(self):
        return self.situacion_legal

    def set_delito(self, delito):
        self.delito = delito

    def get_delito(self):
        return self.delito
    
    def set_edad(self, edad):
        self.edad = edad
            
    def get_edad(self):
        return self.edad

    def set_condena(self, condena):
        self.condena = condena

    def get_condena(self):
        return self.condena

    def set_fecha_ingreso(self, fecha_ingreso):
        self.fecha_ingreso = fecha_ingreso
        
    def get_fecha_ingreso(self):
        return self.fecha_ingreso    
    
    def add_solicitud(self, solicitud):
        self.solicitudes.append(solicitud)

    def get_solicitudes(self):
        return self.solicitudes
    
    def add_entrevista(self, entrevista):
        self.entrevistas.append(entrevista)

    def get_entrevistas(self):
        return self.entrevistas