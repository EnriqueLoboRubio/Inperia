class Solicitud:
    def __init__(self, id_solicitud, id_entrevista, id_interno, fecha_inicio, estado):
        self.id_solicitud = id_solicitud
        self.id_entrevista = id_entrevista
        self.id_interno = id_interno
        self.fecha_inicio = fecha_inicio       
        self.fecha_fin = None
        self.estado = estado
        self.entrevista = None