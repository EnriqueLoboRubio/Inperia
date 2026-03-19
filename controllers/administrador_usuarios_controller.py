import re

from PyQt5.QtWidgets import QDialog

from db.usuario_db import (
    actualizar_usuario_admin,
    agregar_usuario_admin,
    anonimizar_usuario_admin,
    contar_administradores,
    eliminar_usuario_admin,
    listar_usuarios_admin,
)
from gui.ventana_usuario_administrador import VentanaUsuarioAdministrador
from utils.enums import Tipo_situacion_legal
from db.solicitud_db import listar_solicitudes_profesional


class AdministradorUsuariosController:
    """
    Controlador para la gestión de usuarios del administrador.
    """

    RELACIONES_CONTACTO = [
        "Seleccionar...",
        "Padre/Madre",
        "Hermano/a",
        "Esposo/a",
        "Hijo/a",
        "Otro",
    ]

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar_lista_usuarios(self):
        self.recargar_lista()
        pantalla = self.controlador.ventana_administrador.pantalla_lista_usuarios
        self.controlador.ventana_administrador.stacked_widget.setCurrentWidget(pantalla)
        self.controlador.ventana_administrador.establecer_titulo_pantalla("Usuarios")

    def recargar_lista(self):
        pantalla = self.controlador.ventana_administrador.pantalla_lista_usuarios
        filtros = pantalla.obtener_filtros()
        filas = listar_usuarios_admin(
            filtro_rol=filtros.get("rol"),
            texto_busqueda=filtros.get("texto"),
        )
        usuarios = [self._fila_a_dict(fila) for fila in filas]
        pantalla.cargar_datos(usuarios)

    def abrir_creacion_usuario(self):
        ventana = VentanaUsuarioAdministrador(
            parent=self.controlador.ventana_administrador,
            situacion_legal_opciones=self._obtener_situaciones_legales(),
            relacion_contacto_opciones=self.RELACIONES_CONTACTO,
            permitir_eliminacion=False,
        )
        if ventana.exec_() != QDialog.Accepted:
            return

        datos = ventana.get_datos()
        if not self._validar_datos(datos, es_edicion=False):
            return

        try:
            agregar_usuario_admin(
                nombre=datos["nombre"],
                email=datos["email"],
                contrasena=datos["password"],
                rol=datos["rol"],
                num_colegiado=int(datos["num_colegiado"]) if datos["rol"] == "profesional" else None,
                num_rc=int(datos["num_rc"]) if datos["rol"] == "interno" else None,
                fecha_nac=datos["fecha_nac"] if datos["rol"] == "interno" else None,
                situacion_legal=datos["situacion_legal"] if datos["rol"] == "interno" else None,
                delito=datos["delito"] if datos["rol"] == "interno" else None,
                condena=datos["condena"] if datos["rol"] == "interno" else None,
                fecha_ingreso=datos["fecha_ingreso"] if datos["rol"] == "interno" else None,
                modulo=datos["modulo"] if datos["rol"] == "interno" else None,
                lugar_nacimiento=datos["lugar_nacimiento"] if datos["rol"] == "interno" else None,
                nombre_contacto_emergencia=datos["nombre_contacto_emergencia"] if datos["rol"] == "interno" else None,
                relacion_contacto_emergencia=datos["relacion_contacto_emergencia"] if datos["rol"] == "interno" else None,
                numero_contacto_emergencia=datos["numero_contacto_emergencia"] if datos["rol"] == "interno" else None,
            )
        except Exception as e:
            self.controlador.msg.mostrar_advertencia("Atención", f"No se pudo crear el usuario.\n{str(e)}")
            return

        self.controlador.msg.mostrar_mensaje("Usuario creado", "El usuario se ha creado correctamente.")
        self.mostrar_lista_usuarios()

    def abrir_edicion_usuario(self, usuario):
        ventana = VentanaUsuarioAdministrador(
            usuario=usuario,
            parent=self.controlador.ventana_administrador,
            situacion_legal_opciones=self._obtener_situaciones_legales(),
            relacion_contacto_opciones=self.RELACIONES_CONTACTO,
            permitir_eliminacion=self._puede_eliminar_usuario(usuario),
        )
        if ventana.exec_() != QDialog.Accepted:
            return

        if ventana.accion_solicitada() == "eliminar":
            if not self._eliminar_o_anonimizar_usuario(usuario):
                return
            self.mostrar_lista_usuarios()
            return

        datos = ventana.get_datos()
        if not self._validar_datos(datos, es_edicion=True):
            return

        try:
            actualizar_usuario_admin(
                id_usuario=datos["id_usuario"],
                nombre=datos["nombre"],
                email=datos["email"],
                rol=datos["rol"],
                contrasena=datos["password"] or None,
                num_colegiado=int(datos["num_colegiado"]) if datos["rol"] == "profesional" else None,
                num_rc=int(datos["num_rc"]) if datos["rol"] == "interno" else None,
                fecha_nac=datos["fecha_nac"] if datos["rol"] == "interno" else None,
                situacion_legal=datos["situacion_legal"] if datos["rol"] == "interno" else None,
                delito=datos["delito"] if datos["rol"] == "interno" else None,
                condena=datos["condena"] if datos["rol"] == "interno" else None,
                fecha_ingreso=datos["fecha_ingreso"] if datos["rol"] == "interno" else None,
                modulo=datos["modulo"] if datos["rol"] == "interno" else None,
                lugar_nacimiento=datos["lugar_nacimiento"] if datos["rol"] == "interno" else None,
                nombre_contacto_emergencia=datos["nombre_contacto_emergencia"] if datos["rol"] == "interno" else None,
                relacion_contacto_emergencia=datos["relacion_contacto_emergencia"] if datos["rol"] == "interno" else None,
                numero_contacto_emergencia=datos["numero_contacto_emergencia"] if datos["rol"] == "interno" else None,
            )
        except Exception as e:
            self.controlador.msg.mostrar_advertencia("Atención", f"No se pudo actualizar el usuario.\n{str(e)}")
            return

        self.controlador.msg.mostrar_mensaje("Usuario actualizado", "Los cambios se han guardado correctamente.")
        self.mostrar_lista_usuarios()

    def mostrar_perfil_profesional(self, usuario):
        if str(usuario.get("rol", "") or "").strip().lower() != "profesional":
            return

        self.controlador._vista_origen_perfil_profesional_admin = (
            self.controlador.ventana_administrador.stacked_widget.currentWidget()
        )
        self.controlador._titulo_origen_perfil_profesional_admin = (
            self.controlador.ventana_administrador.titulo_pantalla.text()
        )

        filas = listar_solicitudes_profesional(usuario.get("id_usuario"))
        solicitudes = [
            self.controlador.internos._construir_solicitud_desde_fila(fila)
            for fila in (filas or [])
        ]
        internos = self.controlador.internos.cargar_internos_para_solicitudes(solicitudes)

        pantalla = self.controlador.ventana_administrador.pantalla_lista_solicitudes_profesional
        pantalla.cargar_datos(solicitudes, internos)
        pantalla.aplicar_filtro_inicial(
            top_activo=None,
            combo_texto="Todos",
            modo_historial=False,
            mostrar_filtros_superiores=False,
            mostrar_boton_volver=True,
        )
        self.controlador.ventana_administrador.stacked_widget.setCurrentWidget(pantalla)
        nombre = str(usuario.get("nombre", "") or "Profesional").strip()
        self.controlador.ventana_administrador.establecer_titulo_pantalla(f"Perfil profesional: {nombre}")

    def volver_desde_perfil_profesional(self):
        widget = getattr(self.controlador, "_vista_origen_perfil_profesional_admin", None)
        titulo = getattr(self.controlador, "_titulo_origen_perfil_profesional_admin", "Usuarios")
        if widget is not None:
            self.controlador.ventana_administrador.stacked_widget.setCurrentWidget(widget)
            self.controlador.ventana_administrador.establecer_titulo_pantalla(titulo)
            return
        self.mostrar_lista_usuarios()

    def _validar_datos(self, datos, es_edicion):
        nombre = str(datos.get("nombre", "")).strip()
        email = str(datos.get("email", "")).strip()
        password = str(datos.get("password", ""))
        password_confirm = str(datos.get("password_confirm", ""))
        rol = str(datos.get("rol", "")).strip().lower()

        if not nombre or not email:
            self.controlador.msg.mostrar_advertencia("Atención", "Nombre y email son obligatorios.")
            return False

        if not self._validar_email(email):
            self.controlador.msg.mostrar_advertencia("Atención", "El formato del email no es válido.")
            return False

        if not es_edicion and not password:
            self.controlador.msg.mostrar_advertencia("Atención", "Debe indicar una contraseña.")
            return False

        if password or password_confirm:
            if password != password_confirm:
                self.controlador.msg.mostrar_advertencia("Atención", "Las contraseñas no coinciden.")
                return False

        if rol == "profesional" and not str(datos.get("num_colegiado", "")).strip():
            self.controlador.msg.mostrar_advertencia("Atención", "Debe indicar el número de colegiado.")
            return False

        if rol == "interno":
            obligatorios = {
                "num_rc": "el número de recluso",
                "fecha_nac": "la fecha de nacimiento",
                "situacion_legal": "la situación legal",
                "delito": "el delito",
                "condena": "la duración de condena",
                "fecha_ingreso": "la fecha de ingreso",
                "modulo": "el módulo",
                "lugar_nacimiento": "el lugar de nacimiento",
                "nombre_contacto_emergencia": "el nombre del contacto de emergencia",
                "relacion_contacto_emergencia": "la relación del contacto de emergencia",
                "numero_contacto_emergencia": "el número de teléfono del contacto de emergencia",
            }
            faltan = []
            for clave, etiqueta in obligatorios.items():
                valor = str(datos.get(clave, "")).strip()
                if not valor or valor == "Seleccionar...":
                    faltan.append(etiqueta)

            if faltan:
                self.controlador.msg.mostrar_advertencia(
                    "Atención",
                    "Para internos faltan estos campos obligatorios:\n- " + "\n- ".join(faltan),
                )
                return False

        return True

    @staticmethod
    def _validar_email(correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        return re.match(patron, correo) is not None

    def _eliminar_o_anonimizar_usuario(self, usuario):
        id_usuario = usuario.get("id_usuario")
        rol = str(usuario.get("rol", "") or "").strip().lower()

        if rol == "administrador" and not self._puede_eliminar_usuario(usuario):
            self.controlador.msg.mostrar_advertencia(
                "Atención",
                "No se puede borrar este administrador porque debe permanecer al menos un administrador en la aplicación."
            )
            return False

        if rol == "interno":
            decision = self.controlador.msg.mostrar_decision_eliminacion(
                "Borrar usuario interno",
                "¿Qué desea hacer con este interno?\n\n"
                "Si elige eliminar, se borrarán también la solicitud, entrevistas y comentarios asociados.\n"
                "Si elige anonimizar, se conservarán esos datos pero sin mantener la identidad personal.",
                "Eliminar",
                "Anonimizar"
            )
            if decision == "cancelar":
                return False
            try:
                if decision == "confirmar":
                    eliminado = eliminar_usuario_admin(id_usuario)
                    if not eliminado:
                        self.controlador.msg.mostrar_advertencia("Atención", "No se encontró el usuario a borrar.")
                        return False
                    self.controlador.msg.mostrar_mensaje(
                        "Usuario borrado",
                        "El interno y todos sus datos asociados se han eliminado correctamente."
                    )
                    return True

                anonimizar_usuario_admin(id_usuario, rol)
                self.controlador.msg.mostrar_mensaje(
                    "Usuario anonimizado",
                    "El interno se ha anonimizado y se han conservado sus solicitudes y entrevistas."
                )
                return True
            except Exception as e:
                self.controlador.msg.mostrar_advertencia(
                    "Atención",
                    f"No se pudo completar la operación sobre el interno.\n{str(e)}"
                )
                return False

        try:
            eliminado = eliminar_usuario_admin(id_usuario)
            if not eliminado:
                self.controlador.msg.mostrar_advertencia("Atención", "No se encontró el usuario a borrar.")
                return False
            self.controlador.msg.mostrar_mensaje("Usuario borrado", "El usuario se ha eliminado correctamente.")
            return True
        except Exception as e:
            if rol == "profesional":
                anonimizar = self.controlador.msg.mostrar_confirmacion(
                    "No se puede borrar el profesional",
                    "El profesional tiene datos relacionados que impiden el borrado.\n\n"
                    "¿Desea anonimizarlo para conservar comentarios y referencias sin mantener sus datos personales?"
                )
                if not anonimizar:
                    return False
                try:
                    anonimizar_usuario_admin(id_usuario, rol)
                    self.controlador.msg.mostrar_mensaje(
                        "Profesional anonimizado",
                        "El profesional se ha anonimizado y se han conservado sus referencias asociadas."
                    )
                    return True
                except Exception as error_anon:
                    self.controlador.msg.mostrar_advertencia(
                        "Atención",
                        f"No se pudo anonimizar el profesional.\n{str(error_anon)}"
                    )
                    return False

            self.controlador.msg.mostrar_advertencia(
                "Atención",
                f"No se pudo borrar el usuario.\n{str(e)}"
            )
            return False

    @staticmethod
    def _obtener_situaciones_legales():
        return [opcion.value for opcion in Tipo_situacion_legal]

    @staticmethod
    def _puede_eliminar_usuario(usuario):
        rol = str(usuario.get("rol", "") or "").strip().lower()
        if rol != "administrador":
            return True
        return contar_administradores() > 1

    @staticmethod
    def _fila_a_dict(fila):
        return {
            "id_usuario": fila[0],
            "nombre": fila[1],
            "email": fila[2],
            "rol": fila[3],
            "num_colegiado": fila[4],
            "num_rc": fila[5],
            "fecha_nac": fila[6],
            "modulo": fila[7],
            "situacion_legal": fila[8],
            "delito": fila[9],
            "condena": fila[10],
            "fecha_ingreso": fila[11],
            "lugar_nacimiento": fila[12],
            "nombre_contacto_emergencia": fila[13],
            "relacion_contacto_emergencia": fila[14],
            "numero_contacto_emergencia": fila[15],
        }
