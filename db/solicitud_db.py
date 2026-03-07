import sqlite3
from db.conexion import obtener_conexion
from db.fecha_utils import normalizar_fecha

# -------------------------------- SOLICITUD ------------------------------- #

# Función para crear la tabla de solicitud
def crear_solicitud():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY,
            id_interno INTEGER NOT NULL,            
            tipo TEXT NOT NULL CHECK(tipo IN ('familiar', 'medico', 'educativo', 'laboral', 'defuncion', 'juridico')),
            motivo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            urgencia TEXT NOT NULL CHECK(urgencia IN ('normal','importante','urgente')),
            fecha_creacion TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,                                
            fecha_fin TEXT NOT NULL,        
            hora_salida TEXT NOT NULL, 
            hora_llegada TEXT NOT NULL,
            destino TEXT NOT NULL,
            provincia TEXT NOT NULL,
            direccion TEXT NOT NULL,
            cod_pos TEXT NOT NULL,
            nombre_cp TEXT NOT NULL,
            telf_cp TEXT NOT NULL,
            relacion_cp TEXT NOT NULL,
            direccion_cp TEXT NOT NULL,
            nombre_cs TEXT NOT NULL,
            telf_cs TEXT NOT NULL,
            relacion_cs TEXT NOT NULL,
            docs INTEGER NOT NULL,
            compromiso INTEGER NOT NULL,
            observaciones TEXT NOT NULL,
            conclusiones_profesional TEXT,
            id_profesional INTEGER,
            estado TEXT NOT NULL CHECK(estado IN ('iniciada', 'pendiente', 'aceptada', 'rechazada', 'cancelada')),
            FOREIGN KEY (id_interno) REFERENCES internos(num_RC) ON DELETE CASCADE,
            FOREIGN KEY (id_profesional) REFERENCES profesionales(id_usuario) ON DELETE SET NULL                          
        )
    ''')

    # Indices para acelerar filtros/ordenaciones frecuentes.
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sol_prof_estado_id
        ON solicitudes(id_profesional, estado, id DESC)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sol_prof_id
        ON solicitudes(id_profesional, id DESC)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sol_interno_id
        ON solicitudes(id_interno, id DESC)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sol_interno_estado
        ON solicitudes(id_interno, estado)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sol_sin_prof_id
        ON solicitudes(id DESC) WHERE id_profesional IS NULL
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar una nueva solicitud a la base de datos
def agregar_solicitud(id_interno, tipo, motivo, descripcion, urgencia, fecha_creacion, fecha_inicio, fecha_fin, hora_salida, hora_llegada, 
                      destino, provincia, direccion, cod_pos, 
                      nombre_cp, telf_cp, relacion_cp, direccion_cp, nombre_cs, telf_cs, relacion_cs, 
                      docs, compromiso, observaciones, estado, id_profesional=None, conclusiones_profesional=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:        
        fecha_creacion = normalizar_fecha(fecha_creacion)
        fecha_inicio = normalizar_fecha(fecha_inicio)
        fecha_fin = normalizar_fecha(fecha_fin)
        cursor.execute('''
            INSERT INTO solicitudes (id_interno, tipo, motivo, descripcion, urgencia, fecha_creacion, fecha_inicio, fecha_fin, hora_salida, hora_llegada, 
                                    destino, provincia, direccion, cod_pos, 
                                    nombre_cp, telf_cp, relacion_cp, direccion_cp, nombre_cs, telf_cs, relacion_cs, 
                                    docs, compromiso, observaciones, conclusiones_profesional, estado, id_profesional)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id_interno, tipo, motivo, descripcion, urgencia, fecha_creacion, fecha_inicio, fecha_fin, hora_salida, hora_llegada, 
                      destino, provincia, direccion, cod_pos, 
                      nombre_cp, telf_cp, relacion_cp, direccion_cp, nombre_cs, telf_cs, relacion_cs, 
                      docs, compromiso, observaciones, conclusiones_profesional, estado, id_profesional))
        conexion.commit()

        nuevo_id = cursor.lastrowid

    except (sqlite3.IntegrityError, ValueError) as e:
        print(f"Error: No se ha podido crear la solicitud. {e}")
        return None    
    finally:
        conexion.close()

    return nuevo_id

