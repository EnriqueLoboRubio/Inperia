import sqlite3
from db.conexion import obtener_conexion

# -------------------------------- RESPUESTA ------------------------------- #

# Función para crear la tabla de respuestas
def crear_respuesta():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entrevista INTEGER NOT NULL,
            id_pregunta INTEGER NOT NULL,
            texto_respuesta TEXT,            
            ruta_audio TEXT,
            puntuacion_ia REAL,
            nivel INTEGER,                          
            FOREIGN KEY (id_entrevista) REFERENCES entrevistas(id) ON DELETE CASCADE
        )
    ''')

    conexion.commit()
    conexion.close()

#Función para agregar nueva respuesta
def agregar_respuesta(id_entrevista, id_pregunta, texto_respuesta, ruta_audio, puntacion_ia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute('''
            INSERT INTO respuestas (id_entrevista, id_pregunta, texto_respuesta, ruta_audio, puntacion_ia)
            VALUES (?,?,?,?)
        ''', (id_entrevista, id_pregunta, texto_respuesta, ruta_audio, puntacion_ia))
    except sqlite3.IntegrityError:
        print("ERror: No se ha podido crear la respuesta")
        return False

    conexion.commit()
    conexion.close()
    return True

def actualizar_puntuacion_respuesta(id_entrevista, id_pregunta, puntuacion_ia, nivel):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            UPDATE respuestas 
            SET puntuacion_ia = ?, 
                nivel = ?
            WHERE id_entrevista = ? AND id_pregunta = ?
        ''', (puntuacion_ia, nivel, id_entrevista, id_pregunta))
        
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
    finally:
        conexion.close()

def obtener_respuestas_por_entrevista(id_entrevista):
    """
    Recupera todas las respuestas asociadas a una entrevista.
    Devuelve una lista de diccionarios con los datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:      
        cursor.execute('''
            SELECT id_pregunta, texto_respuesta, ruta_audio, puntuacion_ia, nivel 
            FROM respuestas 
            WHERE id_entrevista = ?
        ''', (id_entrevista,))
        
        filas = cursor.fetchall()
        
        lista_respuestas = []
        
        for fila in filas:            
            datos = {
                "id_pregunta": fila[0],
                "texto_respuesta": fila[1],
                "ruta_audio": fila[2],
                "puntuacion_ia": fila[3],
                "nivel": fila[4]
            }
            lista_respuestas.append(datos)
            
        return lista_respuestas

    except Exception as e:
        print(f"Error al obtener respuestas: {e}")
        return []
    finally:
        conexion.close()        

# Función para borrar la tabla de respuesta (para pruebas)
def borrar_respuestas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS respuestas')
    conexion.commit()
    conexion.close()        
    
    