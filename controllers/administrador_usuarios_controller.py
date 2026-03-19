import re

from PyQt5.QtWidgets import QDialog

from db.usuario_db import (
    actualizar_usuario_admin,
    agregar_usuario_admin,
    listar_usuarios_admin,
)
from gui.ventana_usuario_administrador import VentanaUsuarioAdministrador


class AdministradorUsuariosController:
    """
    Controlador para la gestión de usuarios del administrador.
    """

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
        ventana = VentanaUsuarioAdministrador(parent=self.controlador.ventana_administrador)
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
            )
        except Exception as e:
            self.controlador.msg.mostrar_advertencia("Atención", f"No se pudo crear el usuario.\n{str(e)}")
            return

        self.controlador.msg.mostrar_mensaje("Usuario creado", "El usuario se ha creado correctamente.")
        self.mostrar_lista_usuarios()

    def abrir_edicion_usuario(self, usuario):
        ventana = VentanaUsuarioAdministrador(usuario=usuario, parent=self.controlador.ventana_administrador)
        if ventana.exec_() != QDialog.Accepted:
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
            )
        except Exception as e:
            self.controlador.msg.mostrar_advertencia("Atención", f"No se pudo actualizar el usuario.\n{str(e)}")
            return

        self.controlador.msg.mostrar_mensaje("Usuario actualizado", "Los cambios se han guardado correctamente.")
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
            if not str(datos.get("num_rc", "")).strip() or not str(datos.get("fecha_nac", "")).strip():
                self.controlador.msg.mostrar_advertencia(
                    "Atención", "Para internos son obligatorios el número de recluso y la fecha de nacimiento."
                )
                return False

        return True

    @staticmethod
    def _validar_email(correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        return re.match(patron, correo) is not None

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
        }
