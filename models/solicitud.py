class Solicitud:
    def __init__(self, id_solicitud, id_entrevista, id_interno, fecha_inicio, estado):
        self.id_solicitud = id_solicitud
        self.id_entrevista = id_entrevista
        self.id_interno = id_interno
        self.fecha_inicio = fecha_inicio       
        self.fecha_fin = None
        self.estado = estado
        self.entrevista = None
    
    def get_id_solicitud(self):
        return self.id_solicitud
    
    def get_id_entrevista(self):
        return self.id_entrevista
    
    def get_id_interno(self):
        return self.id_interno
    
    def set_fecha_inicio(self, fecha_inicio):
        self.fecha_inicio = fecha_inicio

    def get_fecha_inicio(self):
        return self.fecha_inicio
    
    def set_fecha_fin(self, fecha_fin):
        self.fecha_fin = fecha_fin

    def get_fecha_fin(self):
        return self.fecha_fin
    
    def set_estado(self, estado):
        self.estado = estado

    def get_estado(self):
        return self.estado
    
    def set_entrevista(self, entrevista):
        self.entrevista = entrevista

    def get_entrevista(self):
        return self.entrevista
