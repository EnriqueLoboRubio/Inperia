class Entrevista:
    def __init__(self, id_entrevista, id_interno, id_profesional, fecha):
        self.id_entrevista = id_entrevista
        self.id_profesional = id_profesional
        self.id_interno = id_interno
        self.fecha = fecha
        self.puntuacion = -1
        self.preguntas = []
        self.resumen = ""
        self.comentarios = []

    def get_id_entrevista(self):
        return self.id_entrevista

    def get_id_interno(self):
        return self.id_interno

    def get_id_profesional(self):
        return self.id_profesional

    def set_fecha(self, fecha):
        self.fecha = fecha

    def get_fecha(self):
        return self.fecha        

    def set_puntuacion(self, puntuacion):
        self.puntuacion = puntuacion
        
    def get_puntuacion(self):
        return self.puntuacion

    def set_resumen(self, resumen):
        self.resumen = resumen

    def get_resumen(self):
        return self.resumen    

    def add_comentario(self, nuevo_comentario):
        self.comentarios.append(nuevo_comentario)

    def get_comentarios(self):
        return self.comentarios


