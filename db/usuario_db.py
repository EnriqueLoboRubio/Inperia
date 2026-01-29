import sqlite3
from utils.encriptar import encriptar_contrasena, verificar_contrasena
from db.conexion import obtener_conexion

# -------------------------------- USUARIO ------------------------------- #

# Función para crear la tabla de usuarios
def crear_usuario():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('profesional', 'interno', 'administrador'))
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(nombre, email, contrasena, rol):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try: 
        contrasena_encriptada = encriptar_contrasena(contrasena)
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, contrasena, rol)
            VALUES (?, ?, ?, ?)
        ''', (nombre, email, contrasena_encriptada, rol))
    except sqlite3.IntegrityError:
        print("Error: El email ya está en uso.")
        return False
    
    conexion.commit()
    conexion.close()
    return True

# Función para verificar el login de un usuario, devuelve el tipo de usuario si es correcto o None si no lo es
def verificar_login(email, contrasena):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT contrasena, rol FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    if resultado:
        contrasena_encriptada, rol = resultado
        if verificar_contrasena(contrasena, contrasena_encriptada):
            return rol #login correcto
    return None #login incorrecto

# Función para eliminar un usuario de la base de datos
def eliminar_usuario(email):
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

# Función para encontrar un usuario por su id
def encontrar_usuario_por_id(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=?", (id,))
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
