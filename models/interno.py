from models.usuario import Usuario
from utils.enums import Tipo_rol

class Interno(Usuario):
    def __init__(
        self,
        id_usuario,
        nombre,
        email,
        contrasena,
        rol,
        num_RC,
        situacion_legal,
        delito,
        fecha_nac,
        condena,
        fecha_ingreso,
        modulo,
        lugar_nacimiento="",
        nombre_contacto_emergencia="",
        relacion_contacto_emergencia="",
        numero_contacto_emergencia="",
    ):
        
        super().__init__(id_usuario, nombre, email, contrasena, Tipo_rol.INTERNO.value)

        self.num_RC = num_RC
        self.situacion_legal = situacion_legal
        self.delito = delito
        self.fecha_nac = fecha_nac
        self.condena = condena
        self.fecha_ingreso = fecha_ingreso
        self.modulo = modulo
        self.lugar_nacimiento = lugar_nacimiento
        self.nombre_contacto_emergencia = nombre_contacto_emergencia
        self.relacion_contacto_emergencia = relacion_contacto_emergencia
        self.numero_contacto_emergencia = numero_contacto_emergencia
        self.solicitudes = []     
    
    def add_solicitud(self, solicitud):
        self.solicitudes.append(solicitud)   
    
