class Entrevista:
    def __init__(self, id_entrevista, id_interno, fecha):
        self.id_entrevista = id_entrevista
        self.id_interno = id_interno
        self.fecha = fecha
        self.puntuacion_ia = -1
        self.puntuacion_profesional = -1
        self.estado_evaluacion_ia = "sin evaluación"
        self.respuestas = []
        self.resumen = ""
        self.comentarios = []   

    def add_comentario(self, nuevo_comentario):
        self.comentarios.append(nuevo_comentario)
    
    def add_respuestas(self, respuesta):
        self.respuestas.append(respuesta)
    
    def to_json(self):
        "Devuelve un diccionario con el formato JSON de la entrevista, para mandar a LLM"
        return {
            "id_entrevista": self.id_entrevista,
            "id_interno": self.id_interno,            
            "fecha": self.fecha,
            "puntuacion_ia": self.puntuacion_ia if self.puntuacion_ia != -1 else None,
            "puntuacion_profesional": self.puntuacion_profesional if self.puntuacion_profesional != -1 else None,
            "estado_evaluacion_ia": self.estado_evaluacion_ia,
            "respuestas": [respuesta.to_json() for respuesta in self.respuestas],
        }


