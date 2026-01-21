

class Pregunta():
    def __init__(self, id_pregunta, respuesta):
        self.id_pregunta = id_pregunta
        self.respuesta = respuesta
        self.nivel = -1
        self.valoracion_ia = ""
        self.comentarios = []

    def get_id_pregunta(self):
        return self.id_pregunta    

    def set_respuesta(self, nueva_respuesta):
        self.respuesta = nueva_respuesta

    def get_respuesta(self):
        return self.respuesta

    def set_nivel(self, nivel):
        self.nivel = nivel

    def get_nivel(self):
        return self.nivel

    def set_valoracion_ia(self, valoracion):
        self.valoracion_ia = valoracion

    def get_valoracion_ia(self):
        return self.valoracion_ia

    def add_comentario(self, nuevo_comentario):
        if isinstance(nuevo_comentario, str):
            self.comentarios.append(nuevo_comentario)

    def get_comentarios(self):
        return self.comentarios
    