# Función para eliminar una solicitud de la base de datos
def eliminar_solicitud(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM solicitudes WHERE id=?", (id,))
    conexion.commit()
    conexion.close()

# Función para encontrar una solicitud por id
def encontrar_solicitud_por_id(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM solicitudes WHERE id=?", (id,))
    solicitud = cursor.fetchone()
    conexion.close()
    
    return solicitud

# Función para encontrar una solicitud pendiente o iniciada por id interno
def encontrar_solicitud_pendiente_por_interno(id_interno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM solicitudes WHERE id_interno=? AND estado IN ('pendiente', 'iniciada')", (id_interno,))
    solicitud = cursor.fetchone()
    conexion.close()
    
    return solicitud

def encontrar_ultima_solicitud_por_interno(id_interno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
                   "SELECT * FROM solicitudes WHERE id_interno = ? ORDER BY fecha_creacion DESC, id DESC LIMIT 1;",
                   (id_interno,))
    solicitud = cursor.fetchone()
    conexion.close()
    
    return solicitud

def contar_solicitudes_por_profesional_y_estados(id_profesional, estados):
    if not estados:
        return 0

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        placeholders = ",".join(["?"] * len(estados))
        query = f"""
            SELECT COUNT(*)
            FROM solicitudes
            WHERE id_profesional = ?
              AND estado IN ({placeholders})
        """
        cursor.execute(query, (id_profesional, *estados))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    finally:
        conexion.close()


def contar_solicitudes_por_profesional(id_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM solicitudes
            WHERE id_profesional = ?
            """,
            (id_profesional,)
        )
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    finally:
        conexion.close()


def contar_solicitudes_por_evaluar_profesional(id_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(DISTINCT s.id)
            FROM solicitudes s
            LEFT JOIN entrevistas e
              ON e.id_solicitud = s.id
            LEFT JOIN comentarios_ent ce
              ON ce.id_entrevista = e.id
             AND ce.id_profesional = s.id_profesional
            WHERE s.id_profesional = ?
              AND s.estado IN ('iniciada', 'pendiente')
              AND TRIM(COALESCE(ce.comentario_ia, '')) = ''
              AND TRIM(COALESCE(ce.comentario_profesional, '')) = ''
            """,
            (id_profesional,)
        )
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    finally:
        conexion.close()


def listar_solicitudes_nuevas_sin_profesional():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM solicitudes
            WHERE id_profesional IS NULL
            ORDER BY fecha_creacion DESC, id_interno ASC, id DESC
            """
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def listar_solicitudes_pendientes_profesional(id_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT s.*
            FROM solicitudes s
            WHERE s.id_profesional = ?
              AND s.estado = 'pendiente'
              AND EXISTS (
                  SELECT 1
                  FROM entrevistas e
                  WHERE e.id_solicitud = s.id
              )
            ORDER BY s.fecha_creacion DESC, s.id_interno ASC, s.id DESC
            """,
            (id_profesional,)
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def listar_solicitudes_profesional(id_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM solicitudes
            WHERE id_profesional = ?
            ORDER BY fecha_creacion DESC, id_interno ASC, id DESC
            """,
            (id_profesional,)
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def listar_solicitudes_por_interno(id_interno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT *
            FROM solicitudes
            WHERE id_interno = ?
            ORDER BY fecha_creacion DESC, id DESC
            """,
            (id_interno,),
        )
        return cursor.fetchall()
    finally:
        conexion.close()

# Función para borrar la tabla de solicitudes (para pruebas)
def borrar_solicitudes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS solicitudes')
    conexion.commit()
    conexion.close()


def actualizar_estado_solicitud(id_solicitud, estado):   
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            UPDATE solicitudes 
            SET estado = ?
            WHERE id = ?
        ''', (estado, id_solicitud))
        
        conexion.commit()
        return True
    except Exception as e: 
        print(f"Error: No se ha podido crear la solicitud. {e}")       
        return False
    finally:
        conexion.close()


def asignar_profesional_a_solicitud(id_solicitud, id_profesional):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            UPDATE solicitudes
            SET id_profesional = ?
            WHERE id = ?
            """,
            (id_profesional, id_solicitud)
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al asignar profesional a solicitud: {e}")
        return False
    finally:
        conexion.close()


def obtener_estado_solicitud(id_solicitud):   
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            SELECT estado           
            FROM solicitudes 
            WHERE id = ?
        ''', (id_solicitud))

        estado = cursor.fetchone()
        
        conexion.commit()
        return estado
    except Exception as e:        
        return None
    finally:
        conexion.close()
