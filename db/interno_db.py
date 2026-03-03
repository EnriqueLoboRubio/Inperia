import sqlite3
from db.conexion import obtener_conexion
from db.fecha_utils import normalizar_fecha

# NOTA: en SQLite no existe tipo DATE; se guarda como TEXT en formato YYYY-MM-DD.

# -------------------------------- INTERNO ------------------------------- #


def _asegurar_columnas_extra_interno(cursor):
    columnas_nuevas = [
        "lugar_nacimiento TEXT",
        "nombre_contacto_emergencia TEXT",
        "relacion_contacto_emergencia TEXT",
        "numero_contacto_emergencia TEXT",
    ]
    for definicion in columnas_nuevas:
        try:
            cursor.execute(f"ALTER TABLE internos ADD COLUMN {definicion}")
        except sqlite3.OperationalError:
            # La columna ya existe.
            pass

# Función para crear la tabla de internos
def crear_interno():
    conexion = obtener_conexion()
    cursor = conexion.cursor()   

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internos (
            num_RC INTEGER PRIMARY KEY,
            id_usuario INTEGER NOT NULL UNIQUE,       
            situacion_legal TEXT CHECK(situacion_legal IN ('provisional', 'condenado', 'libertad_condicional')),
            delito TEXT,
            condena REAL,       
            fecha_nac TEXT NOT NULL,                       
            fecha_ingreso TEXT, 
            modulo TEXT,
            lugar_nacimiento TEXT,
            nombre_contacto_emergencia TEXT,
            relacion_contacto_emergencia TEXT,
            numero_contacto_emergencia TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE       
        )
    ''')

    _asegurar_columnas_extra_interno(cursor)

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo interno a la base de datos, vinculado a un usuario existente
def agregar_interno(
    num_rc,
    id_usuario,
    situacion,
    delito,
    condena,
    fecha_nac,
    fecha_ingreso,
    modulo,
    lugar_nacimiento=None,
    nombre_contacto_emergencia=None,
    relacion_contacto_emergencia=None,
    numero_contacto_emergencia=None,
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        fecha_nac = normalizar_fecha(fecha_nac)
        fecha_ingreso = normalizar_fecha(fecha_ingreso) if fecha_ingreso else None
        cursor.execute('''
            INSERT INTO internos (
                num_RC, id_usuario, situacion_legal, delito, condena,
                fecha_nac, fecha_ingreso, modulo, lugar_nacimiento,
                nombre_contacto_emergencia, relacion_contacto_emergencia, numero_contacto_emergencia
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            num_rc, id_usuario, situacion, delito, condena,
            fecha_nac, fecha_ingreso, modulo, lugar_nacimiento,
            nombre_contacto_emergencia, relacion_contacto_emergencia, numero_contacto_emergencia
        ))
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


def encontrar_internos_por_num_rc(lista_num_rc):
    if not lista_num_rc:
        return []

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        placeholders = ",".join(["?"] * len(lista_num_rc))
        query = f"""
            SELECT i.num_RC, i.id_usuario, i.situacion_legal, i.delito, i.condena,
                   i.fecha_nac, i.fecha_ingreso, i.modulo,
                   u.nombre, u.email, u.contrasena, u.rol,
                   i.lugar_nacimiento, i.nombre_contacto_emergencia,
                   i.relacion_contacto_emergencia, i.numero_contacto_emergencia
            FROM internos i
            INNER JOIN usuarios u ON u.id = i.id_usuario
            WHERE i.num_RC IN ({placeholders})
        """
        cursor.execute(query, tuple(lista_num_rc))
        return cursor.fetchall()
    finally:
        conexion.close()

# Función para borrar la tabla de internos (para pruebas)
def borrar_internos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS internos')
    conexion.commit()
    conexion.close()
