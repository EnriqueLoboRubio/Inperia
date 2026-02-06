import sqlite3
from db.conexion import obtener_conexion

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
            fecha_inicio TEXT NOT NULL,                                
            fecha_fin TEXT NOT NULL,        
            hora_salida TEXT NOT NULL, 
            hora_llegada TEXT NOT NULL,
            destino TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            direccion TEXT NOT NULL,
            cod_pos TEXT NOT NULL,
            nombre_cp TEXT NOT NULL,
            telf_cp TEXT NOT NULL,
            relacion_cp TEXT NOT NULL,
            direccion_cp TEXTO NOT NULL,
            nombre_cs TEXT NOT NULL,
            telf_cs TEXT NOT NULL,
            relacion_cs TEXT NOT NULL,
            docs INTEGER NOT NULL,
            compromiso INTEGER NOT NULL,
            observaciones TEXT NOT NULL,
            estado TEXT NOT NULL CHECK(estado IN ('iniciada', 'pendiente', 'aceptada', 'rechazada', 'cancelada')),
            FOREIGN KEY (id_interno) REFERENCES internos(num_RC)                          
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar una nueva solicitud a la base de datos
def agregar_solicitud(id_interno, tipo, motivo, descripcion, urgencia, fecha_inicio, fecha_fin, hora_salida, hora_llegada, 
                      destino, ciudad, direccion, cod_pos, 
                      nombre_cp, telf_cp, relacion_cp, direccion_cp, nombre_cs, telf_cs, relacion_cs, 
                      docs, compromiso, observaciones, estado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:        
        cursor.execute('''
            INSERT INTO solicitudes (id_interno, tipo, motivo, descripcion, urgencia, fecha_inicio, fecha_fin, hora_salida, hora_llegada, 
                                    destino, ciudad, direccion, cod_pos, 
                                    nombre_cp, telf_cp, relacion_cp, direccion_cp, nombre_cs, telf_cs, relacion_cs, 
                                    docs, compromiso, observaciones, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id_interno, tipo, motivo, descripcion, urgencia, fecha_inicio, fecha_fin, hora_salida, hora_llegada, 
                      destino, ciudad, direccion, cod_pos, 
                      nombre_cp, telf_cp, relacion_cp, direccion_cp, nombre_cs, telf_cs, relacion_cs, 
                      docs, compromiso, observaciones, estado))
        conexion.commit()

        nuevo_id = cursor.lastrowid

    except sqlite3.IntegrityError as e:
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

# Función para borrar la tabla de solicitudes (para pruebas)
def borrar_solicitudes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS solicitudes')
    conexion.commit()
    conexion.close()


def buscar_y_mostrar_solicitud(id_interno):
    """
    Busca una solicitud pendiente o iniciada para un interno específico
    y muestra los detalles por pantalla.
    """
    print(f"\n--- 🔍 BUSCANDO SOLICITUD PARA EL INTERNO: {id_interno} ---")
    
    # Llamamos a la función importada de db/solicitud_db.py
    solicitud = encontrar_solicitud_pendiente_por_interno(id_interno)

    if solicitud:
        print("✅ Solicitud encontrada con éxito:")
        print("-" * 40)
        # Accedemos a los índices según el orden de creación en la tabla
        print(f"🆔 ID Solicitud: {solicitud[0]}")
        print(f"👤 ID Interno:   {solicitud[1]}")
        print(f"📂 Tipo:         {solicitud[2]}")
        print(f"📝 Motivo:       {solicitud[3]}")
        print(f"📄 Descripción:  {solicitud[4]}")
        print(f"🚨 Urgencia:     {solicitud[5]}")
        print(f"📅 Fecha Inicio: {solicitud[6]}")
        print(f"📍 Destino:      {solicitud[10]}")
        print(f"📊 Estado:       {solicitud[24]}") # El estado está en la última columna
        print("-" * 40)
    else:
        print(f"❌ No se encontró ninguna solicitud pendiente o iniciada para el ID {id_interno}.")    
