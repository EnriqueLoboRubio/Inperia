import sys
import os
from PyQt5.QtWidgets import QApplication

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from gui.pantalla_resumen_profesional import PantallaResumen as PantallaResumenProfesional
from gui.pantalla_resumen_interno import PantallaResumen as PantallaResumenInterno
from gui.pantalla_resumen_edit_interno import PantallaResumenEditable as PantallaResumenEditInterno


def main():
    app = QApplication(sys.argv)

    ventanaResumenProf = PantallaResumenProfesional()
    ventanaResumenInterno = PantallaResumenInterno()
    ventanaResumenEditInterno = PantallaResumenEditInterno()
    
    
    # Configuraciones 
    ventanaResumenProf.resize(1200, 900)
    ventanaResumenProf.setWindowTitle("Prueba - Pantalla Resumen Profesional")

    ventanaResumenInterno.resize(1200, 900)
    ventanaResumenInterno.setWindowTitle("Prueba - Pantalla Resumen Interno")

    ventanaResumenEditInterno.resize(1200, 900)
    ventanaResumenEditInterno.setWindowTitle("Prueba - Pantalla Resumen Editable Interno")
    

    ventanaResumenProf.show()
    #ventanaResumenInterno.show()
    #ventanaResumenEditInterno.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()