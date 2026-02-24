from db.usuario_db import *
from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *
from db.respuesta_db import *
from db.comentario_pregunta_db import *
from db.comentario_entrevista_db import *
from db.conexion import obtener_conexion
import sqlite3
import json
import os
from models.entrevista import Entrevista

from models.pregunta import Pregunta

def generar_usuario():    
    agregar_usuario("admin", "admin@g.com", "Admin123", "administrador") #1
    agregar_usuario("interno 2", "2@g.com", "2", "interno") #2
    agregar_usuario("interno 3", "3@g.com", "3", "interno") #3
    agregar_usuario("profesional", "4@g.com", "4", "profesional") #4
    agregar_usuario("interno 5", "5@g.com", "5", "interno") #5
    agregar_usuario("interno 6", "6@g.com", "6", "interno") #6

def generar_internos():
    agregar_interno("2", "2", "condenado", "Robo", "5", "01/01/1980", "01/01/2025", "Módulo A")
    agregar_interno("3", "3", "condenado", "Robo", "5", "01/01/1980", "01/01/2025", "Módulo A")
    agregar_interno("5", "5", "condenado", "Robo", "5", "01/01/1980", "01/01/2025", "Módulo B")
    agregar_interno("6", "6", "condenado", "Estafa", "4", "02/02/1980", "02/02/2025", "Módulo C")

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
    agregar_solicitud("6", "juridico", "cita judicial", "salida para comparecencia en sede judicial", "normal", "10/03/2026", "10/03/2026",
                      "08:00", "14:00", "Juzgado Central", "Huelva", "Avenida Principal 45", "21001",
                      "Laura Perez", "600112233", "hermana", "Calle Real 10",
                      "Antonio Perez", "600445566", "padre",
                      "1", "1", "Documentacion completa revisada", "rechazada") #3


def generar_entrevista():
    lista_objetos_pregunta = []

    # Creamos 10 objetos Pregunta con datos de relleno
    for i in range(1, 11):
        # Instanciamos: ID (i) y Texto ("respuesta X")
        nueva_pregunta = Pregunta(i, f"respuesta {i}")
        lista_objetos_pregunta.append(nueva_pregunta)

    agregar_entrevista_y_respuestas("5", "2", "22/11/2020", lista_objetos_pregunta)
    agregar_entrevista_y_respuestas("6", "3", "10/03/2026", lista_objetos_pregunta)

def generar_comentarios_preguntas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Entrevistas generadas en generar_entrevista()
    entrevistas_objetivo = [2, 3]

    for id_entrevista in entrevistas_objetivo:
        cursor.execute(
            """
            SELECT id, id_pregunta
            FROM respuestas
            WHERE id_entrevista = ?
            ORDER BY id_pregunta
            """,
            (id_entrevista,),
        )
        respuestas = cursor.fetchall()

        for id_respuesta, id_pregunta in respuestas:
            comentarios = [
                (4, f"Comentario 1 - Entrevista {id_entrevista}, pregunta {id_pregunta}", "12/03/2026"),
                (1, f"Comentario 2 - Entrevista {id_entrevista}, pregunta {id_pregunta}", "13/03/2026"),
            ]

            cursor.executemany(
                """
                INSERT INTO comentarios_pre (id_respuesta, id_profesional, comentario, fecha)
                VALUES (?, ?, ?, ?)
                """,
                [(id_respuesta, id_profesional, texto, fecha) for id_profesional, texto, fecha in comentarios],
            )

    conexion.commit()
    conexion.close()

def reiniciar_base_de_datos():
    

    print("Borrando tablas antiguas...")    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS comentarios_pre")
    cursor.execute("DROP TABLE IF EXISTS comentarios_ent")
    conexion.commit()
    conexion.close()

    borrar_respuestas()
    borrar_entrevistas()
    borrar_solicitudes()
    borrar_internos()
    borrar_usuarios()    
    
    
    print("Tablas borradas con éxito.")

    print("Creando nuevas tablas...")
    
    crear_usuario()       #
    crear_interno()       #
    #crear_profesional()   #
    crear_respuesta()     #
    crear_comentario_pre() #
    crear_comentario_ent() #
    crear_solicitud()     #
    crear_entrevista()    #
    
    print("Base de datos reconstruida completamente.")  

def ver_info_completa_por_solicitud(id_solicitud):

    #Ver estado de soliciud
    estado= obtener_estado_solicitud(id_solicitud)
    print(f"Estado solicitud {estado}")
    
    #Buscar entrevista con id asociada
    entrevista = None
    datos_entrevista = encontrar_entrevista_por_solicitud(id_solicitud)
    if datos_entrevista:
        entrevista = Entrevista(
                id_entrevista=datos_entrevista[0],
                id_interno=datos_entrevista[1],
                fecha=datos_entrevista[3]
            )

        entrevista.puntuacion = datos_entrevista[4]

    #Cargar respuestas de entrevista
    datos_respuestas = obtener_respuestas_por_entrevista(entrevista.id_entrevista)

    for dato in datos_respuestas:
    # A. Instanciamos la Pregunta con los datos obligatorios del __init__
    # __init__(self, id_pregunta, respuesta)
        nueva_pregunta = Pregunta(
            id_pregunta=dato["id_pregunta"], 
            respuesta=dato["texto_respuesta"]
        )
        
        # B. Rellenamos los atributos opcionales que no están en el __init__
        # pero que sí están en tu clase Pregunta y en la BD
        if dato["nivel"] is not None:
            nueva_pregunta.nivel = dato["nivel"]
            
        if dato["puntuacion_ia"] is not None:
            nueva_pregunta.valoracion_ia = str(dato["puntuacion_ia"]) # Lo convierto a string si tu modelo lo espera así
            
        if dato["ruta_audio"] is not None:
            nueva_pregunta.archivo_audio = dato["ruta_audio"]

        # C. Añadimos el objeto Pregunta a la lista de respuestas de la Entrevista
        entrevista.add_respuestas(nueva_pregunta)

    print(entrevista.to_json())

def reiniciar_y_generar():
    reiniciar_base_de_datos()

    generar_usuario()
    generar_internos()
    generar_solicitud()    
    generar_entrevista()
    generar_comentarios_preguntas()

if __name__ == "__main__":
    
    reiniciar_y_generar()
    
    #ver_info_completa_por_solicitud("1")                 
    
