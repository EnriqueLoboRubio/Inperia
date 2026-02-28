import os, shutil
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog
from datetime import date

from controllers.solicitud_controller import SolicitudController
from controllers.progreso_controller import ProgresoController

from gui.interno_inicio import VentanaInterno
from gui.ventana_detalle_edit_pregunta_interno import VentanaDetallePreguntaEdit
from gui.ventana_detalle_pregunta_interno import VentanaDetallePregunta

from db.interno_db import *
from db.solicitud_db import *
from db.entrevista_db import *
from db.usuario_db import actualizar_usuario

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
        self.solicitud_actual = self.cargar_ultima_solicitud()         
              
        if self.interno:                       
            self.ventana_interno.cargar_datos_interno(self.interno)
            if self.solicitud_actual is not None:
                self.interno.add_solicitud(self.solicitud_actual)

        self.solicitud_controller = SolicitudController(self.ventana_interno.pantalla_solicitud, self.interno.num_RC)
        self.progreso_controller = ProgresoController(self.ventana_interno.pantalla_progreso, self.solicitud_actual, self.interno)

        # ACTUALIZAR PANTALLA INICIO
        self.tiene_solicitud = self.solicitud_actual is not None
        self.tiene_entrevista = False
        self.tiene_entrevista = (
            self.tiene_solicitud and 
            self.solicitud_actual.estado == Tipo_estado_solicitud.PENDIENTE.value
        )
        estado_solicitud = self.solicitud_actual.estado if self.solicitud_actual else None
        self.ventana_interno.pantalla_bienvenida.actualizar_interfaz(
            self.tiene_solicitud,
            self.tiene_entrevista,
            estado_solicitud
        )
        
        self.msg = Mensajes(self.ventana_interno)

        self.conectar_senales()

    # -------- CARGAR DATOS --------

    # Buscar interno por id de usuario y cargar datos
    def cargar_interno(self):
        datos_interno = encontrar_interno_por_id(self.usuario.id_usuario)
        if datos_interno:
            interno = Interno(
                id_usuario=self.usuario.id_usuario,
                nombre=self.usuario.nombre,
                email=self.usuario.email,
                contrasena=self.usuario.contrasena,
                rol=self.usuario.rol,
                num_RC=datos_interno[0],
                situacion_legal=datos_interno[2],
                delito=datos_interno[3],
                fecha_nac=datos_interno[5],
                condena=datos_interno[4],
                fecha_ingreso=datos_interno[6],
                modulo=datos_interno[7]
            )
            return interno
        else:
            return None
        
    def cargar_ultima_solicitud(self):
        datos_solicitud = encontrar_ultima_solicitud_por_interno(self.interno.num_RC)
        if datos_solicitud:
            solicitud = Solicitud()
            solicitud.id_solicitud=datos_solicitud[0]               
            solicitud.tipo=datos_solicitud[2]
            solicitud.motivo=datos_solicitud[3]
            solicitud.descripcion=datos_solicitud[4]
            solicitud.urgencia=datos_solicitud[5]
            solicitud.fecha_creacion = datos_solicitud[6]

            solicitud.fecha_inicio = datos_solicitud[7]
            solicitud.fecha_fin = datos_solicitud[8]
            solicitud.hora_salida = datos_solicitud[9]
            solicitud.hora_llegada = datos_solicitud[10]
            solicitud.destino = datos_solicitud[11]
            solicitud.provincia = datos_solicitud[12]
            solicitud.direccion = datos_solicitud[13]
            solicitud.cod_pos = datos_solicitud[14]

            # Contacto Principal (CP)
            solicitud.nombre_cp = datos_solicitud[15]
            solicitud.telf_cp = datos_solicitud[16]
            solicitud.relacion_cp = datos_solicitud[17]
            solicitud.direccion_cp = datos_solicitud[18]

            # Contacto Secundario (CS)
            solicitud.nombre_cs = datos_solicitud[19]
            solicitud.telf_cs = datos_solicitud[20]
            solicitud.relacion_cs = datos_solicitud[21]

            solicitud.docs = datos_solicitud[22]
            solicitud.compromisos = datos_solicitud[23]
            
            # Otros campos
            solicitud.observaciones = datos_solicitud[24]
            solicitud.conclusiones_profesional = datos_solicitud[25]
            solicitud.id_profesional = datos_solicitud[26]
            solicitud.estado = datos_solicitud[27]
            solicitud.evaluacion_automatica = datos_solicitud[28] if len(datos_solicitud) > 28 else ""
            solicitud.entrevista = self.cargar_entrevista_solicitud(solicitud.id_solicitud)                                                   

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
                fecha=datos_entrevista[3]
            )

            entrevista.puntuacion = datos_entrevista[4]

            # Cargar respuestas de entrevista
            if entrevista:
                datos_respuestas = obtener_respuestas_por_entrevista(entrevista.id_entrevista)

                for dato in datos_respuestas:
                    nueva_pregunta = Pregunta(
                        id_pregunta=dato["id_pregunta"], 
                        respuesta=dato["texto_respuesta"]
                    )
                    nueva_pregunta.set_archivo_audio(dato["ruta_audio"])
                    entrevista.add_respuestas(nueva_pregunta)

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

        estado_solicitud = self.solicitud_actual.estado if self.solicitud_actual else None

        if self.tiene_solicitud is False:
            boton_inicio.clicked.connect(self.iniciar_nueva_solicitud)                       
        elif estado_solicitud in [Tipo_estado_solicitud.INICIADA.value]:
            boton_inicio.clicked.connect(self.iniciar_entrevista)
        elif estado_solicitud in [Tipo_estado_solicitud.CANCELADA.value]:
            boton_inicio.clicked.connect(self.iniciar_nueva_solicitud)
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

        #PANTALLA RESUMEN ENTREVISTA EDITABLE
        self.ventana_interno.pantalla_resumen_edit.boton_atras.clicked.connect(
            self.pantalla_resumen_atras
        )
        
        self.ventana_interno.pantalla_resumen_edit.grupo_botones_entrar.idClicked.connect(
            self.mostrar_detalle_pregunta_edit
        )

        self.ventana_interno.pantalla_resumen_edit.boton_enviar.clicked.connect(
            self.almacenar_entrevista
        )

        #PANTALLA SOLICITUD
        self.solicitud_controller.solicitud_finalizada.connect(
            self.solicitud_finalizada
        )

        #PANTALLA PROGRESO
        self.progreso_controller.ver_entrevista_solicitud.connect(
            self.mostrar_resumen_entrevista
        )

        self.progreso_controller.realizar_entrevista_nueva.connect(
            self.iniciar_entrevista
        )

        #PANTALLA RESUMEN ENTREVISTA NO EDITABLE
        self.ventana_interno.pantalla_resumen.grupo_botones_entrar.idClicked.connect(
            self.mostrar_detalle_pregunta
        )

        self.ventana_interno.pantalla_resumen.boton_atras.clicked.connect(
            self.iniciar_progreso
        )

        # PANTALLA PERFIL
        self.ventana_interno.pantalla_perfil.guardar_cambios.connect(
            self.guardar_cambios_perfil
        )

    # -------- FUNCIONES DE NAVEGACIÓN --------

    def iniciar_entrevista(self):
        self.ventana_interno.mostrar_pantalla_preguntas()  

    def iniciar_nueva_solicitud(self):
        self.ventana_interno.mostrar_pantalla_solicitud()

    def iniciar_progreso(self):
        self.ventana_interno.mostrar_pantalla_progreso() 

    def iniciar_perfil(self):
        if self.interno:
            self.ventana_interno.pantalla_perfil.set_datos_usuario(self.interno)
        self.ventana_interno.mostrar_pantalla_perfil()    

    def pregunta_atras(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_atras()

    def siguiente_pregunta(self):
        self.ventana_interno.pantalla_preguntas.ir_pregunta_siguiente()

    def finalizar_entrevista(self, lista_respuestas, lista_audios):
        """
        Se ejecuta cuando la vista confirma que todas las preguntas están respondidas.
        Crea el objeto Entrevista y actualiza el estado.
        """
        
        # Crear Objeto Entrevista
        nueva_entrevista = Entrevista(
            id_entrevista=None, # Se generará en BD
            id_interno=self.interno.num_RC,
            fecha=date.today().strftime("%d/%m/%Y") # Fecha de hoy
        )
        
        # Asignamos las respuestas      
        for i, (texto_res, ruta_audio) in enumerate(zip(lista_respuestas, lista_audios)):
            id_pregunta = i + 1

            obj_pregunta = Pregunta(id_pregunta, texto_res)            

            if ruta_audio:
                obj_pregunta.set_archivo_audio(ruta_audio)

            nueva_entrevista.add_respuestas(obj_pregunta)        
        
        
        # Asociar a la solicitud actual
        if self.solicitud_actual:
            self.solicitud_actual.entrevista = nueva_entrevista                       
        
        # Ir a la pantalla de resumen
        self.ventana_interno.mostrar_pantalla_resumen_edit()
        
        # Recargar resumen en la vista
        self.ventana_interno.pantalla_resumen_edit.cargar_datos_respuestas(nueva_entrevista)

    def mostrar_resumen_entrevista(self):
        """
        Muestra el resumen de la entrevista desde la pantalla de progreso
        """
        entrevista = self.cargar_entrevista_solicitud(self.solicitud_actual.id_solicitud)

        if entrevista:
            self.ventana_interno.pantalla_resumen.cargar_datos_respuestas(entrevista)
            self.ventana_interno.mostrar_pantalla_resumen()
        

    def mostrar_detalle_pregunta_edit(self, id_pregunta):
        """
        Mostrar detalle de la pregunta para editar, se puede cambiar el audio o el texto de la respuesta
        y cambia el objeto de entrevista

        """
        self.pregunta_mostrar = None

        entrevista_actual = self.solicitud_actual.entrevista
        
        #Buscar pregunta en el objeto Entrevista por id
        for pregunta in self.solicitud_actual.entrevista.respuestas:
            if pregunta.id_pregunta == id_pregunta:
                self.pregunta_mostrar = pregunta
                break                        

        if self.pregunta_mostrar:
            ventana_detalle = VentanaDetallePreguntaEdit(self.pregunta_mostrar, id_pregunta)            
            resultado = ventana_detalle.exec_()

            if resultado == QDialog.Accepted:
                datos = ventana_detalle.get_datos()
                nuevo_texto = datos["texto"]
                ruta_definitiva = datos["ruta_audio"]

                self.pregunta_mostrar.respuesta = nuevo_texto
                self.pregunta_mostrar.archivo_audio = ruta_definitiva

                self.ventana_interno.pantalla_resumen_edit.cargar_datos_respuestas(entrevista_actual)
                
                self.msg.mostrar_mensaje(
                    "Guardado", 
                    f"La pregunta {id_pregunta} se ha actualizado correctamente."                   
                )  

            self.solicitud_actual.entrevista = entrevista_actual      

    def mostrar_detalle_pregunta(self, id_pregunta):
        """
        Mostrar detalle de la pregunta para ver, sin opción a editar
        """
        entrevista_actual = self.solicitud_actual.entrevista
        
        #Buscar pregunta en el objeto Entrevista por id
        for pregunta in self.solicitud_actual.entrevista.respuestas:
            if pregunta.id_pregunta == id_pregunta:
                self.pregunta_mostrar = pregunta
                break                        

        if self.pregunta_mostrar:
            ventana_detalle = VentanaDetallePregunta(self.pregunta_mostrar, id_pregunta)            
            ventana_detalle.exec_()

    def almacenar_entrevista(self):
        """
        Recibe la confirmación después de editar la entrevista y la almacena en la base de datos
        Actualiza el estado de la solicitud de iniciada a pendiente
        """

        #Mensaje de confirmación para guardar
        confirmacion = self.msg.mostrar_confirmacion(
            "Enviar entrevista",
            "¿Desea enviar la entrevista?\n\nProximamente será evaluado por un profesional"
        )

        if confirmacion:
            #Almacenar entrevista con pregunta en bd            
            id_entrevista = agregar_entrevista_y_respuestas(self.interno.num_RC, self.solicitud_actual.id_solicitud, 
                                                            self.solicitud_actual.entrevista.fecha,
                                                            self.solicitud_actual.entrevista.respuestas)
            
            self.solicitud_actual.entrevista.id_entrevista = id_entrevista
            self.solicitud_actual.estado = Tipo_estado_solicitud.PENDIENTE.value
            self.progreso_controller.solicitud = self.solicitud_actual
            self.progreso_controller.cargar_datos()


            #Actualizar estado de solicitud
            actualizacion = actualizar_estado_solicitud(self.solicitud_actual.id_solicitud, Tipo_estado_solicitud.PENDIENTE.value)
            if actualizacion is False:
                self.msg.mostrar_advertencia("Error BD", "Error en la actualización del estado de la solicitud.")


            # Mensaje + ir a progreso
            if id_entrevista:
                self.msg.mostrar_mensaje("Entrevista enviada", "La entrevista ha sido enviada correctamente")
                self.iniciar_progreso()
                self.tiene_entrevista = True
            else:
                self.msg.mostrar_mensaje("Error en entrevista", "No ha podido realizarse el envío de la entrevista.\n\nContacte con un administrador.")
            

    def pantalla_resumen_atras(self):
        self.ventana_interno.abrir_pregunta(10)  # Ir a la última pregunta

    # FUNCIONES DEL MENU

    def verificar_acceso_preguntas(self):
        """
        Lógica para controlar si se despliega el menú de preguntas.
        """
        if self.tiene_solicitud is False:
            self.ventana_interno.mostrar_advertencia(
                "Sin Solicitud", 
                "No tiene una solicitud de evaluación iniciada o pendiente."
            )
            return

        if self.tiene_solicitud is True and self.solicitud_actual.estado != Tipo_estado_solicitud.INICIADA.value:
            self.ventana_interno.mostrar_advertencia(
                "Entrevista en proceso", 
                "Ya ha realizado la entrevista para esta solicitud, espere a finalizar."
            )
            return
        
        if self.tiene_solicitud is True and self.tiene_entrevista is True:
            self.ventana_interno.mostrar_advertencia(
                "Entrevista ya realizada", 
                "Ya ha completado la entrevista para esta solicitud."
            )
            return            
        
        self.ventana_interno.movimiento_submenu_preguntas()

    def verificar_ver_progreso(self):
        
        if self.solicitud_actual is None:
            self.ventana_interno.mostrar_advertencia(
                "Sin solicitud",
                "No tiene una solicitud de evaluación iniciada o pendiente."
            )
            return 
        
        self.progreso_controller.solicitud = self.solicitud_actual
        self.progreso_controller.cargar_datos()
        self.iniciar_progreso()

    def verificar_creacion_solicitud(self):
        """
        Lógica se puede crear una nueva solicitud, solo si no tiene pendiente ni iniciada
        """        

        # tiene solicitud pendiente o iniciada
        if self.solicitud_actual and self.solicitud_actual.estado in ["iniciada", "pendiente"]:
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

    def solicitud_finalizada(self):
        # Actualizar estado interno
        self.tiene_solicitud = True
        self.tiene_entrevista = False

        # Cambiar de pantalla
        self.ventana_interno.mostrar_pantalla_progreso()

        # Actualizar progreso
        self.solicitud_actual = self.cargar_ultima_solicitud()
        self.progreso_controller.solicitud = self.solicitud_actual
        self.progreso_controller.cargar_datos()
        
    def guardar_cambios_perfil(self):
        if not self.interno:
            return

        datos = self.ventana_interno.pantalla_perfil.get_datos_edicion()
        nombre_nuevo = datos["nombre"]
        nombre_original = datos["nombre_original"]
        password = datos["password"]
        password_confirm = datos["password_confirm"]

        if not nombre_nuevo:
            self.msg.mostrar_advertencia("Atencion", "El nombre no puede estar vacio.")
            return

        if password or password_confirm:
            if password != password_confirm:
                self.msg.mostrar_advertencia("Atencion", "Las contraseñas no coinciden.")
                return

        cambio_nombre = nombre_nuevo != nombre_original
        cambio_password = bool(password)
        if not cambio_nombre and not cambio_password:
            self.msg.mostrar_advertencia("Atencion", "No hay cambios para guardar.")
            return

        ok = actualizar_usuario(
            self.interno.id_usuario,
            nombre=nombre_nuevo if cambio_nombre else None,
            contrasena=password if cambio_password else None
        )
        if not ok:
            self.msg.mostrar_advertencia("Atencion", "No se pudo actualizar el perfil.")
            return

        self.interno.nombre = nombre_nuevo
        self.usuario.nombre = nombre_nuevo
        self.ventana_interno.pantalla_bienvenida.set_interno(self.interno)
        self.msg.mostrar_mensaje("Perfil actualizado", "Cambios guardados correctamente.")



