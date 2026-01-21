from PyQt5.QtCore import pyqtSignal, QObject

from gui.interno_inicio import VentanaInterno

class InternoController(QObject):

    def __init__(self, interno_id):
        super().__init__()
        self.interno_id = interno_id        
        self.ventana_interno = VentanaInterno()
        self.conectar_senales()

    # Buscar interno por id y cargar datos

    def inicio(self):
        self.ventana_interno.show()

    def conectar_senales(self):

        # PANTALLA BIENVENIDA INTERNO
        self.ventana_interno.pantalla_bienvenida.boton_iniciar.clicked.connect(
            self.iniciar_entrevista
        )

        # PANTALLA PREGUNTAS
        self.ventana_interno.pantalla_preguntas.boton_atras.clicked.connect(
            self.pregunta_atras
        )

        self.ventana_interno.pantalla_preguntas.boton_siguiente.clicked.connect(
            self.siguiente_pregunta
        )
        self.ventana_interno.pantalla_preguntas.boton_finalizar.clicked.connect(
            self.finalizar_entrevista
        )

        #quitar coneziones de botones en pantalla de interno y manejar desde el controlador

    def iniciar_entrevista(self):

        self.ventana_interno.mostrar_pantalla_preguntas()    

    def pregunta_atras(self):
        pass

    def siguiente_pregunta(self):
        pass

    def finalizar_entrevista(self):
        pass