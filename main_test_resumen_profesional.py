import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.pantalla_resumen_profesional import PantallaResumen
from gui.ventana_detalle_pregunta_profesional import VentanaDetallePregunta
from models.pregunta import Pregunta
from models.comentario import Comentario


def crear_preguntas_mock():
    preguntas = {}
    for i in range(1, 11):
        p = Pregunta(i, f"Respuesta de ejemplo para la pregunta {i}.")
        p.nivel = (i % 5) + 1
        p.valoracion_ia = (
            f"Valoracion IA de prueba para la pregunta {i}. "
            "Este texto simula el analisis profesional."
        )
        p.add_comentario(Comentario("Enrique Lobo", "Psicologo", "Comentario de prueba 1."))
        p.add_comentario(Comentario("Marta Ruiz", "Trabajadora social", "Comentario de prueba 2."))
        p.archivo_audio = "assets/audio_mock_no_existe.wav"
        preguntas[i] = p
    return preguntas


class VentanaPruebaResumenProfesional(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba - Pantalla Resumen Profesional")
        self.resize(1400, 900)

        self.preguntas_mock = crear_preguntas_mock()
        self.pantalla = PantallaResumen()
        self.setCentralWidget(self.pantalla)

        self.pantalla.grupo_botones_entrar.idClicked.connect(self.abrir_detalle_pregunta)
        self.pantalla.boton_atras.clicked.connect(self.close)

    def abrir_detalle_pregunta(self, numero_pregunta):
        pregunta = self.preguntas_mock.get(numero_pregunta)
        if pregunta is None:
            return

        ventana = VentanaDetallePregunta(pregunta, numero_pregunta, self)
        ventana.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPruebaResumenProfesional()
    ventana.show()
    sys.exit(app.exec_())
