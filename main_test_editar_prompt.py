import sys

from PyQt5.QtWidgets import QApplication

from gui.ventana_detalle_edit_prompt_profesional import VentanaDetallePromptEditProfesional


def main():
    app = QApplication(sys.argv)

    numero = 1
    if len(sys.argv) > 1:
        try:
            numero = int(sys.argv[1])
        except ValueError:
            numero = 1

    ventana = VentanaDetallePromptEditProfesional(numero_pregunta=numero)
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
