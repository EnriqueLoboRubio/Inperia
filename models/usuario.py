from abc import ABC

class Usuario(ABC):
    def __init__(self, id_usuario, nombre, email, contrasena, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.rol = rol

    def autenticar(self, contrasena):
        return self.contrasena == contrasena