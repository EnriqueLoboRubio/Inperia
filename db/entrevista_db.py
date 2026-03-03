import sqlite3
from db.conexion import obtener_conexion
from db.respuesta_db import *
from db.fecha_utils import normalizar_fecha

# -------------------------------- ENTREVISTA ------------------------------- #

# Función para crear la tabla de entrevistas CAMBIAR ID PROFESIONAL A SU TABLA
def crear_entrevista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrevistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_interno INTEGER NOT NULL, 
            id_solicitud INTEGER NOT NULL,           
            fecha TEXT NOT NULL,
            puntuacion_global REAL,          
            FOREIGN KEY (id_interno) REFERENCES internos(num_RC) ON DELETE CASCADE,
            FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id) ON DELETE CASCADE                     
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_ent_solicitud
        ON entrevistas(id_solicitud)
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo entrevista a la base de datos, y añade las respuestas a su tabla
def agregar_entrevista(id_interno, id_solicitud, fecha):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:        
        fecha = normalizar_fecha(fecha)
        cursor.execute('''
            INSERT INTO entrevistas (id_interno, id_solicitud, fecha)
            VALUES (?, ?, ?)
        ''', (id_interno, id_solicitud, fecha))

        id_entrevista = cursor.lastrowid       

    except (sqlite3.IntegrityError, ValueError) as e:
        print(f"Error: No se ha podido crear la entrevista. {e}")
        return False
     
    
    conexion.commit()
    conexion.close()
    return id_entrevista    

# Función para agregar un nuevo entrevista a la base de datos, y añade las respuestas a su tabla
def agregar_entrevista_y_respuestas(id_interno, id_solicitud, fecha, lista_respuestas):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:        
        fecha = normalizar_fecha(fecha)
        cursor.execute('''
            INSERT INTO entrevistas (id_interno, id_solicitud, fecha)
            VALUES (?, ?, ?)
        ''', (id_interno, id_solicitud, fecha))

        id_entrevista = cursor.lastrowid

        for i, pregunta in enumerate(lista_respuestas):
            id_pregunta = i + 1
            
            cursor.execute('''
                INSERT INTO respuestas (id_entrevista, id_pregunta, texto_respuesta, ruta_audio)
                VALUES (?, ?, ?, ?)
            ''', (id_entrevista, id_pregunta, pregunta.respuesta, pregunta.archivo_audio))

    except Exception as e:
        print(f"CRITICAL ERROR DB: {e}")
        return None
     
    
    conexion.commit()
    conexion.close()
    return id_entrevista 

# Función para eliminar una entrevista de la base de datos
def eliminar_entrevista(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM entrevistas WHERE id=?", (id,))
    conexion.commit()
    conexion.close()

# Función para encontrar una entrevista por id de solicitud
def encontrar_entrevista_por_solicitud(id_solicitud):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM entrevistas WHERE id_solicitud=?", (id_solicitud,))
    entrevista = cursor.fetchone()
    conexion.commit()
    conexion.close()    
    return entrevista


def listar_ultimas_entrevistas_por_interno(id_interno, limite=5):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT
                e.id,
                e.id_solicitud,
                e.fecha,
                e.puntuacion_global,
                s.tipo,
                COALESCE(ce.comentario_profesional, ''),
                COALESCE(u.nombre, '')
            FROM entrevistas e
            LEFT JOIN solicitudes s ON s.id = e.id_solicitud
            LEFT JOIN comentarios_ent ce
              ON ce.id_entrevista = e.id
             AND ce.id_profesional = s.id_profesional
            LEFT JOIN usuarios u
              ON u.id = s.id_profesional
            WHERE e.id_interno = ?
            ORDER BY e.fecha DESC, e.id DESC
            LIMIT ?
            """,
            (id_interno, limite),
        )
        return cursor.fetchall()
    finally:
        conexion.close()

# Función para borrar la tabla de entrevistas (para pruebas)
def borrar_entrevistas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS entrevistas')
    conexion.commit()
    conexion.close()

def actualizar_puntuacion_entrevista(id, puntuacion_global):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            UPDATE entrevistas 
            SET puntuacion_global = ?,                 
            WHERE id = ?
        ''', (puntuacion_global, id))
        
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
    finally:
        conexion.close()    
