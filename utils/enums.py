from enum import Enum

class Tipo_rol(Enum):
    ADMIN = "Administrador"
    INTERNO = "Interno"
    PROFESIONAL = "Profesional"

class Tipo_estado_solicitud(Enum):
    PENDIENTE = "pendiente"
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada" 

class Tipo_permiso(Enum):
    FAMILIAR = "familiar"
    MEDICO = "medico"
    EDUCATIVO = "educativo"
    LABORAL = "laboral"
    DEFUNCION = "defuncion"
    JURIDICO = "juridico"

class Tipo_urgencia(Enum):
    NORMAL = "normal"
    IMPORTANTE = "importante"
    URGENTE = "urgente"

class Tipo_docs(Enum):
    DNI_FAMILIAR = "dni_familiar"
    RELACION = "relacion"
    INVITACION = "invitacion"

class Tipo_compromiso(Enum):
    HORARIO = "horario"
    CONTACTO = "contacto"
    CONSUMIR = "consumir"
    COMPROBANTE = "comprobante"
    CAMBIO = "cambio"
    LUGAR = "lugar"

class Tipo_profesional(Enum):
    PSICOLOGO = "Psicólogo"
    TRABAJADOR_SOCIAL = "Trabajador Social"
    EDUCADOR = "Educador"

class Tipo_situacion_legal(Enum):
    PROVISIONAL = "Provisional"
    CONDENADO = "Condenado"
    LIBERTAD_CONDICIONAL = "Libertad Condicional"
            