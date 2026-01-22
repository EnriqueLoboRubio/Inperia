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

    def iniciar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_preguntas()    

    def pregunta_atras(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_atras()

    def siguiente_pregunta(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_siguiente()

    def finalizar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_resumen() 