from enum import Enum

class tipo_rol(Enum):
    ADMIN = "Administrador"
    INTERNO = "Interno"
    PROFESIONAL = "Profesional"

class tipo_estado_solicitud(Enum):
    PENDIENTE = "Pendiente"
    ACEPTADA = "Aceptada"
    RECHAZADA = "Rechazada"
    CANCELADA = "Cancelada"

class tipo_profesional(Enum):
    PSICOLOGO = "Psicólogo"
    TRABAJADOR_SOCIAL = "Trabajador Social"
    EDUCADOR = "Educador"

class tipo_situacion_legal(Enum):
    PROVISIONAL = "Provisional"
    CONDENADO = "Condenado"
    LIBERTAD_CONDICIONAL = "Libertad Condicional"
    

            