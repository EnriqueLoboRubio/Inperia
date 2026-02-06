from db.usuario_db import *
from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *

def generar_usuario():    
    agregar_usuario("admin", "admin@g.com", "Admin123", "administrador") #1
    agregar_usuario("interno 2", "2@g.com", "2", "interno") #2
    agregar_usuario("interno 3", "3@g.com", "3", "interno") #3
    agregar_usuario("profesional", "4@g.com", "4", "profesional") #4
    agregar_usuario("interno 5", "5@g.com", "5", "interno") #5

def generar_internos():
    agregar_interno("2", "2", "condenado", "Robo", "5", "01/01/2020", "01/01/2025", "Módulo A")
    agregar_interno("3", "3", "condenado", "Robo", "5", "01/01/2020", "01/01/2025", "Módulo A")
    agregar_interno("5", "5", "condenado", "Robo", "5", "01/01/2020", "01/01/2025", "Módulo B")

def generar_solicitud():
    agregar_solicitud("2", "familiar", "cumpleaños hija", "finde en Moguer para celebrar cumpleaños", "importante", "22/11/2020", "25/22/2020",
                      "16:00", "10:00", "Moguer", "Moguer", "calle 123", "21", 
                      "pepa", "1233", "mujer", "calle 123",
                      "carmen", "2222", "madre",
                      "123", "123456", "nada", "iniciada") #1
    agregar_solicitud("5", "familiar", "cumpleaños hija", "finde en Moguer para celebrar cumpleaños", "importante", "22/11/2020", "25/22/2020",
                      "16:00", "10:00", "Moguer", "Moguer", "calle 123", "21", 
                      "pepa", "1233", "mujer", "calle 123",
                      "carmen", "2222", "madre",
                      "123", "123456", "nada", "pendiente") #2  

def generar_entrevista():
    agregar_entrevista("4", "5", "2", "22/11/2020", "34")

def reiniciar_base_de_datos():
    

    print("Borrando tablas antiguas...")
    # PASO 1: Borrar en orden de dependencia (de hijas a padres)
    
    borrar_entrevista()
    borrar_solicitudes()
    borrar_internos()
    borrar_usuarios()    
    
    
    print("Tablas borradas con éxito.")

    print("Creando nuevas tablas...")
    # PASO 2: Crear en orden de jerarquía (de padres a hijas)
    crear_usuario()       #
    crear_interno()       #
    #crear_profesional()   #
    crear_solicitud()     #
    crear_entrevista()    #
    #crear_respuesta()     #
    #crear_comentario()    #
    
    print("Base de datos reconstruida completamente.")    
    

if __name__ == "__main__":
    
    reiniciar_base_de_datos()

    generar_usuario()
    generar_internos()
    generar_solicitud()    
    generar_entrevista()                  
    