import os, shutil
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog
from datetime import date

from controllers.solicitud_controller import SolicitudController

from gui.interno_inicio import VentanaInterno
from gui.ventana_detalle_edit_pregunta_interno import VentanaDetallePreguntaEdit

from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *

from models.interno import Interno
from models.solicitud import Solicitud
from models.entrevista import Entrevista
from models.pregunta import Pregunta

from utils.enums import Tipo_estado_solicitud

from gui.mensajes import Mensajes

class InternoController(QObject):

    #Señales
    logout_signal = pyqtSignal()

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana_interno = VentanaInterno()            

        self.interno = self.cargar_interno()
        self.solicitud_pedendiente_iniciada = self.cargar_solicitud_pendiente_iniciada()         
              
        if self.interno:                       
            self.ventana_interno.cargar_datos_interno(self.interno)
            if self.solicitud_pedendiente_iniciada is not None:
                self.interno.add_solicitud(self.solicitud_pedendiente_iniciada)

        self.solicitud_controller = SolicitudController(self.ventana_interno.pantalla_solicitud, self.interno.num_RC)

        # ACTUALIZAR PANTALLA INICIO
        self.tiene_pendiente_iniciada = self.solicitud_pedendiente_iniciada is not None
        self.tiene_entrevista = False
        if self.tiene_pendiente_iniciada is True:         
            self.tiene_entrevista = self.solicitud_pedendiente_iniciada.estado == Tipo_estado_solicitud.PENDIENTE  
        self.ventana_interno.pantalla_bienvenida.actualizar_interfaz(self.tiene_pendiente_iniciada, self.tiene_entrevista)
        

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
        
    #Buscar solicitud pendiente o iniciada del interno
    def cargar_solicitud_pendiente_iniciada(self):
        datos_solicitud = encontrar_solicitud_pendiente_por_interno(self.interno.num_RC)
        if datos_solicitud:
            solicitud = Solicitud()
            id_solicitud=datos_solicitud[0]               
            tipo=datos_solicitud[2]
            motivo=datos_solicitud[3]
            descripcion=datos_solicitud[4]
            urgencia=datos_solicitud[5]

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

            #solicitud.docs = datos_solicitud[21]
            #solicitud.compromisos = datos_solicitud[22]
            
            # Otros campos
            solicitud.observaciones = datos_solicitud[23]
            solicitud.estado = datos_solicitud[24]
            solicitud.entrevista = encontrar_entrevista_por_solicitud(solicitud.id_solicitud)                                                   

            return solicitud
        else:
            return None


    #Buscar entrevista del interno
    def cargar_entrevista_solicitud(self, id_solicitud):
        datos_entrevista = encontrar_entrevista_por_solicitud(id_solicitud)
        if datos_entrevista:
            entrevista = Entrevista(
                id_entrevista=datos_entrevista[0],
                id_interno=datos_entrevista[1],
                id_profesional=datos_entrevista[2],
                fecha=datos_entrevista[3]
            )

            entrevista.puntuacion = datos_entrevista[4]

            return entrevista
        else:
            return None
        
    # -------- CONECTAR BOTONES Y ACCIONES POR PANTALLAS --------     

    def conectar_senales(self):

        # MENU LATERAL
        # Boton preguntas
        self.ventana_interno.boton_preguntas.clicked.connect(
            self.verificar_acceso_preguntas
        )

        #Boton Progreso
        self.ventana_interno.boton_progreso.clicked.connect(
            self.verificar_ver_progreso
        )

        #Boton Evaluacion
        self.ventana_interno.boton_solicitud.clicked.connect(
            self.verificar_creacion_solicitud
        )

        #Boton Perfil
        self.ventana_interno.boton_usuario.clicked.connect(
            self.iniciar_perfil
        )

        #Boton Perfil (Menu)
        self.ventana_interno.boton_perfil_menu.clicked.connect(
            self.iniciar_perfil
        )
        #Boton Cerrar Sesion
        self.ventana_interno.boton_cerrar_sesion.clicked.connect(
            self.cerrar_sesion
        )        

        # PANTALLA BIENVENIDA INTERNO
        boton_inicio = self.ventana_interno.pantalla_bienvenida.boton_iniciar
               
        try: boton_inicio.clicked.disconnect()
        except: pass

        if self.tiene_pendiente_iniciada is False:
            boton_inicio.clicked.connect(self.iniciar_nueva_solicitud)                       
        elif self.tiene_entrevista is False:          
            boton_inicio.clicked.connect(self.iniciar_entrevista)
        else:
            boton_inicio.clicked.connect(self.iniciar_progreso)    

        # PANTALLA PREGUNTAS
        self.ventana_interno.pantalla_preguntas.boton_atras.clicked.connect(
            self.pregunta_atras
        )

        self.ventana_interno.pantalla_preguntas.boton_siguiente.clicked.connect(
            self.siguiente_pregunta
        )

        self.ventana_interno.pantalla_preguntas.boton_finalizar.clicked.connect(
            self.ventana_interno.pantalla_preguntas.finalizar_entrevista
        )        

        # Si la validación pasa
        self.ventana_interno.pantalla_preguntas.entrevista_finalizada.connect(
            self.finalizar_entrevista
        )        

        #PANTALLA RESUMEN ENTREVISTA
        self.ventana_interno.pantalla_resumen_edit.boton_atras.clicked.connect(
            self.pantalla_resumen_atras
        )
        
        self.ventana_interno.pantalla_resumen_edit.grupo_botones_entrar.idClicked.connect(
            self.mostrar_detalle_pregunta
        )

        #PANTALLA SOLICITUD
        self.solicitud_controller.solicitud_finalizada.connect(
            self.on_solicitud_finalizada
        )

    # -------- FUNCIONES DE NAVEGACIÓN --------

    def iniciar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_preguntas()  

    def iniciar_nueva_solicitud(self):

        self.ventana_interno.mostrar_pantalla_solicitud() 
        
    def iniciar_progreso(self):        
        self.ventana_interno.mostrar_pantalla_progreso()

    def iniciar_perfil(self):
        self.ventana_interno.mostrar_pantalla_perfil()    

    def pregunta_atras(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_atras()

    def siguiente_pregunta(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_siguiente()

    def mostrar_detalle_pregunta(self, id_pregunta):

        self.pregunta_mostrar = None

        entrevista_actual = self.solicitud_pedendiente_iniciada.entrevista
        id_entrevista = entrevista_actual.id_entrevista
        id_interno = entrevista_actual.id_interno
        
        #Buscar pregunta en el objeto Entrevista por id
        for pregunta in self.solicitud_pedendiente_iniciada.entrevista.respuestas:
            if pregunta.id_pregunta == id_pregunta:
                self.pregunta_mostrar = pregunta
                break                        

        if self.pregunta_mostrar:
            ventana_detalle = VentanaDetallePreguntaEdit(self.pregunta_mostrar, id_pregunta, id_entrevista)            
            resultado = ventana_detalle.exec_()

            if resultado == QDialog.Accepted:
                datos = ventana_detalle.get_datos()
                nuevo_texto = datos["texto"]
                ruta_temp = datos["ruta_temporal"]
                hay_nuevo_audio = datos["hay_nuevo_audio"]

                self.pregunta_mostrar.respuesta = nuevo_texto

                if hay_nuevo_audio and os.path.exists(ruta_temp):
                    carpeta_grabaciones = os.path.dirname(ruta_temp)
                    nombre_final = f"{id_interno}_{id_entrevista}_{id_pregunta}.wav"
                    ruta_final = os.path.join(carpeta_grabaciones, nombre_final)

                    try:
                        # Borrar anterior si existe
                        if os.path.exists(ruta_final):
                            os.remove(ruta_final)
                        
                        # Mover temporal a definitivo
                        shutil.move(ruta_temp, ruta_final)
                        
                        # Actualizar objeto
                        self.pregunta_mostrar.set_archivo_audio(ruta_final)
                        
                    except Exception as e:
                        print(f"Error moviendo audio: {e}")
                        msg = Mensajes(self.ventana_interno)
                        msg.mostrar_advertencia("Error", "No se pudo guardar el audio correctamente.")

                self.ventana_interno.pantalla_resumen_edit.cargar_datos_respuestas(entrevista_actual)

                msg = Mensajes(self.ventana_interno)
                msg.mostrar_mensaje(
                    "Guardado", 
                    f"La pregunta {id_pregunta} se ha actualizado correctamente."                   
                )

    def finalizar_entrevista(self, lista_respuestas, lista_audios):
        """
        Se ejecuta cuando la vista confirma que todas las preguntas están respondidas.
        Crea el objeto Entrevista y actualiza el estado.
        """
        
        # 1. Crear Objeto Entrevista
        nueva_entrevista = Entrevista(
            id_entrevista=None, # Se generará en BD
            id_interno=self.interno.num_RC,
            id_profesional=None, # Aún no asignado
            fecha=date.today().strftime("%d/%m/%Y") # Fecha de hoy
        )
        
        # Asignamos las respuestas      
        for i, (texto_res, ruta_audio) in enumerate(zip(lista_respuestas, lista_audios)):
            id_pregunta = i + 1

            obj_pregunta = Pregunta(id_pregunta, texto_res)            

            if ruta_audio:
                obj_pregunta.set_archivo_audio(ruta_audio)

            nueva_entrevista.add_respuestas(obj_pregunta)        
        
        
        # 2. Asociar a la solicitud actual
        if self.solicitud_pedendiente_iniciada:
            self.solicitud_pedendiente_iniciada.entrevista = nueva_entrevista                       

        # 3. Cambiar UI                        
        #self.tiene_entrevista = True
        
        # Ir a la pantalla de resumen
        self.ventana_interno.mostrar_pantalla_resumen()
        
        # Recargar resumen en la vista
        self.ventana_interno.pantalla_resumen_edit.cargar_datos_respuestas(nueva_entrevista)

    def pantalla_resumen_atras(self):
        self.ventana_interno.abrir_pregunta(10)  # Ir a la última pregunta

    # FUNCIONES DEL MENU

    def verificar_acceso_preguntas(self):
        """
        Lógica para controlar si se despliega el menú de preguntas.
        """
        if self.tiene_pendiente_iniciada is False:
            self.ventana_interno.mostrar_advertencia(
                "Sin Solicitud", 
                "No tiene una solicitud de evaluación iniciada o pendiente."
            )
            return
        
        if self.tiene_pendiente_iniciada is True and self.tiene_entrevista is True:
            self.ventana_interno.mostrar_advertencia(
                "Entrevista ya realizada", 
                "Ya ha completado la entrevista para esta solicitud."
            )
            return
        
        self.ventana_interno.movimiento_submenu_preguntas()

    def verificar_ver_progreso(self):
        """
        Logica: ver progreso solo si tene solicitud pendiente o iniciada
        """
        if self.tiene_pendiente_iniciada is False:
            self.ventana_interno.mostrar_advertencia(
                "Sin solicitud",
                "No tiene una solicitud de evaluación iniciada o pendiente."
            )
            return  
        else:
            self.iniciar_progreso()

    def verificar_creacion_solicitud(self):
        """
        Lógica se puede crear una nueva solicitud, solo si no tiene pendiente ni iniciada
        """        

        # tiene solicitud pendiente o iniciada
        if self.tiene_pendiente_iniciada is True:
            self.ventana_interno.mostrar_advertencia(
                "Solicitud iniciada o pendiente",
                "Tiene una solicitud iniciada o pendiente, no puede crear otra"
            )
            return  
        else:
            self.iniciar_nueva_solicitud()

    def cerrar_sesion(self):
        """
        Gestiona el intento de cierre de sesión
        """

        confirmado = self.ventana_interno.mostrar_confirmacion_logout()

        if confirmado:
            self.ventana_interno.close()
            self.logout_signal.emit()

    def on_solicitud_finalizada(self):
        # Actualizar estado interno
        self.tiene_pendiente_iniciada = True
        self.tiene_entrevista = False

        # Cambiar de pantalla
        self.ventana_interno.mostrar_pantalla_progreso()
