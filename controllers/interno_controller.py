from PyQt5.QtCore import pyqtSignal, QObject

from gui.interno_inicio import VentanaInterno

from db.interno_db import *
from models.interno import Interno

class InternoController(QObject):

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana_interno = VentanaInterno()
        self.conectar_senales()
        self.interno = self.cargar_interno()

        

    # Buscar interno por id de usuario y cargar datos
    def cargar_interno(self):
        datos_interno = encontrar_interno_por_id(self.usuario.get_id_usuario())
        if datos_interno:
            interno = Interno(
                id_usuario=datos_interno[0],
                nombre=self.usuario.get_nombre(),
                contrasena=self.usuario.get_contrasena(),
                rol=self.usuario.get_rol(),
                num_RC=datos_interno[1],
                situacion_legal=datos_interno[2],
                delito=datos_interno[3],
                fecha_nac=datos_interno[4],
                condena=datos_interno[5],
                fecha_ingreso=datos_interno[6],
                modulo=datos_interno[7]
            )
            return interno
        else:
            return None
        
    #Buscar solicitudes del interno
    def cargar_solicitudes(self):
        pass

    #Buscar entrevistas del interno
    def cargar_entrevistas(self):
        pass    

    # Sin uso
    def inicio(self):
        self.ventana_interno.show()

    def conectar_senales(self):

        #PANTALLA INICIO

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

        #PANTALLA RESUMEN ENTREVISTA
        self.ventana_interno.pantalla_resumen_profesional.boton_atras.clicked.connect(
            self.pantalla_resumen_atras
        )
        
                



    def iniciar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_preguntas()    

    def pregunta_atras(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_atras()

    def siguiente_pregunta(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_siguiente()

    def finalizar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_resumen() 

        #Debe comprobar los datos de la entrevista: si hay algunas respuestas incompletas, mensaje de error

        # Guardarlos en el objeto Interno, creando primero el objeto Entrevista

        #

        #Y en la base de datos (aún no implementado)

    def pantalla_resumen_atras(self):
        self.ventana_interno.abrir_pregunta(10)  # Ir a la última pregunta
