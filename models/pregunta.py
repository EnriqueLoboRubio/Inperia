
import os

class Pregunta():
    def __init__(self, id_pregunta, respuesta):
        self.id_pregunta = id_pregunta
        self.respuesta = respuesta
        self.nivel = -1
        self.valoracion_ia = ""
        self.comentarios = []
        self.archivo_audio = None  # Ruta al archivo de audio asociado

    def add_comentario(self, nuevo_comentario):        
        self.comentarios.append(nuevo_comentario)   
    
    def set_archivo_audio(self, nuevo_audio):
        if os.path.exists(nuevo_audio):
            self.archivo_audio = nuevo_audio
            return True
        else:
            return False       
    
    def to_json(self):
        "Devuelve un diccionario con el formato JSON de la pregunta, para mandar a LLM"
        return {
            "id_pregunta": self.id_pregunta,
            "respuesta": self.respuesta
        }
    
