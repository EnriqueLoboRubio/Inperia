from db.usuario_db import *
from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *

def generar_usuario():    
    agregar_usuario("admin", "admin@g.com", "Admin123", "administrador") #1
    agregar_usuario("interno 2", "2@g.com", "2", "interno") #2
    agregar_usuario("interno 3", "3@g.com", "3", "interno") #3
    agregar_usuario("profesional", "4@g.com", "4", "profesional") #4

def reiniciar_usuario():
    borrar_usuarios()
    crear_usuario()


def generar_internos():
    agregar_interno("2", "2", "condenado", "Robo", "5", "01-01-2020", "01-01-2025", "Módulo A")
    agregar_interno("3", "3", "condenado", "Robo", "5", "01-01-2020", "01-01-2025", "Módulo A")

def reiniciar_internos():
    borrar_internos()
    crear_interno()

def generar_solicitud():
    agregar_solicitud("2", "familiar", "cumpleaños hija", "finde en Moguer para celebrar cumpleaños", "importante", "22-11-2020", "25-22-2020",
                      "16:00", "10:00", "Moguer", "Moguer", "calle 123", "21", 
                      "pepa", "1233", "mujer",
                      "carmen", "2222", "madre",
                      "123", "123456", "nada", "pendiente")
    
def reiniciar_solicitudes():
    borrar_solicitudes()
    crear_solicitud()
    

if __name__ == "__main__":
    reiniciar_usuario()
    generar_usuario()
    reiniciar_internos()
    generar_internos()
    reiniciar_solicitudes()
    generar_solicitud()