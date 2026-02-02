from PyQt5.QtCore import pyqtSignal, QObject

from gui.interno_inicio import VentanaInterno
from gui.ventana_detalle_pregunta import VentanaDetallePregunta

from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *

from models.interno import Interno
from models.solicitud import Solicitud

class InternoController(QObject):

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana_interno = VentanaInterno()        

        self.interno = self.cargar_interno()
        self.solicitud_pendiente = self.cargar_solicitud_pendiente() 
              
        if self.interno:                       
            self.ventana_interno.cargar_datos_interno(self.interno)
            if self.solicitud_pendiente is not None:
                self.interno.add_solicitud(self.solicitud_pendiente)

        # ACTUALIZAR PANTALLA INICIO
        tiene_pendiente = self.solicitud_pendiente is not None
        self.ventana_interno.pantalla_bienvenida.actualizar_interfaz(tiene_pendiente)

        self.conectar_senales()

    # -------- CARGAR DATOS --------

    # Buscar interno por id de usuario y cargar datos
    def cargar_interno(self):
        datos_interno = encontrar_interno_por_id(self.usuario.id_usuario)
        if datos_interno:
            interno = Interno(
                id_usuario=datos_interno[0],
                nombre=self.usuario.nombre,
                email=self.usuario.email,
                contrasena=self.usuario.contrasena,
                rol=self.usuario.rol,
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
        
    #Buscar solicitud pendiente del interno
    def cargar_solicitud_pendiente(self):
        datos_solicitud = encontrar_solicitud_pendiente_por_interno(self.interno.num_RC)
        if datos_solicitud:
            solicitud = Solicitud(
                id_solicitud=datos_solicitud[0],                
                tipo=datos_solicitud[2],
                motivo=datos_solicitud[3],
                descripcion=datos_solicitud[4],
                urgencia=datos_solicitud[5]
            ) 

            solicitud.fecha_inicio = datos_solicitud[6]
            solicitud.fecha_fin = datos_solicitud[7]
            solicitud.hora_salida = datos_solicitud[8]
            solicitud.hora_llegada = datos_solicitud[9]
            solicitud.destino = datos_solicitud[10]
            solicitud.cuidad = datos_solicitud[11]
            solicitud.direccion = datos_solicitud[12]
            solicitud.cod_pos = datos_solicitud[13]

            # Contacto Principal (CP)
            solicitud.nombre_cp = datos_solicitud[14]
            solicitud.telf_cp = datos_solicitud[15]
            solicitud.relacion_cp = datos_solicitud[16]
            solicitud.direccion_cp = datos_solicitud[17]

            # Contacto Secundario (CS)
            solicitud.nombre_cs = datos_solicitud[18]
            solicitud.telf_cs = datos_solicitud[19]
            solicitud.relacion_cs = datos_solicitud[20]
            
            # Otros campos
            solicitud.observaciones = datos_solicitud[21]                                

            return solicitud
        else:
            return None


    #Buscar entrevistas del interno
    def cargar_entrevista_solicitud(self, id_solicitud):
        datos_entrevista = encontrar_entrevista_por_solicitud(id_solicitud)

    # Sin uso
    def inicio(self):
        self.ventana_interno.show()

    # -------- CONECTAR BOTONES Y ACCIONES POR PANTALLAS --------     

    def conectar_senales(self):

        # MENU LATERAL
        # Boton preguntas
        self.ventana_interno.boton_preguntas.clicked.connect(
            self.verificar_acceso_preguntas
        )        

        # PANTALLA BIENVENIDA INTERNO
        boton_inicio = self.ventana_interno.pantalla_bienvenida.boton_iniciar
               
        try: boton_inicio.clicked.disconnect()
        except: pass

        if self.solicitud_pendiente:           
            boton_inicio.clicked.connect(self.iniciar_entrevista)
        else:          
            boton_inicio.clicked.connect(self.iniciar_nueva_solicitud)

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

        #VENTANAS DE LAS PREGUNTAS
        self.ventana_interno.pantalla_resumen_profesional.grupo_botones_entrar.idClicked.connect(
            self.mostrar_detalle_pregunta
        )


    # -------- FUNCIONES DE NAVEGACIÓN --------

    def iniciar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_preguntas()  

    def iniciar_nueva_solicitud(self):
            print("Redirigiendo a nueva solicitud...")
            # Aquí debes llamar al método de tu QStackedWidget o ventana que cambie la página
            # Ejemplo: self.ventana_interno.mostrar_pantalla_solicitud() 
            pass          

    def pregunta_atras(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_atras()

    def siguiente_pregunta(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_siguiente()

    def mostrar_detalle_pregunta(self, id_pregunta):
        
        """

        """

        ventana_detalle = VentanaDetallePregunta()

    def finalizar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_resumen() 

        #Debe comprobar los datos de la entrevista: si hay algunas respuestas incompletas, mensaje de error

        # Guardarlos en el objeto Interno, creando primero el objeto Entrevista

        #

        #Y en la base de datos (aún no implementado)

    def pantalla_resumen_atras(self):
        self.ventana_interno.abrir_pregunta(10)  # Ir a la última pregunta

    def verificar_acceso_preguntas(self):
        """
        Lógica para controlar si se despliega el menú de preguntas.
        """
        if self.solicitud_pendiente is None:
            self.ventana_interno.mostrar_advertencia(
                "Sin Solicitud", 
                "No tienes una solicitud de evaluación aceptada o activa."
            )
            return
        
        if self.solicitud_pendiente.entrevista is not None:
            self.ventana_interno.mostrar_advertencia(
                "Entrevista ya realizada", 
                "Ya has completado o tienes asignada una entrevista para esta solicitud."
            )
            return
        
        self.ventana_interno.movimiento_submenu_preguntas()
