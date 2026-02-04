from PyQt5.QtCore import QObject, pyqtSignal
from db.solicitud_db import agregar_solicitud

class SolicitudController(QObject):
    solicitud_finalizada = pyqtSignal() # Señal para avisar al InternoController

    def __init__(self, vista_solicitud, num_RC):
        super().__init__()
        self.vista = vista_solicitud
        self.num_RC = num_RC
        self.current_step = 1
        self.total_steps = 4
        self.conectar_senales()

    def conectar_senales(self):
        self.vista.btn_siguiente.clicked.connect(self.siguiente_paso)
        self.vista.btn_anterior.clicked.connect(self.paso_anterior)

    def siguiente_paso(self):
        if self.current_step < self.total_steps:
            # Aquí añadirías las validaciones del modelo que tenías en permiso_app.py
            self.current_step += 1
            self.vista.actualizar_ui(self.current_step)
        else:
            self.guardar_solicitud()

    def paso_anterior(self):
        if self.current_step > 1:
            self.current_step -= 1
            self.vista.actualizar_ui(self.current_step)

    def guardar_solicitud(self):
        # 1. Extraer datos de los widgets de la vista
        # (Similar a _capture_step_data en permiso_app.py)
        datos = self.vista.obtener_datos_formulario()
        
        # 2. Llamar a la base de datos (solicitud_db.py)
        nuevo_id = agregar_solicitud(
            id_interno=self.num_RC,
            tipo=datos['tipo'],
            motivo=datos['motivo'],
            descripcion=datos['descripcion'],
            urgencia=datos['urgencia'],
            fecha_inicio=datos['fecha_inicio'],
            fecha_fin=datos['fecha_fin'],
            # ... resto de campos según solicitud_db.py
            estado='pendiente'
        )
        
        if nuevo_id:
            self.solicitud_finalizada.emit()