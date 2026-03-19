from PyQt5.QtWidgets import QDialog

from gui.ventana_detalle_edit_pregunta_profesional import (
    VentanaDetallePreguntaEditProfesional,
)
from gui.ventana_detalle_edit_prompt_profesional import (
    VentanaDetallePromptEditProfesional,
)


class AdministradorEdicionController:
    """
    Controlador para la gestión de edición de preguntas y prompts del administrador.
    """

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar_lista_modificar_preguntas(self):
        pantalla = self.controlador.ventana_administrador.pantalla_lista_modificar_preguntas
        pantalla.cargar_preguntas()
        self.controlador.ventana_administrador.stacked_widget.setCurrentWidget(pantalla)
        self.controlador.ventana_administrador.establecer_titulo_pantalla("Modificar preguntas")

    def mostrar_lista_modificar_prompts(self):
        pantalla = self.controlador.ventana_administrador.pantalla_lista_modificar_prompt
        pantalla.cargar_prompts()
        self.controlador.ventana_administrador.stacked_widget.setCurrentWidget(pantalla)
        self.controlador.ventana_administrador.establecer_titulo_pantalla("Ajustes del modelo")

    def mostrar_detalle_editar_pregunta(self, id_pregunta):
        ventana_detalle = VentanaDetallePreguntaEditProfesional(
            numero_pregunta=id_pregunta,
            parent=self.controlador.ventana_administrador,
        )
        resultado = ventana_detalle.exec_()

        if resultado == QDialog.Accepted:
            self.controlador.ventana_administrador.pantalla_lista_modificar_preguntas.cargar_preguntas()
            self.controlador.msg.mostrar_mensaje(
                "Guardado",
                f"La pregunta {id_pregunta} se ha actualizado correctamente.",
            )

    def mostrar_detalle_editar_prompt(self, id_pregunta):
        ventana_detalle = VentanaDetallePromptEditProfesional(
            numero_pregunta=id_pregunta,
            parent=self.controlador.ventana_administrador,
        )
        resultado = ventana_detalle.exec_()

        if resultado == QDialog.Accepted:
            self.controlador.ventana_administrador.pantalla_lista_modificar_prompt.cargar_prompts()
            self.controlador.ventana_administrador.pantalla_lista_modificar_preguntas.cargar_preguntas()
            self.controlador.msg.mostrar_mensaje(
                "Guardado",
                f"El prompt asociado a la pregunta {id_pregunta} se ha actualizado correctamente.",
            )
