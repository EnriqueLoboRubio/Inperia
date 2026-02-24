import argparse
import os
from datetime import datetime

# Asegúrate de importar tus clases desde la ruta correcta en tu proyecto
from models.solicitud import Solicitud
from utils.documentoPDF import DocumentoPDF

class MockInterno:
    """Clase falsa para simular los datos de un interno sin usar la BD"""
    def __init__(self):
        self.num_RC = "12345/2026"
        self.nombre = "Juan Pérez González"
        self.fecha_nac = "15/04/1985"
        self.situacion_legal = "Penado"
        self.delito = "Robo con fuerza, atentado contra la autoridad y otros delitos menores"
        self.fecha_ingreso = "10/01/2020"
        self.modulo = "Módulo 4 - Respeto"
        self.condena = "8 años y 6 meses"

class MockEntrevista:
    """Clase falsa para la fecha de la entrevista"""
    def __init__(self):
        self.fecha = datetime.now().strftime("%d/%m/%Y")

def main():
    parser = argparse.ArgumentParser(description="Genera un PDF de prueba con textos largos sin base de datos.")
    parser.add_argument(
        "--output",
        type=str,
        default="Solicitud_Prueba_Textos_Largos.pdf",
        help="Ruta del PDF de salida.",
    )
    args = parser.parse_args()

    # 1. Crear la solicitud mock directamente en memoria
    solicitud = Solicitud()
    solicitud.id_solicitud = 9999
    solicitud.tipo = "Permiso Extraordinario"
    solicitud.urgencia = "Alta"
    
    # 2. Inyectar textos muy largos para forzar el salto de línea y expansión de cajas en el PDF
    solicitud.motivo = (
        "Solicitud de permiso por motivos familiares"
    ) * 2
    
    solicitud.descripcion = (
        "El interno solicita este permiso para poder visitar a su familia"
    ) * 2

    solicitud.observaciones = (
        "Durante la tramitación se ha comprobado el domicilio aportado mediante"
    ) * 2

    solicitud.conclusiones_profesional = (
        "Tras la entrevista personal exhaustiva."
    ) * 2

    # 3. Resto de datos comunes de la solicitud
    solicitud.fecha_creacion = datetime.now().strftime("%d/%m/%Y")
    solicitud.fecha_inicio = "01/03/2026"
    solicitud.fecha_fin = "05/03/2026"
    solicitud.hora_salida = "10:30"
    solicitud.hora_llegada = "19:00"
    solicitud.destino = "Huelva Capital"
    solicitud.provincia = "Huelva"
    solicitud.direccion = "Avenida de Andalucía 123, Bloque 4, 2ºB"
    solicitud.cod_pos = "21004"
    
    solicitud.nombre_cp = "María González (Madre)"
    solicitud.telf_cp = "600123456"
    solicitud.relacion_cp = "Familiar Directo"
    solicitud.direccion_cp = "Avenida de Andalucía 123, Huelva"
    
    solicitud.nombre_cs = "Carlos Pérez (Hermano)"
    solicitud.telf_cs = "600654321"
    solicitud.relacion_cs = "Familiar Directo"
    
    solicitud.compromisos = 63 # 63 activa los 6 bits de COMP_LABELS (1+2+4+8+16+32)
    solicitud.estado = "EN TRAMITACIÓN AVANZADA"
    solicitud.entrevista = MockEntrevista()

    # 4. Crear el interno de prueba
    interno = MockInterno()

    output = os.path.abspath(args.output)

    # 5. Generar el PDF
    try:
        DocumentoPDF.generar_pdf_solicitud(solicitud, output, interno)
        print(f"PDF de prueba generado con éxito en: {output}")
    except Exception as e:
        print(f"Ocurrió un error al generar el PDF: {e}")

if __name__ == "__main__":
    main()