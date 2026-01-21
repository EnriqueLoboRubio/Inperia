from db.usuario_db import *

def generar_usuario():    
    agregar_usuario("admin", "admin@g.com", "Admin123", "administrador")
    agregar_usuario("profesional", "1@g.com", "1", "profesional")
    agregar_usuario("interno", "2@g.com", "2", "interno")

def reiniciar_base_datos_usuario():
    borrar_usuarios()
    crear_usuario()

if __name__ == "__main__":
    #reiniciar_base_datos_usuario()
    generar_usuario()