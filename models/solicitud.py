from utils.enums import Tipo_estado_solicitud

class Solicitud:
    def __init__(self):
        self.id_solicitud = None       
        self.tipo = None
        self.motivo = ""
        self.descripcion = ""
        self.urgencia = None

        self.fecha_inicio = ""       
        self.fecha_fin = ""
        self.hora_salida = ""
        self.hora_llegada = ""
        self.destino = ""
        self.ciudad = ""
        self.direccion = ""
        self.cod_pos = ""

        self.nombre_cp = ""
        self.telf_cp = ""
        self.relacion_cp = ""
        self.direccion_cp = ""
        self.nombre_cs = ""
        self.telf_cs = ""
        self.relacion_cs = ""        

        self.docs = 0
        self.compromisos = 0
        self.observaciones = ""

        self.estado = Tipo_estado_solicitud.INICIADA
        
        self.entrevista = None              

    def valida_paso1(self):
        """
        Valida los datos del paso 1 
        """
        if not self.tipo:
            return False, "Debe seleccionar un tipo de permiso"
        if not self.motivo.strip():
            return False, "Debe ingresar una descripción del motivo"
        if not self.urgencia:
            return False, "Debe seleccionar un nivel de urgencia"
        if not self.motivo.strip():
            return False, "Debe ingresar el motivo específico"
        return True, ""
    
    def valida_paso2(self):
        """
        Valida los datos del paso 2
        """
        if not self.fecha_inicio or not self.fecha_fin:
            return False, "Debe seleccionar las fechas de inicio y fin"
        if not self.hora_salida or not self.hora_llegada:
            return False, "Debe seleccionar las horas de salida y llegada"
        if not self.destino.strip():
            return False, "Debe ingresar el destino"
        if not self.ciudad.strip():
            return False, "Debe ingresar la ciudad"
        if not self.direccion.strip():
            return False, "Debe ingresar la dirección"
        return True, ""
    
    def valida_paso3(self):
        """
        Valida los datos del paso 3
        """
        if not self.nombre_cp.strip():
            return False, "Debe ingresar el nombre del contacto principal"
        if not self.telf_cp.strip():
            return False, "Debe ingresar el teléfono del contacto principal"
        if not self.relacion_cp or self.relacion_cp == "Seleccionar...":
            return False, "Debe seleccionar la relación del contacto principal"
        if not self.direccion_cp.strip():
            return False, "Debe ingresar la dirección del contacto principal"
        return True, ""

    def valida_paso4(self):
        """
        Valida los datos del paso 4
        """
        if not self.docs:
            return False, "Debe seleccionar al menos un documento"
        if not self.compromisos:
            return False, "Debe aceptar al menos un compromiso"
        return True, ""

    def reset(self):
        """Reinicia todos los datos del modelo"""
        # Paso 1
        self.tipo = None
        self.descripcion = ""
        self.urgencia = None
        self.motivo = ""
        
        # Paso 2
        self.fecha_inicio = None
        self.fecha_fin = None
        self.hora_salida = None
        self.hora_llegada = None
        self.destino = ""
        self.ciudad = ""
        self.direccion = ""
        self.cod_pos = ""
        
        # Paso 3
        self.nombre_cp = ""
        self.telf_cp = ""
        self.relacion_cp = ""
        self.direccion_cp = ""
        self.nombre_cs = ""
        self.telf_cs = ""
        self.relacion_cs = ""
        
        # Paso 4
        self.docs = []
        self.compromisos = []
        self.observaciones = ""

    def get_resumen(self):
        """Devuelve un resumen de la solicitud"""
        return {
            "tipo": self.tipo_,
            "descripcion": self.descripcion,
            "urgencia": self.urgencia,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "destino": self.destino_principal,
            "ciudad": self.ciudad,
            "contacto_emergencia": self.nombre_cp,
            "telefono_emergencia": self.telf_cp,
            "documentos": self.documentos,
            "compromisos": self.compromisos
        }