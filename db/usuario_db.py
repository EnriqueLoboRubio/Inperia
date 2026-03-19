import sqlite3
from datetime import datetime

from db.conexion import obtener_conexion
from db.fecha_utils import normalizar_fecha
from utils.encriptar import encriptar_contrasena, verificar_contrasena

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


def eliminar_usuario_admin(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def contar_administradores():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'administrador'")
        fila = cursor.fetchone()
        return int(fila[0]) if fila and fila[0] is not None else 0
    finally:
        conexion.close()


def anonimizar_usuario_admin(id_usuario, rol):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        rol_norm = str(rol or "").strip().lower()
        sello = datetime.now().strftime("%Y%m%d%H%M%S")
        email_anon = f"eliminado_{id_usuario}_{sello}@deleted.local"
        nombre_anon = f"Usuario eliminado #{id_usuario}"

        cursor.execute(
            """
            UPDATE usuarios
            SET nombre = ?, email = ?, contrasena = ?
            WHERE id = ?
            """,
            (nombre_anon, email_anon, encriptar_contrasena(f"eliminado_{id_usuario}_{sello}"), id_usuario),
        )

        if rol_norm == "interno":
            cursor.execute(
                """
                UPDATE internos
                SET situacion_legal = NULL,
                    delito = NULL,
                    condena = NULL,
                    fecha_nac = ?,
                    fecha_ingreso = NULL,
                    modulo = NULL,
                    lugar_nacimiento = NULL,
                    nombre_contacto_emergencia = NULL,
                    relacion_contacto_emergencia = NULL,
                    numero_contacto_emergencia = NULL
                WHERE id_usuario = ?
                """,
                ("1900-01-01", id_usuario),
            )
        elif rol_norm == "profesional":
            cursor.execute(
                """
                UPDATE profesionales
                SET num_colegiado = ?
                WHERE id_usuario = ?
                """,
                (-int(id_usuario), id_usuario),
            )

        conexion.commit()
        return True
    except Exception:
        conexion.rollback()
        raise
    finally:
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


def actualizar_usuario(id_usuario, nombre=None, contrasena=None):
    campos = []
    valores = []

    if nombre is not None:
        campos.append("nombre = ?")
        valores.append(nombre)

    if contrasena is not None:
        campos.append("contrasena = ?")
        valores.append(encriptar_contrasena(contrasena))

    if not campos:
        return False

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?"
        valores.append(id_usuario)
        cursor.execute(query, tuple(valores))
        conexion.commit()
        return cursor.rowcount > 0
    finally:
        conexion.close()

# Función para borrar la tabla de usuarios (para pruebas)
def listar_usuarios_admin(filtro_rol=None, texto_busqueda=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            SELECT
                u.id,
                u.nombre,
                u.email,
                u.rol,
                p.num_colegiado,
                i.num_RC,
                i.fecha_nac,
                i.modulo,
                i.situacion_legal,
                i.delito,
                i.condena,
                i.fecha_ingreso,
                i.lugar_nacimiento,
                i.nombre_contacto_emergencia,
                i.relacion_contacto_emergencia,
                i.numero_contacto_emergencia
            FROM usuarios u
            LEFT JOIN profesionales p ON p.id_usuario = u.id
            LEFT JOIN internos i ON i.id_usuario = u.id
            WHERE 1 = 1
        """
        parametros = []

        rol = str(filtro_rol or "").strip().lower()
        if rol and rol != "todos":
            query += " AND u.rol = ?"
            parametros.append(rol)

        texto = str(texto_busqueda or "").strip().lower()
        if texto:
            like = f"%{texto}%"
            query += """
                AND (
                    LOWER(u.nombre) LIKE ?
                    OR LOWER(u.email) LIKE ?
                    OR CAST(COALESCE(p.num_colegiado, '') AS TEXT) LIKE ?
                    OR CAST(COALESCE(i.num_RC, '') AS TEXT) LIKE ?
                )
            """
            parametros.extend([like, like, like, like])

        query += " ORDER BY LOWER(u.nombre) ASC, u.id ASC"
        cursor.execute(query, tuple(parametros))
        return cursor.fetchall()
    finally:
        conexion.close()


def agregar_usuario_admin(
    nombre,
    email,
    contrasena,
    rol,
    num_colegiado=None,
    num_rc=None,
    fecha_nac=None,
    situacion_legal=None,
    delito=None,
    condena=None,
    fecha_ingreso=None,
    modulo=None,
    lugar_nacimiento=None,
    nombre_contacto_emergencia=None,
    relacion_contacto_emergencia=None,
    numero_contacto_emergencia=None,
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        rol_norm = str(rol or "").strip().lower()
        cursor.execute(
            """
            INSERT INTO usuarios (nombre, email, contrasena, rol)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, email, encriptar_contrasena(contrasena), rol_norm),
        )
        id_usuario = cursor.lastrowid

        if rol_norm == "profesional":
            cursor.execute(
                """
                INSERT INTO profesionales (id_usuario, num_colegiado)
                VALUES (?, ?)
                """,
                (id_usuario, num_colegiado),
            )
        elif rol_norm == "interno":
            cursor.execute(
                """
                INSERT INTO internos (
                    num_RC, id_usuario, situacion_legal, delito, condena,
                    fecha_nac, fecha_ingreso, modulo, lugar_nacimiento,
                    nombre_contacto_emergencia, relacion_contacto_emergencia, numero_contacto_emergencia
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    num_rc,
                    id_usuario,
                    situacion_legal,
                    delito,
                    condena,
                    normalizar_fecha(fecha_nac),
                    normalizar_fecha(fecha_ingreso),
                    modulo,
                    lugar_nacimiento,
                    nombre_contacto_emergencia,
                    relacion_contacto_emergencia,
                    numero_contacto_emergencia,
                ),
            )

        conexion.commit()
        return id_usuario
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def actualizar_usuario_admin(
    id_usuario,
    nombre,
    email,
    rol,
    contrasena=None,
    num_colegiado=None,
    num_rc=None,
    fecha_nac=None,
    situacion_legal=None,
    delito=None,
    condena=None,
    fecha_ingreso=None,
    modulo=None,
    lugar_nacimiento=None,
    nombre_contacto_emergencia=None,
    relacion_contacto_emergencia=None,
    numero_contacto_emergencia=None,
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT rol FROM usuarios WHERE id = ?", (id_usuario,))
        fila = cursor.fetchone()
        if not fila:
            return False

        rol_actual = str(fila[0] or "").strip().lower()
        if rol_actual != str(rol or "").strip().lower():
            raise ValueError("No se permite cambiar el rol de un usuario existente.")

        campos = ["nombre = ?", "email = ?"]
        valores = [nombre, email]

        if contrasena:
            campos.append("contrasena = ?")
            valores.append(encriptar_contrasena(contrasena))

        valores.append(id_usuario)
        cursor.execute(
            f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?",
            tuple(valores),
        )

        if rol_actual == "profesional":
            cursor.execute(
                """
                UPDATE profesionales
                SET num_colegiado = ?
                WHERE id_usuario = ?
                """,
                (num_colegiado, id_usuario),
            )
        elif rol_actual == "interno":
            cursor.execute(
                """
                UPDATE internos
                SET num_RC = ?, situacion_legal = ?, delito = ?, condena = ?,
                    fecha_nac = ?, fecha_ingreso = ?, modulo = ?, lugar_nacimiento = ?,
                    nombre_contacto_emergencia = ?, relacion_contacto_emergencia = ?, numero_contacto_emergencia = ?
                WHERE id_usuario = ?
                """,
                (
                    num_rc,
                    situacion_legal,
                    delito,
                    condena,
                    normalizar_fecha(fecha_nac),
                    normalizar_fecha(fecha_ingreso),
                    modulo,
                    lugar_nacimiento,
                    nombre_contacto_emergencia,
                    relacion_contacto_emergencia,
                    numero_contacto_emergencia,
                    id_usuario,
                ),
            )

        conexion.commit()
        return True
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def borrar_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS usuarios')
    conexion.commit()
    conexion.close()
