from utils.enums import Tipo_estado_solicitud
from db.solicitud_db import (
    contar_solicitudes_por_evaluar_profesional,
    contar_solicitudes_por_profesional,
    contar_solicitudes_por_profesional_y_estados,
)


class ProfesionalNavegacionController:
    """
    Controlador para la gestión de la navegación.
    """
    def __init__(self, controlador):
        self.controlador = controlador

    def actualizar_inicio_profesional(self):
        if not self.controlador.profesional:
            return

        num_pendientes = contar_solicitudes_por_evaluar_profesional(
            self.controlador.profesional.id_usuario
        )
        num_completadas = contar_solicitudes_por_profesional_y_estados(
            self.controlador.profesional.id_usuario,
            [
                Tipo_estado_solicitud.ACEPTADA.value,
                Tipo_estado_solicitud.RECHAZADA.value,
                Tipo_estado_solicitud.CANCELADA.value,
            ],
        )
        num_historial = contar_solicitudes_por_profesional(
            self.controlador.profesional.id_usuario
        )

        self.controlador.ventana_profesional.actualizar_interfaz_inicio(
            num_pendientes,
            num_completadas,
            num_historial,
        )
        self.controlador.ventana_profesional.pantalla_bienvenida.boton_historial_solicitudes.setVisible(
            num_historial > 0
        )

    def cerrar_sesion(self):
        confirmado = self.controlador.ventana_profesional.mostrar_confirmacion_logout()
        if confirmado:
            self.controlador.ventana_profesional.close()
            self.controlador.logout_signal.emit()
