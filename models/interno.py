from models.usuario import Usuario
from utils.enums import Tipo_rol

class Interno(Usuario):
    def __init__(self, id_usuario, nombre, contrasena, rol, num_RC, situacion_legal, delito, edad, condena, fecha_ingreso):
        
        super().__init__(id_usuario, nombre, contrasena, Tipo_rol.INTERNO)

        self.num_RC = num_RC
        self.situacion_legal = situacion_legal
        self.delito = delito
        self.edad = edad
        self.condena = condena
        self.fecha_ingreso = fecha_ingreso

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