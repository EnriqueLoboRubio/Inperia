from abc import ABC

class Usuario(ABC):
    def __init__(self, id_usuario, nombre, email, contrasena, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.rol = rol

    def get_id_usuario(self):
        return self.id_usuario
    
    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_nombre(self):
         return self.nombre
    
    def set_email(self, email):
        self.email = email
        
    def get_email(self):
        return self.email

    def set_contrasena(self, contrasena):
        self.contrasena = contrasena

    def get_contrasena(self):
        return self.contrasena    
    
    def get_rol(self):
        return self.rol

    def autenticar(self, contrasena):
        return self.contrasena == contrasena    
    
    def cerrar_sesion(self):
        pass