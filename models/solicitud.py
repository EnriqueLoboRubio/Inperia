from utils.enums import Tipo_estado_solicitud

class Solicitud:
    def __init__(self, id_solicitud, tipo, motivo, descripcion, urgencia):
        self.id_solicitud = id_solicitud        
        self.tipo = tipo
        self.motivo = motivo
        self.descripcion = descripcion
        self.urgencia = urgencia

        self.fecha_inicio = None       
        self.fecha_fin = None
        self.hora_salida = None
        self.hora_llegada = None
        self.destino = None
        self.cuidad = None
        self.direccion = None
        self.cod_pos = None

        self.nombre_cp = None
        self.telf_cp = None
        self.relacion_cp = None
        self.direccion_cp = None
        self.nombre_cs = None
        self.telf_cs = None
        self.relacion_cs = None        

        self.docs = []
        self.compromisos = []
        self.observaciones = None

        self.estado = Tipo_estado_solicitud.INICIADA
        
        self.entrevista = None

    def add_docs(self, doc):
        self.docs.append(doc)         

    def add_compromiso(self, compromiso):
        self.compromisos.append(compromiso)       

