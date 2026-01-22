import sqlite3
from db.conexion import obtener_conexion

# NOTA: no existe el tipo Date, por lo que se usa TEXT. Fechas en formato 'DD-MM-YYYY'

# -------------------------------- INTERNO ------------------------------- #

# Función para crear la tabla de internos
def crear_interno():
    conexion = obtener_conexion()
    cursor = conexion.cursor()   

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internos (
            num_RC INTEGER PRIMARY KEY,
            id_usuario INTEGER NOT NULL,       
            situacion_legal TEXT CHECK(situacion_legal IN ('provisional', 'condenado', 'libertad_condicional')),
            delito TEXT,
            condena REAL,       
            fecha_nac TEXT NOT NULL,                       
            fecha_ingreso TEXT, 
            modulo TEXT,       
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE       
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo interno a la base de datos, vinculado a un usuario existente
def agregar_interno(num_rc, id_usuario, situacion, delito, condena, fecha_nac, fecha_ingreso, modulo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO internos (num_RC, id_usuario, situacion_legal, delito, condena, fecha_nac, fecha_ingreso, modulo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (num_rc, id_usuario, situacion, delito, condena, fecha_nac, fecha_ingreso, modulo))
        conexion.commit()
        exito = True
    except sqlite3.IntegrityError as e:
        exito = False
    finally:
        conexion.close()
    
    return exito


# Función para eliminar un interno de la base de datos
def eliminar_interno_por_id(id_usuario):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try: 
        cursor.execute("DELETE FROM internos WHERE id_usuario=?", (id_usuario,))
        conexion.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        conexion.close()
    

# Función para encontrar interno por id de usuario
def encontrar_interno_por_id(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM internos WHERE id_usuario=?", (id_usuario,))
    interno = cursor.fetchone()
    conexion.close()
    return interno

# Función para borrar la tabla de internos (para pruebas)
def borrar_internos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS internos')
    conexion.commit()
    conexion.close()
