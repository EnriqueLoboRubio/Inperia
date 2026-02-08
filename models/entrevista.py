class Entrevista:
    def __init__(self, id_entrevista, id_interno, id_profesional, fecha):
        self.id_entrevista = id_entrevista
        self.id_profesional = id_profesional
        self.id_interno = id_interno
        self.fecha = fecha
        self.puntuacion = -1
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
            "id_profesional": self.id_profesional,
            "id_interno": self.id_interno,            
            "fecha": self.fecha,
            "puntuacion_global": self.puntuacion if self.puntuacion != -1 else None,
            "respuestas": [respuesta.to_json() for respuesta in self.respuestas],
        }


