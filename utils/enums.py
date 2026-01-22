from enum import Enum

class Tipo_rol(Enum):
    ADMIN = "Administrador"
    INTERNO = "Interno"
    PROFESIONAL = "Profesional"

class Tipo_estado_solicitud(Enum):
    PENDIENTE = "Pendiente"
    ACEPTADA = "Aceptada"
    RECHAZADA = "Rechazada"
    CANCELADA = "Cancelada"
    FINALIZADA = "Finalizada"

class Tipo_profesional(Enum):
    PSICOLOGO = "Psicólogo"
    TRABAJADOR_SOCIAL = "Trabajador Social"
    EDUCADOR = "Educador"

class Tipo_situacion_legal(Enum):
    PROVISIONAL = "Provisional"
    CONDENADO = "Condenado"
    LIBERTAD_CONDICIONAL = "Libertad Condicional"


            