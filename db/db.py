import sqlite3
from utils.encriptar import encriptar_contrasena, verificar_contrasena

# -------------------------------- USUARIO ------------------------------- #

# Función para crear la tabla de usuarios
def crear_usuario():
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('profesional', 'interno'))
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(nombre, email, contrasena, rol):
    conexion = sqlite3.connect('db/usuarios.db')
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

# Función para verificar el login de un usuario, devuelve el tipo de usuario si es correcto o None si no lo es
def verificar_login(email, contrasena):
    conexion = sqlite3.connect("db/usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT contrasena, rol FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    if resultado:
        contrasena_encriptada, rol = resultado
        if verificar_contrasena(contrasena, contrasena_encriptada):
            return rol #login correcto
    return None #login incorrecto

def eliminar_usuario(email):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE email=?", (email,))
    conexion.commit()
    conexion.close()

def encontrar_usuario(email):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conexion.close()
    return usuario
