from PyQt5.QtCore import QObject, pyqtSignal, QStandardPaths
from PyQt5.QtWidgets import QFileDialog
import os
from models.solicitud import Solicitud
from gui.mensajes import Mensajes
from utils.documentoPDF import DocumentoPDF

from db.solicitud_db import *

class ProgresoController(QObject):
    """
    Controlador para la pantalla de detalle de solicitud
    Gestiona la visualización y las acciones sobre una solicitud existente
    """

    #Señales
    ver_entrevista_solicitud = pyqtSignal(int) # ID de la entrevista   
    realizar_entrevista_nueva = pyqtSignal()

    def __init__(self, vista_progreso, solicitud, interno):
        super().__init__()
        self.vista = vista_progreso
        self.solicitud = solicitud
        self.interno = interno

        self.msg = Mensajes(vista_progreso)

        self.cargar_datos()
        self.conectar_senales()
        

    def conectar_senales(self):
        """
        conecta las señales de los botones con sus acciones
        """
        self.vista.boton_solicitud.clicked.connect(self.descargar_solicitud)
        self.vista.boton_entrevista.clicked.connect(self.accion_boton_entrevista)
        self.vista.boton_cancelar.clicked.connect(self.cancelar_solicitud)

    def accion_boton_entrevista(self):
        """
        Decide la acción del botón de entrevista según el estado actual.
        """
        if not self.solicitud:
            return

        if self.solicitud.estado == "iniciada":
            self.realizar_entrevista()
        else:
            self.ver_entrevista()

    def cargar_datos(self):
        """
        Carga los datos de la solicitud en la vista
        """

        if not self.solicitud:
            self.vista.cargar_datos_solicitud(
                self.solicitud,
                self.interno.nombre,
                self.interno.num_RC
            )
            self.vista.boton_solicitud.setEnabled(False)
            self.vista.boton_solicitud.setToolTip("Desactivado: no hay solicitud para descargar.")
            self.vista.boton_entrevista.setEnabled(False)
            self.vista.boton_entrevista.setToolTip("Desactivado: no hay solicitud asociada.")
            self.vista.boton_cancelar.setEnabled(False)
            self.vista.boton_cancelar.setToolTip("Desactivado: no hay solicitud asociada.")
            return

        self.vista.cargar_datos_solicitud(
            self.solicitud,
            self.interno.nombre,
            self.interno.num_RC
        )

        self.vista.boton_solicitud.setEnabled(True)
        self.vista.boton_solicitud.setToolTip("Descargar solicitud en PDF")
        self.vista.boton_cancelar.setEnabled(
            self.solicitud.estado not in ["aceptada", "rechazada", "cancelada"]
        )
        if self.solicitud.estado in ["aceptada", "rechazada", "cancelada"]:
            self.vista.boton_cancelar.setToolTip(
                "Desactivado: la solicitud ya está finalizada y no puede cancelarse."
            )
        else:
            self.vista.boton_cancelar.setToolTip("Cancelar solicitud")

        # Habilitar / deshabilitar botón de entrevista si hay o la solicitud está iniciada
        if self.solicitud.entrevista or self.solicitud.estado == "iniciada":
            self.vista.boton_entrevista.setEnabled(True)
            if self.solicitud.estado == "iniciada":
                self.vista.boton_entrevista.setToolTip("Realizar entrevista")
            else:
                self.vista.boton_entrevista.setToolTip("Ver entrevista")
        else:
            self.vista.boton_entrevista.setEnabled(False)
            self.vista.boton_entrevista.setToolTip(
                "Desactivado: aun no hay entrevista disponible."
            )

    def ver_entrevista(self):
        """
        Maneja la acción de ver la entrevista
        Emite una señal para que el InternoController maneje la navegación
        """
        if not self.solicitud:
            return

        if self.solicitud.entrevista and self.solicitud.entrevista.id_entrevista:
            self.ver_entrevista_solicitud.emit(self.solicitud.entrevista.id_entrevista)
        else:
            self.msg.mostrar_advertencia(
                "Entrevista no disponible",
                "La entrevista aún no está disponible para visualización."
        )                
       
    def realizar_entrevista(self):
        """
        Maneja la acción de realizar la entrevista
        Emite una señal para que el InternoController maneje la navegación
        """
        if not self.solicitud:
            return

        self.realizar_entrevista_nueva.emit()
    

    def descargar_solicitud(self):
        """
        Maneja la descarga de la solicitud en formato PDF
        """
        if not self.solicitud:
            return

        try:
            # Solicitar ubicación de guardado
            ruta_guardado, _ = QFileDialog.getSaveFileName(
                self.vista,
                "Guardar Solicitud",
                os.path.join(
                    QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
                    f"Solicitud_{self.solicitud.id_solicitud}.pdf",
                ),
                "PDF Files (*.pdf)"
            )
            
            if ruta_guardado:
                # Generar el PDF                
                DocumentoPDF.generar_pdf_solicitud(self.solicitud, ruta_guardado, self.interno)
                
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
        if not self.solicitud:
            return

        confirmado = self.msg.mostrar_confirmacion(
            "Cancelar solicitud",
            "¿Desea cancelar esta solicitud?\n\nEsta acción cambiará su estado a cancelada."
        )
        if not confirmado:
            return

        self.solicitud.estado = "cancelada"
        self.cargar_datos()

        # Guarda solicitud en BD
        actualizar_estado_solicitud(self.solicitud.id_solicitud, "cancelada")

        self.msg.mostrar_mensaje(
            "Actualización existosa",
            "La solicitud se ha cancelado correctamente"
        )

        # Deshabilitar botón de entrevista al cancelar
        self.vista.boton_entrevista.setEnabled(False)
        self.vista.boton_entrevista.setToolTip(
            "Desactivado: la solicitud está cancelada."
        )



    
    
