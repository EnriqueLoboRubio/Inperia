import sys
import os
from PyQt5.QtWidgets import QApplication

# Aseguramos que Python encuentre la carpeta 'gui'
# Esto añade el directorio actual al path de búsqueda de módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importamos la clase de la pantalla de bienvenida
from gui.pantalla_bienvenida_interno import PantallaBienvenidaInterno
from gui.pantalla_resumen_profesional import PantallaResumen
from gui.pantalla_preguntas import PantallaPreguntas

def main():
    app = QApplication(sys.argv)

    # Creamos la instancia de la pantalla
    ventana = PantallaResumen()
    #ventana = PantallaBienvenidaInterno()
    #ventana = PantallaPreguntas()
    
    # Configuraciones básicas de la ventana para la prueba
    ventana.resize(1200, 900) # Un tamaño razonable para ver el diseño
    ventana.setWindowTitle("Prueba - Pantalla Resumen Profesional")
    
    # Mostramos la ventana
    ventana.show()

    # Conectar el botón a una acción de prueba para verificar que funciona
    # (Esto imprimirá en la consola cuando pulses el botón)
    #ventana.boton_iniciar.clicked.connect(lambda: print("¡Botón 'Iniciar nueva entrevista' pulsado!"))

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()