from datetime import datetime

from db.conexion import obtener_conexion


def crear_prompt():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pregunta INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            plantilla TEXT NOT NULL,
            descripcion TEXT,
            version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
            activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
            fecha_modificacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_pregunta) REFERENCES preguntas(id),
            UNIQUE (id_pregunta, version)
        )
        """
    )
    conexion.commit()
    conexion.close()


def _ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _fila_a_dict(fila):
    return {
        "id": fila[0],
        "id_pregunta": fila[1],
        "titulo": fila[2],
        "plantilla": fila[3],
        "texto": fila[3],
        "descripcion": fila[4],
        "version": fila[5],
        "activo": fila[6],
        "fecha_modificacion": fila[7],
    }


def listar_prompts(solo_activos=False, id_pregunta=None):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    where = []
    params = []
    if solo_activos:
        where.append("activo = 1")
    if id_pregunta is not None:
        where.append("id_pregunta = ?")
        params.append(int(id_pregunta))

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    cursor.execute(
        f"""
        SELECT id, id_pregunta, titulo, plantilla, descripcion, version, activo, fecha_modificacion
        FROM prompts
        {where_sql}
        ORDER BY id_pregunta ASC, version DESC, id DESC
        """,
        tuple(params),
    )
    filas = cursor.fetchall()
    conexion.close()
    return filas


def obtener_prompt_por_id(id_prompt):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT id, id_pregunta, titulo, plantilla, descripcion, version, activo, fecha_modificacion
        FROM prompts
        WHERE id = ?
        """,
        (int(id_prompt),),
    )
    fila = cursor.fetchone()
    conexion.close()
    return _fila_a_dict(fila) if fila else None


def obtener_prompt_activo_por_pregunta(id_pregunta):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT id, id_pregunta, titulo, plantilla, descripcion, version, activo, fecha_modificacion
        FROM prompts
        WHERE id_pregunta = ? AND activo = 1
        ORDER BY version DESC, id DESC
        LIMIT 1
        """,
        (int(id_pregunta),),
    )
    fila = cursor.fetchone()
    conexion.close()
    return _fila_a_dict(fila) if fila else None


def obtener_versiones_prompt_por_pregunta(id_pregunta):
    filas = listar_prompts(solo_activos=False, id_pregunta=id_pregunta)
    return [_fila_a_dict(fila) for fila in filas]


def obtener_versiones_activas_por_pregunta():
    filas = listar_prompts(solo_activos=True)
    versiones = {}
    for fila in filas:
        datos = _fila_a_dict(fila)
        # Si hubiera incoherencias y hubiese mas de una activa, se prioriza mayor version.
        id_p = int(datos["id_pregunta"])
        if id_p not in versiones or int(datos["version"]) > int(versiones[id_p]):
            versiones[id_p] = int(datos["version"])
    return versiones


def obtener_prompts_como_diccionario(solo_activos=False):
    filas = listar_prompts(solo_activos=solo_activos)
    prompts = {}
    for fila in filas:
        datos = _fila_a_dict(fila)
        if solo_activos:
            clave = str(datos["id_pregunta"])
            actual = prompts.get(clave)
            if (not actual) or int(datos["version"]) > int(actual.get("version", 0)):
                prompts[clave] = datos
        else:
            prompts[str(datos["id"])] = datos
    return prompts


def insertar_prompt(id_pregunta, titulo, plantilla, descripcion="", version=1, activo=1):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO prompts (
            id_pregunta, titulo, plantilla, descripcion, version, activo, fecha_modificacion
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            int(id_pregunta),
            str(titulo or ""),
            str(plantilla or ""),
            str(descripcion or ""),
            int(version),
            1 if activo else 0,
            _ahora(),
        ),
    )
    nuevo_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return nuevo_id


def actualizar_prompt(id_prompt, id_pregunta, titulo, plantilla, descripcion="", version=1, activo=1):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE prompts
        SET id_pregunta = ?,
            titulo = ?,
            plantilla = ?,
            descripcion = ?,
            version = ?,
            activo = ?,
            fecha_modificacion = ?
        WHERE id = ?
        """,
        (
            int(id_pregunta),
            str(titulo or ""),
            str(plantilla or ""),
            str(descripcion or ""),
            int(version),
            1 if activo else 0,
            _ahora(),
            int(id_prompt),
        ),
    )
    conexion.commit()
    filas = cursor.rowcount
    conexion.close()
    return filas > 0


def desactivar_versiones_prompt(id_pregunta, excluir_id=None):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if excluir_id is None:
        cursor.execute(
            "UPDATE prompts SET activo = 0 WHERE id_pregunta = ?",
            (int(id_pregunta),),
        )
    else:
        cursor.execute(
            "UPDATE prompts SET activo = 0 WHERE id_pregunta = ? AND id <> ?",
            (int(id_pregunta), int(excluir_id)),
        )
    conexion.commit()
    conexion.close()


def guardar_prompt_version(
    id_pregunta,
    titulo,
    plantilla,
    descripcion="",
    version=None,
    id_prompt=None,
    activar=True,
):
    crear_prompt()
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    id_pregunta = int(id_pregunta)
    titulo = str(titulo or "")
    plantilla = str(plantilla or "")
    descripcion = str(descripcion or "")
    fecha = _ahora()

    if id_prompt is not None:
        cursor.execute(
            """
            UPDATE prompts
            SET titulo = ?, plantilla = ?, descripcion = ?, fecha_modificacion = ?
            WHERE id = ? AND id_pregunta = ?
            """,
            (titulo, plantilla, descripcion, fecha, int(id_prompt), id_pregunta),
        )
        if cursor.rowcount == 0:
            conexion.rollback()
            conexion.close()
            return None
        prompt_id = int(id_prompt)
    else:
        if version is None:
            cursor.execute(
                "SELECT COALESCE(MAX(version), 0) FROM prompts WHERE id_pregunta = ?",
                (id_pregunta,),
            )
            version = int(cursor.fetchone()[0]) + 1
        else:
            version = int(version)

        cursor.execute(
            """
            INSERT INTO prompts (
                id_pregunta, titulo, plantilla, descripcion, version, activo, fecha_modificacion
            )
            VALUES (?, ?, ?, ?, ?, 0, ?)
            """,
            (id_pregunta, titulo, plantilla, descripcion, version, fecha),
        )
        prompt_id = int(cursor.lastrowid)

    if activar:
        cursor.execute("UPDATE prompts SET activo = 0 WHERE id_pregunta = ?", (id_pregunta,))
        cursor.execute("UPDATE prompts SET activo = 1 WHERE id = ?", (prompt_id,))

    conexion.commit()
    conexion.close()
    return prompt_id


def insertar_o_actualizar_prompt(id_prompt, titulo, texto, id_pregunta=None, descripcion="", version=None, activo=1):
    """
    Compatibilidad con llamadas antiguas.
    """
    if id_pregunta is None:
        id_pregunta = int(id_prompt)
    return guardar_prompt_version(
        id_pregunta=id_pregunta,
        titulo=titulo,
        plantilla=texto,
        descripcion=descripcion,
        version=version,
        id_prompt=id_prompt,
        activar=bool(activo),
    )


def borrar_prompts():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS prompts")
    conexion.commit()
    conexion.close()
