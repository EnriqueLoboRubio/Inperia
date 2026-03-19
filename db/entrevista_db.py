import sqlite3
from db.conexion import obtener_conexion
from db.respuesta_db import *
from db.fecha_utils import normalizar_fecha
from db.comentario_ia_entrevista_db import crear_tabla_comentarios_ia_entrevista

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
            puntuacion_ia REAL,
            puntuacion_profesional REAL,
            estado_evaluacion_ia TEXT NOT NULL DEFAULT 'sin evaluación'
                CHECK(estado_evaluacion_ia IN ('sin evaluación', 'evaluando', 'evaluada')),
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


def encontrar_entrevista_por_id(id_entrevista):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM entrevistas WHERE id=?", (id_entrevista,))
    entrevista = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return entrevista


def listar_ultimas_entrevistas_por_interno(id_interno, limite=5):
    crear_tabla_comentarios_ia_entrevista()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT
                e.id,
                e.id_solicitud,
                e.fecha,
                e.puntuacion_ia,
                s.tipo,
                COALESCE(cie.comentario_ia, ''),
                'IA'
            FROM entrevistas e
            LEFT JOIN solicitudes s ON s.id = e.id_solicitud
            LEFT JOIN comentarios_ia_ent cie
              ON cie.id_entrevista = e.id
            WHERE e.id_interno = ?
            ORDER BY
              CASE
                WHEN e.fecha GLOB '____-__-__' THEN e.fecha
                WHEN e.fecha GLOB '__/__/____' THEN substr(e.fecha, 7, 4) || '-' || substr(e.fecha, 4, 2) || '-' || substr(e.fecha, 1, 2)
                ELSE e.fecha
              END DESC,
              e.id DESC
            LIMIT ?
            """,
            (id_interno, limite),
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_ultima_entrevista_interno_profesional(id_interno, id_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT e.id, e.fecha, e.puntuacion_ia
            FROM entrevistas e
            INNER JOIN solicitudes s
              ON s.id = e.id_solicitud
            WHERE e.id_interno = ?
              AND s.id_profesional = ?
            ORDER BY
              CASE
                WHEN e.fecha GLOB '____-__-__' THEN e.fecha
                WHEN e.fecha GLOB '__/__/____' THEN substr(e.fecha, 7, 4) || '-' || substr(e.fecha, 4, 2) || '-' || substr(e.fecha, 1, 2)
                ELSE e.fecha
              END DESC,
              e.id DESC
            LIMIT 1
            """,
            (id_interno, id_profesional),
        )
        return cursor.fetchone()
    finally:
        conexion.close()


def obtener_ultima_entrevista_interno(id_interno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT e.id, e.fecha, e.puntuacion_ia
            FROM entrevistas e
            WHERE e.id_interno = ?
            ORDER BY
              CASE
                WHEN e.fecha GLOB '____-__-__' THEN e.fecha
                WHEN e.fecha GLOB '__/__/____' THEN substr(e.fecha, 7, 4) || '-' || substr(e.fecha, 4, 2) || '-' || substr(e.fecha, 1, 2)
                ELSE e.fecha
              END DESC,
              e.id DESC
            LIMIT 1
            """,
            (id_interno,),
        )
        return cursor.fetchone()
    finally:
        conexion.close()


def obtener_ultimas_entrevistas_interno(id_interno, limite=2):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT e.id, e.fecha, e.puntuacion_ia
            FROM entrevistas e
            WHERE e.id_interno = ?
            ORDER BY
              CASE
                WHEN e.fecha GLOB '____-__-__' THEN e.fecha
                WHEN e.fecha GLOB '__/__/____' THEN substr(e.fecha, 7, 4) || '-' || substr(e.fecha, 4, 2) || '-' || substr(e.fecha, 1, 2)
                ELSE e.fecha
              END DESC,
              e.id DESC
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

def actualizar_puntuacion_entrevista(id, puntuacion_ia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            UPDATE entrevistas 
            SET puntuacion_ia = ?
            WHERE id = ?
        ''', (puntuacion_ia, id))
        
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
    finally:
        conexion.close()


def actualizar_puntuacion_profesional_entrevista(id, puntuacion_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            '''
            UPDATE entrevistas
            SET puntuacion_profesional = ?
            WHERE id = ?
            ''',
            (puntuacion_profesional, id),
        )
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar puntuacion profesional: {e}")
        return False
    finally:
        conexion.close()


def actualizar_estado_evaluacion_ia_entrevista(id, estado_evaluacion_ia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            '''
            UPDATE entrevistas
            SET estado_evaluacion_ia = ?
            WHERE id = ?
            ''',
            (estado_evaluacion_ia, id),
        )
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar estado de evaluacion IA: {e}")
        return False
    finally:
        conexion.close()
