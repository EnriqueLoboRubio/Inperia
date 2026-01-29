import sqlite3
from utils.encriptar import encriptar_contrasena, verificar_contrasena
from db.conexion import obtener_conexion

# -------------------------------- ENTREVISTA ------------------------------- #

# Función para crear la tabla de entrevistas
def crear_entrevista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrevistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_profesional TEXT NOT NULL,
            id_usuario TEXT NOT NULL,
            fecha TEXT NOT NULL,
            puntuacion_global REAL,                    
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo entrevista a la base de datos
def agregar_entrevista(id_profesional, id_usuario, fecha, puntuacion_global):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:        
        cursor.execute('''
            INSERT INTO entrevistas (id_profesional, id_usuario, fecha, puntuacion_global)
            VALUES (?, ?, ?, ?)
        ''', (id_profesional, id_usuario, fecha, puntuacion_global))
    except sqlite3.IntegrityError:
        print("Error: No se ha podido crear la entrevista")
        return False
    
    conexion.commit()
    conexion.close()
    return True

# Función para eliminar una entrevista de la base de datos
def eliminar_entrevista(email):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE email=?", (email,))
    conexion.commit()
    conexion.close()

# Función para encontrar un usuario por su email
def encontrar_usuario_por_email(email):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conexion.close()
    
    return usuario


# Función para borrar la tabla de usuarios (para pruebas)
def borrar_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS usuarios')
    conexion.commit()
    conexion.close()
