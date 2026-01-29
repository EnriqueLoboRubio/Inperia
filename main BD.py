from db.usuario_db import *
from db.interno_db import *

def generar_usuario():    
    agregar_usuario("admin", "admin@g.com", "Admin123", "administrador")
    agregar_usuario("profesional", "1@g.com", "1", "profesional")
    agregar_usuario("interno", "2@g.com", "2", "interno")

def reiniciar_usuario():
    borrar_usuarios()
    crear_usuario()


def generar_internos():
    agregar_interno("2", "2", "condenado", "Robo", "5", "01-01-2020", "01-01-2025", "Módulo A")

def reiniciar_internos():
    borrar_internos()
    crear_interno()

if __name__ == "__main__":
    reiniciar_usuario()
    generar_usuario()
    reiniciar_internos()
    generar_internos()