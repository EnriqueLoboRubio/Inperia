from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from models.solicitud import Solicitud
from gui.mensajes import Mensajes

from db.solicitud_db import *

class ProgresoController(QObject):
    """
    Controlador para la pantalla de detalle de solicitud
    Gestiona la visualización y las acciones sobre una solicitud existente
    """

    #Señales
    ver_entrevista_solicitud = pyqtSignal(int) # ID de la entrevista   

    def __init__(self, vista_progreso, solicitud, interno):
        super().__init__()
        self.vista = vista_progreso
        self.solicitud = solicitud
        self.interno = interno

        self.msg = Mensajes(vista_progreso)

        self.conectar_senales()
        self.cargar_datos()

    def conectar_senales(self):
        """
        conecta las señales de los botones con sus acciones
        """
        self.vista.boton_solicitud.clicked.connect(self.descargar_solicitud)
        self.vista.boton_entrevista.clicked.connect(self.ver_entrevista)
        self.vista.boton_cancelar.clicked.connect(self.cancelar_solicitud)

    def cargar_datos(self):
        """
        Carga los datos de la solicitud en la vista
        """

        self.vista.cargar_datos_solicitud(
            self.solicitud,
            self.interno.nombre,
            self.interno.num_RC
        )

        # Habilitar / deshabilitar botón de entrevista si hay o no
        if self.solicitud.entrevista:
            self.vista.boton_entrevista.setEnabled(True)
        else:
            self.vista.boton_entrevista.setEnable(False)

    def ver_entrevista(self):
        """
        Maneja la acción de ver la entrevista
        Emite una señal para que el InternoController maneje la navegación
        """

        if self.solicitud.entrevista:
            # Verificar que la entrevista tiene ID
            if hasattr(self.solicitud.entrevista, 'id_entrevista') and self.solicitud.entrevista.id_entrevista:
                self.ver_entrevista_solicitud.emit(self.solicitud.entrevista.id_entrevista)
            else:
                self.msg.mostrar_advertencia(
                    "Entrevista no disponible",
                    "La entrevista aún no está disponible para visualización."
                )                
        else:

            self.msg.mostrar_mensaje(
                "Sin entrevista",
                "Esta solicitud aún no tiene una entrevista asociada."
            )

    def descargar_solicitud(self):
        """
        Maneja la descarga de la solicitud en formato PDF
        """
        try:
            # Solicitar ubicación de guardado
            ruta_guardado, _ = QFileDialog.getSaveFileName(
                self.vista,
                "Guardar Solicitud",
                f"Solicitud_{self.solicitud.id_solicitud}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if ruta_guardado:
                # lógica para generar el PDF                
                self.generar_pdf_solicitud(ruta_guardado)
                
                self.msg.mostrar_mensaje(                    
                    "Descarga exitosa",
                    f"La solicitud se ha guardado en:\n{ruta_guardado}"
                )
        except Exception as e:
            self.msg.mostrar_advertencia(
                "Error al descargar",
                f"No se pudo guardar la solicitud:\n{str(e)}"
            )

    def generar_pdf_solicitud(self, ruta_destino):
        """
        Genera un PDF con los datos de la solicitud 
        """
        pass

    def cancelar_solicitud(self):
        """
        Cambia el estado de la solicitud a cancelada y se actulizada la interfaz
        Guarda el cambio en la BD
        """

        self.solicitud.estado = "cancelada"
        self.cargar_datos()

        # Guarda solicitud en BD
        actualizar_estado_solicitud(self.solicitud.id_solicitud, "cancelada")


        self.msg.mostrar_mensaje(
            "Actualización existosa",
            "La solicitud se ha cancelado correctamente"
        )

    
    
