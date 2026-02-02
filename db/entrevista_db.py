import sqlite3
from db.conexion import obtener_conexion

# -------------------------------- ENTREVISTA ------------------------------- #

# Función para crear la tabla de entrevistas CAMBIAR ID PROFESIONAL A SU TABLA
def crear_entrevista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrevistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_profesional INTEGER,
            id_interno INTEGER NOT NULL, 
            id_solicitud INTEGER NOT NULL,           
            fecha TEXT NOT NULL,
            puntuacion_global REAL,          
            FOREIGN KEY (id_interno) REFERENCES internos(num_RC),
            FOREIGN KEY (id_profesional) REFERENCES usuarios(id),
            FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id)                     
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo entrevista a la base de datos
def agregar_entrevista(id_profesional, id_interno, id_solicitud, fecha, puntuacion_global):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:        
        cursor.execute('''
            INSERT INTO entrevistas (id_profesional, id_interno, id_solicitud, fecha, puntuacion_global)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_profesional, id_interno, id_solicitud, fecha, puntuacion_global))
    except sqlite3.IntegrityError:
        print("Error: No se ha podido crear la entrevista")
        return False
    
    conexion.commit()
    conexion.close()
    return True

# Función para eliminar una entrevista de la base de datos
def eliminar_entrevista(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM entrevista WHERE id=?", (id,))
    conexion.commit()
    conexion.close()

# Función para encontrar una entrevista por id de solicitud
def encontrar_entrevista_por_solicitud(id_solicitud):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM entrevista WHERE id_solicitud=?", (id_solicitud,))
    conexion.commit()
    conexion.close()    

# Función para borrar la tabla de entrevistas (para pruebas)
def borrar_entrevista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS entrevistas')
    conexion.commit()
    conexion.close()
