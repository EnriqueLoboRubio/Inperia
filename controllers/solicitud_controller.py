from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog
from db.solicitud_db import agregar_solicitud
from models.solicitud import Solicitud
from gui.dialog_solicitud_enviada import DialogSolicitudEnviada

class SolicitudController(QObject):

    #Señales
    solicitud_finalizada = pyqtSignal() # Señal para avisar al InternoController
    paso_cambiado = pyqtSignal(int)   

    def __init__(self, vista_solicitud, num_RC):
        super().__init__()
        self.vista = vista_solicitud
        self.num_RC = num_RC
        self.solicitud = Solicitud()
        self.paso_actual = 1
        self.total_pasos = 4
        self.conectar_senales()

    def conectar_senales(self):
        self.vista.boton_siguiente.clicked.connect(self.siguiente_paso)
        self.vista.boton_anterior.clicked.connect(self.paso_anterior)

    def siguiente_paso(self):

        """
        Avanza al siguiente paso si la validación es exitosa
        """

        #Capturar datos de vista antes de validar
        self.capturar_datos_paso(self.paso_actual)

        #Validar paso actual
        es_valido, error_mensaje = self.validar_paso_actual()

        if not es_valido:
            self.vista.mostrar_validacion_error(error_mensaje)
            return False
        
        #Avanzar al siguiente paso
        if self.paso_actual < self.total_pasos:
            self.paso_actual += 1
            self.vista.actualizar_ui(self.paso_actual)
            return True
        elif self.paso_actual == self.total_pasos:
            # 1️⃣ Construir resumen (NO guardar)
            datos = self.solicitud.get_resumen()

            # 2️⃣ Mostrar diálogo de confirmación
            dialogo = DialogSolicitudEnviada(datos, parent=self.vista)
            confirmado = dialogo.exec_()

            # 3️⃣ Decisión del usuario
            if confirmado == QDialog.Accepted:
                self.guardar_solicitud()
            else:
                # Usuario dijo NO → volver al paso 4
                return False
        
        return False

    def paso_anterior(self):
        """
        Retroceder al paso anterior
        """
        if self.paso_actual > 1:
            self.paso_actual -= 1
            self.vista.actualizar_ui(self.paso_actual)
            return True
        
        return False
    
    def validar_paso_actual(self):
        """
        Valida el paso actual
        """
        validaciones = {
            1: self.solicitud.valida_paso1,
            2: self.solicitud.valida_paso2,
            3: self.solicitud.valida_paso3,
            4: self.solicitud.valida_paso4
        }   

        validacion = validaciones.get(self.paso_actual)
        if validacion:
            return validacion()
        
        return True, ""

    def capturar_datos_paso(self, paso):
        """
        Captura los datos de la vista y los almacena en el modelo
        """

        if paso == 1:
            self.capturar_datos_paso1(self.vista.paso1)
        elif paso == 2: 
            self.capturar_datos_paso2(self.vista.paso2)
        elif paso == 3: 
            self.capturar_datos_paso3(self.vista.paso3)
        elif paso == 4: 
            self.capturar_datos_paso4(self.vista.paso4)

    def capturar_datos_paso1(self, paso_widget):
        
        #Tipo de permiso
        tarjetas = [
            ("familiar", paso_widget.tarjeta_familiar),
            ("educativo", paso_widget.tarjeta_educativo),
            ("defuncion", paso_widget.tarjeta_defuncion),
            ("medico", paso_widget.tarjeta_medico),
            ("laboral", paso_widget.tarjeta_laboral),
            ("juridico", paso_widget.tarjeta_juridico),
        ]

        self.solicitud.tipo = None

        for tipo, tarjeta in tarjetas:
            if tarjeta.seleccionado:
                self.solicitud.tipo = tipo
                break

        # Descripcion y motivo
        self.solicitud.descripcion = paso_widget.desc_texto.toPlainText()
        self.solicitud.motivo = paso_widget.motivo_texto.text()

        # Nivel de urgencia
        if paso_widget.boton_normal.isChecked():
            self.solicitud.urgencia = "normal"
        elif paso_widget.boton_importante.isChecked():
            self.solicitud.urgencia = "importante"
        elif paso_widget.boton_urgente.isChecked():
            self.solicitud.urgencia = "urgente"

    def capturar_datos_paso2(self, paso_widget):    
        self.solicitud.fecha_inicio = paso_widget.fecha_inicio.date().toString("dd/MM/yyyy")
        self.solicitud.fecha_fin = paso_widget.fecha_fin.date().toString("dd/MM/yyyy")
        self.solicitud.hora_salida = paso_widget.hora_salida.time().toString("HH:mm")
        self.solicitud.hora_llegada = paso_widget.hora_llegada.time().toString("HH:mm")
        self.solicitud.destino = paso_widget.destino_texto.text().strip()
        self.solicitud.ciudad = paso_widget.ciudad_texto.text()
        self.solicitud.direccion = paso_widget.direccion_texto.text()
        self.solicitud.cod_pos = paso_widget.codigo_texto.text()

    def capturar_datos_paso3(self, paso_widget):
        self.solicitud.nombre_cp = paso_widget.nombre_prin_texto.text()
        self.solicitud.telf_cp = paso_widget.telefono_prin_texto.text()
        self.solicitud.relacion_cp = paso_widget.relacion_prin_combo.currentText()
        self.solicitud.direccion_cp = paso_widget.direccion_prin_texto.text()
        self.solicitud.nombre_cs = paso_widget.nombre_secun_texto.text()
        self.solicitud.telf_cs = paso_widget.telefono_secun_texto.text()
        self.solicitud.relacion_cs = paso_widget.relacion_secun_combo.currentText()

    def capturar_datos_paso4(self, paso_widget):
        # Documentos
        documentos =[
            paso_widget.doc_identidad,
            paso_widget.doc_relacion,
            paso_widget.doc_invitacion
        ]

        valor_guardar_docs = 0

        for i, documento in enumerate(documentos):
            if documento.isChecked():
                valor_guardar_docs += (1<< i)

        self.solicitud.docs = valor_guardar_docs

         # Compromisos    
        self.compromisos = [
            paso_widget.comp1,
            paso_widget.comp2, 
            paso_widget.comp3, 
            paso_widget.comp4, 
            paso_widget.comp5, 
            paso_widget.comp6
        ]

        valor_guardar_com = 0
        
        for i, checkbox in enumerate(self.compromisos):
            if checkbox.isChecked():
                valor_guardar_com += (1 << i)

        self.solicitud.compromisos = valor_guardar_com
        
        # Observaciones
        self.solicitud.observaciones = paso_widget.observaciones_texto.toPlainText()
        
    def ver_resumen(self):
        """
        Envía el formulario
        """
        resumen = self.solicitud.get_resumen()
        self.vista.ver_resumen(resumen)

    def guardar_solicitud(self):            
        
        # Llamar a la base de datos
        nuevo_id = agregar_solicitud(
            id_interno=self.num_RC,
            tipo=self.solicitud.tipo,
            motivo=self.solicitud.motivo,
            descripcion=self.solicitud.descripcion,
            urgencia=self.solicitud.urgencia,
            fecha_inicio=self.solicitud.fecha_inicio,
            fecha_fin=self.solicitud.fecha_fin,
            hora_salida=self.solicitud.hora_salida,
            hora_llegada=self.solicitud.hora_llegada,
            destino=self.solicitud.destino,
            ciudad=self.solicitud.ciudad,
            direccion=self.solicitud.direccion,
            cod_pos=self.solicitud.cod_pos,
            nombre_cp=self.solicitud.nombre_cp,
            telf_cp=self.solicitud.telf_cp,
            relacion_cp=self.solicitud.relacion_cp,
            direccion_cp=self.solicitud.direccion_cp,
            nombre_cs=self.solicitud.nombre_cs,
            telf_cs=self.solicitud.telf_cs,
            relacion_cs=self.solicitud.relacion_cs,
            docs=self.solicitud.docs,
            compromiso=self.solicitud.compromisos,                
            observaciones=self.solicitud.observaciones,
            estado='iniciada'
        )
        
        if not nuevo_id:
            self.solicitud_finalizada.emit()