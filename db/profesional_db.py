import sqlite3
from db.conexion import obtener_conexion

# -------------------------------- PROFESIONAL ------------------------------- #

# Función para crear la tabla de profesionales
def crear_profesional():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE profesionales (
            id_usuario INTEGER PRIMARY KEY,
            num_colegiado INTEGER UNIQUE NOT NULL ,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo profesional a la base de datos, vinculado a un usuario existente
def agregar_profesional(id_usuario, num_colegiado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO profesionales (id_usuario, num_colegiado)
            VALUES (?, ?)
        ''', (id_usuario, num_colegiado))
        conexion.commit()
        exito = True
    except sqlite3.IntegrityError as e:
        exito = False
    finally:
        conexion.close()
    
    return exito

# Función para encontrar un profesional por su id de usuario
def encontrar_profesional_por_id(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT num_colegiado FROM profesionales WHERE id_usuario=?', (id_usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

# Función para borrar la tabla de profesionales
def eliminar_profesional():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS profesionales')
    conexion.commit()
    conexion.close()