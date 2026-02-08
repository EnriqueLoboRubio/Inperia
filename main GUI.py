import sys
import os
from PyQt5.QtWidgets import QApplication

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from gui.pantalla_resumen_profesional import PantallaResumen as PantallaResumenProfesional
from gui.pantalla_resumen_interno import PantallaResumen as PantallaResumenInterno
from gui.pantalla_resumen_edit_interno import PantallaResumen as PantallaResumenEditInterno
from gui.ventana_detalle_pregunta_profesional import VentanaDetallePregunta as VentanaDetallePreguntaProfesional
from gui.ventana_detalle_pregunta_interno import VentanaDetallePregunta as VentanaDetallePreguntaInterno
from gui.ventana_detalle_edit_pregunta_interno import VentanaDetallePregunta as VentanaDetalleEditPreguntaInterno
from gui.pantalla_preguntas import PantallaPreguntas as PantallaPreguntas
from gui.pantalla_solicitud import PantallaSolicitudInterno

from models.pregunta import Pregunta
from models.comentario import Comentario


def main():
    app = QApplication(sys.argv)

    ventanaResumenProf = PantallaResumenProfesional()
    ventanaResumenInterno = PantallaResumenInterno()
    ventanaResumenEditInterno = PantallaResumenEditInterno()
    ventanaPreguntas = PantallaPreguntas()
    ventanaSolicitud = PantallaSolicitudInterno()

    #Datos para ventana detalle 
    pregunta = Pregunta(1, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    lista_comentarios = [
        Comentario("prof1", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
        Comentario("prof1", "comentario2"),
        Comentario("prof2", "comentario3")
    ]

    for c in lista_comentarios:
        pregunta.add_comentario(c)
    pregunta.nivel = 1
    pregunta.valoracion_ia = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    pregunta.set_archivo_audio(r"C:\Users\Enrique\Downloads\ROSALÍA\LUX\ROSALÍA-LUX-02-Reliquia.wav")

    VentanaDetalleProfesional = VentanaDetallePreguntaProfesional(pregunta, 1)
    VentanaDetalleInterno = VentanaDetallePreguntaInterno(pregunta, 1)
    VentanaDetalleEditInterno = VentanaDetalleEditPreguntaInterno(pregunta ,1)

    # Configuraciones 
    ventanaResumenProf.resize(1200, 900)
    ventanaResumenProf.setWindowTitle("Prueba - Pantalla Resumen Profesional")

    ventanaResumenInterno.resize(1200, 900)
    ventanaResumenInterno.setWindowTitle("Prueba - Pantalla Resumen Interno")

    ventanaResumenEditInterno.resize(1200, 900)
    ventanaResumenEditInterno.setWindowTitle("Prueba - Pantalla Resumen Editable Interno")    
    

    #ventanaResumenProf.show()
    #ventanaResumenInterno.show()
    #ventanaResumenEditInterno.show()

    VentanaDetalleProfesional.show()
    #VentanaDetalleInterno.show()
    #VentanaDetalleEditInterno.show()

    #ventanaPreguntas.show()


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()