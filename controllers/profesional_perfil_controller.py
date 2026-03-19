from db.usuario_db import actualizar_usuario


class ProfesionalPerfilController:
    """
    Controlador para la gestión del perfil.
    """
    def __init__(self, controlador):
        self.controlador = controlador

    def iniciar_perfil(self):
        if not self.controlador.profesional:
            return
        self.controlador.ventana_profesional.pantalla_perfil.set_datos_usuario(
            self.controlador.profesional
        )
        self.controlador.ventana_profesional.mostrar_pantalla_perfil()

    def guardar_cambios_perfil(self):
        if not self.controlador.profesional:
            return

        datos = self.controlador.ventana_profesional.pantalla_perfil.get_datos_edicion()
        nombre_nuevo = datos["nombre"]
        nombre_original = datos["nombre_original"]
        password = datos["password"]
        password_confirm = datos["password_confirm"]

        if not nombre_nuevo:
            self.controlador.msg.mostrar_advertencia(
                "Atención", "El nombre no puede estar vacío."
            )
            return

        if password or password_confirm:
            if password != password_confirm:
                self.controlador.msg.mostrar_advertencia(
                    "Atención", "Las contraseñas no coinciden."
                )
                return

        cambio_nombre = nombre_nuevo != nombre_original
        cambio_password = bool(password)
        if not cambio_nombre and not cambio_password:
            self.controlador.msg.mostrar_advertencia(
                "Atención", "No hay cambios para guardar."
            )
            return

        ok = actualizar_usuario(
            self.controlador.profesional.id_usuario,
            nombre=nombre_nuevo if cambio_nombre else None,
            contrasena=password if cambio_password else None,
        )
        if not ok:
            self.controlador.msg.mostrar_advertencia(
                "Atención", "No se pudo actualizar el perfil."
            )
            return

        self.controlador.profesional.nombre = nombre_nuevo
        self.controlador.usuario.nombre = nombre_nuevo
        self.controlador.ventana_profesional.pantalla_bienvenida.set_profesional(
            self.controlador.profesional
        )
        self.controlador.msg.mostrar_mensaje(
            "Perfil actualizado", "Cambios guardados correctamente."
        )
