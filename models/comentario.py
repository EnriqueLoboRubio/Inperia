
import os

class Comentario():
    def __init__(self, id_pregunta, contenido):
        self.id_profesional = id_pregunta
        self.contenido = contenido       

    def get_id_profesional(self):
        return self.id_profesional    

    def set_contenido(self, nuevo_contenido):
        self.contenido = nuevo_contenido

    def get_contenido(self):
        return self.contenido    
    
