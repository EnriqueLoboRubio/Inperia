import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas


COMP_LABELS = [
    "Cumplir estrictamente con los horarios establecidos",
    "Mantener contacto permanente con la institucion",
    "No consumir alcohol ni sustancias prohibidas",
    "Presentar comprobantes de las actividades realizadas",
    "Informar cualquier cambio en la programacion",
    "No alejarse del lugar autorizado sin permiso",
]

def decodificar(valor, etiquetas):
    """
    Decodifica un valor entero en una lista de etiquetas según los bits activos.
    """
    if valor is None:
        return []
    try:
        valor_int = int(valor)
    except (TypeError, ValueError):
        return []
    return [texto for i, texto in enumerate(etiquetas) if valor_int & (1 << i)]


class DocumentoPDF:
    color_pag = colors.HexColor("#EFEFEF")
    color_caja = colors.HexColor("#DEDEDE")
    color_borde = colors.HexColor("#B9B9B9")
    color_titulo_caja = colors.HexColor("#CFCFCF")
    margen_x = 30
    contenido_w = A4[0] - (margen_x * 2)
    espacio_fila = 25
    espacio_fila = 24

    @staticmethod
    def texto(valor, vacio="  __________"):
        if valor is None:
            return vacio
        texto = str(valor).strip()
        return texto if texto else vacio

    @staticmethod
    def logo_inperia():
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "assets", "inperiaPDF.png")

    @staticmethod
    def dibujar_pag(c, ancho, alto):
        c.setFillColor(DocumentoPDF.color_pag)
        c.rect(0, 0, ancho, alto, stroke=0, fill=1)

    @staticmethod
    def dibujar_logo(c, x, y, tam=42):
        path = DocumentoPDF.logo_inperia()
        if os.path.exists(path):
            c.drawImage(ImageReader(path), x, y, width=tam, height=tam, preserveAspectRatio=True, mask="auto")
        else:
            c.setFont("Times-Bold", 38)
            c.setFillColor(colors.black)
            c.drawString(x + 6, y + 2, "I")

    @staticmethod
    def dibujar_encabezado(c, ancho, alto):
        DocumentoPDF.dibujar_logo(c, 15, alto - 90, tam=92)
        c.setFillColor(colors.black)
      
        c.setFont("Helvetica", 16)
        c.drawString(74, alto - 42, "NPERIA")
        c.setFont("Helvetica-Bold", 31)
        c.drawString(74, alto - 67, "Comprobante de la solicitud")

    @staticmethod
    def dibujar_titulo_caja(c, x, y, texto, w=210, h=24):
        c.setFillColor(DocumentoPDF.color_titulo_caja)
        c.roundRect(x, y - h, w, h, 12, stroke=0, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 16)
        c.drawString(x + 26, y - 17, texto)

    @staticmethod
    def dibujar_caja(c, x, y_top, w, h):
        c.setFillColor(DocumentoPDF.color_caja)
        c.setStrokeColor(DocumentoPDF.color_borde)
        c.roundRect(x, y_top - h, w, h, 14, stroke=1, fill=1)
        c.setFillColor(colors.black)

    @staticmethod
    def anadir_apartado(c, x, y, label, value):
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, label)
        dx = c.stringWidth(label, "Helvetica-Bold", 10) + 3
        c.setFont("Helvetica", 10)
        c.drawString(x + dx, y, DocumentoPDF.texto(value))

    @staticmethod
    def texto_linea(c, x, y_top, text, width, max_lines=2):
        lines = simpleSplit(DocumentoPDF.texto(text, ""), "Helvetica", 10, width)[:max_lines]
        if not lines:
            lines = ["  __________"]
        y = y_top
        c.setFont("Helvetica", 10)
        for ln in lines:
            c.drawString(x, y, ln)
            y -= 13

    @staticmethod
    def generar_pdf_solicitud(solicitud, ruta_archivo, interno=None):
        canv = canvas.Canvas(ruta_archivo, pagesize=A4)
        ancho, alto = A4

        # Pagina 1
        DocumentoPDF.dibujar_pag(canv, ancho, alto)
        DocumentoPDF.dibujar_encabezado(canv, ancho, alto)

        x0 = DocumentoPDF.margen_x
        w = DocumentoPDF.contenido_w
        x_izq = x0 + 36
        x_der = x0 + (w / 2) + 10

        # Caja de datos del interno
        y = alto - 96
        DocumentoPDF.dibujar_titulo_caja(canv, x0 + 24, y, "Datos del interno")
        caja_top = y - 22
        caja_altura = 122
        
        DocumentoPDF.dibujar_caja(canv, x0, caja_top, w, caja_altura)

        
        fila = caja_top - 30
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Número RC:", getattr(interno, "num_RC", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Nombre:", getattr(interno, "nombre", None))
        fila -= DocumentoPDF.espacio_fila
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Fecha Nacimiento:", getattr(interno, "fecha_nac", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Situación:", getattr(interno , "situacion_legal", None))
        fila -= DocumentoPDF.espacio_fila
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Delito de última condena:", getattr(interno, "delito", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Fecha ingreso:", getattr(interno, "fecha_ingreso", None))
        fila -= DocumentoPDF.espacio_fila
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Módulo:", getattr(interno, "modulo", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Duración condena (años):", getattr(interno, "condena", None))

        # Caja de datos de la solicitud
        y = caja_top - caja_altura - 28
        DocumentoPDF.dibujar_titulo_caja(canv, x0 + 24, y, "Datos de la solicitud")
        caja_top = y - 22
        caja_altura = 198
        DocumentoPDF.dibujar_caja(canv, x0, caja_top, w, caja_altura)

        fila = caja_top - 30
        fecha_creacion = getattr(getattr(solicitud, "entrevista", None), "fecha", None)
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Identificador:", getattr(solicitud, "id_solicitud", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Fecha Creación:", fecha_creacion)
        fila -= DocumentoPDF.espacio_fila

        # Reparto equitativo de la fila: tipo | motivo | urgencia
        columnas_3 = w - 72
        col1 = x_izq
        col2 = x_izq + (columnas_3 / 3)
        col3 = x_izq + (2 * columnas_3 / 3)
        DocumentoPDF.anadir_apartado(canv, col1, fila, "Tipo:", getattr(solicitud, "tipo", None))
        DocumentoPDF.anadir_apartado(canv, col2, fila, "Motivo:", getattr(solicitud, "motivo", None))
        DocumentoPDF.anadir_apartado(canv, col3, fila, "Urgencia:", getattr(solicitud, "urgencia", None))

        fila -= DocumentoPDF.espacio_fila
        canv.setFont("Helvetica-Bold", 10)
        canv.drawString(x_izq, fila, "Descripción:")
        DocumentoPDF.texto_linea(canv, x_izq + 65, fila, getattr(solicitud, "descripcion", None), 450, max_lines=2)

        fila -= DocumentoPDF.espacio_fila * 2
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Fecha inicio:", getattr(solicitud, "fecha_inicio", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Hora salida:", getattr(solicitud, "hora_salida", None))
        fila -= DocumentoPDF.espacio_fila
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Fecha fin:", getattr(solicitud, "fecha_fin", None))
        DocumentoPDF.anadir_apartado(canv, x_der, fila, "Hora entrada:", getattr(solicitud, "hora_llegada", None))
        fila -= DocumentoPDF.espacio_fila
        destino = ", ".join([
            DocumentoPDF.texto(getattr(solicitud, "direccion", None), ""),
            DocumentoPDF.texto(getattr(solicitud, "destino", None), ""),
            DocumentoPDF.texto(getattr(solicitud, "provincia", None), ""),
            DocumentoPDF.texto(getattr(solicitud, "cod_pos", None), "") 
        ]).strip()
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Dirección destino:", destino)


        # Caja de estado y observaciones
        y = caja_top - caja_altura - 28
        DocumentoPDF.dibujar_titulo_caja(canv, x0 + 24, y, "Estado de la solicitud")
        caja_top = y - 22
        caja_altura = 126
        DocumentoPDF.dibujar_caja(canv, x0, caja_top, w, caja_altura)

        fila = caja_top - 30
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Estado:", getattr(solicitud, "estado", None))
        fila -= DocumentoPDF.espacio_fila
        canv.setFont("Helvetica-Bold", 10)
        canv.drawString(x_izq, fila, "Observaciones:")
        DocumentoPDF.texto_linea(canv, x_izq + 80, fila, getattr(solicitud, "observaciones", None), 460, max_lines=1)
        fila -= DocumentoPDF.espacio_fila
        fecha_entrevista = getattr(getattr(solicitud, "entrevista", None), "fecha", None)
        DocumentoPDF.anadir_apartado(canv, x_izq, fila, "Fecha entrevista:", fecha_entrevista)
        fila -= DocumentoPDF.espacio_fila
        canv.setFont("Helvetica-Bold", 10)
        canv.drawString(x_izq, fila, "Conclusiones del profesional:")
        conclusiones = DocumentoPDF.texto(getattr(solicitud, "conclusiones_profesional", None), "sin comentarios")
        DocumentoPDF.texto_linea(canv, x_izq + 145, fila, conclusiones, 400, max_lines=1)

        canv.showPage()

        # Pagina 2
        DocumentoPDF.dibujar_pag(canv, ancho, alto)
        DocumentoPDF.dibujar_logo(canv, ancho, alto, tam=42)

        # Caja de contactos
        y2 = alto - 80
        DocumentoPDF.dibujar_titulo_caja(canv, x0 + 16, y2, "Datos de contactos")
        caja_top = y2 - 22
        caja_altura = 160
        DocumentoPDF.dibujar_caja(canv, x0 - 10, caja_top, w + 20, caja_altura)

        x1 = x0 + 30
        x2 = x0 + 215
        x3 = x0 + 390
        fila = caja_top - 24

        canv.setFont("Helvetica-Bold", 10)
        canv.drawString(x1, fila, "CONTACTO PRINCIPAL")
        fila -= DocumentoPDF.espacio_fila - 2
        DocumentoPDF.anadir_apartado(canv, x1, fila, "Nombre:", getattr(solicitud, "nombre_cp", None))
        DocumentoPDF.anadir_apartado(canv, x2, fila, "Teléfono:", getattr(solicitud, "telf_cp", None))
        DocumentoPDF.anadir_apartado(canv, x3, fila, "Relación:", getattr(solicitud, "relacion_cp", None))
        fila -= DocumentoPDF.espacio_fila
        DocumentoPDF.anadir_apartado(canv, x1, fila, "Dirección:", getattr(solicitud, "direccion_cp", None))
        fila -= DocumentoPDF.espacio_fila
        canv.setFont("Helvetica-Bold", 10)
        canv.drawString(x1, fila, "CONTACTO SECUNDARIO")
        fila -= DocumentoPDF.espacio_fila - 2
        DocumentoPDF.anadir_apartado(canv, x1, fila, "Nombre:", getattr(solicitud, "nombre_cs", None))
        DocumentoPDF.anadir_apartado(canv, x2, fila, "Teléfono:", getattr(solicitud, "telf_cs", None))
        DocumentoPDF.anadir_apartado(canv, x3, fila, "Relación:", getattr(solicitud, "relacion_cs", None))

        y2 = caja_top - caja_altura - 30
        DocumentoPDF.dibujar_titulo_caja(canv, x0 + 16, y2, "Compromisos", w=150)
        caja_top = y2 - 22
        caja_altura = 150
        DocumentoPDF.dibujar_caja(canv, x0 - 10, caja_top, w + 20, caja_altura)

        canv.setFont("Helvetica-Bold", 10)
        canv.drawString(x1, caja_top - 28, "Se ha comprometido a:")
        compromisos = decodificar(getattr(solicitud, "compromisos", 0), COMP_LABELS) or ["__________"]
        y_comp = caja_top - 48
        canv.setFont("Helvetica", 10)
        for comp in compromisos[:6]:
            canv.drawString(x1 + 8, y_comp, f"- {comp}")
            y_comp -= 17

        canv.setFillColor(colors.black)
        canv.setFont("Helvetica-Bold", 20)
        canv.drawString(x0, 255, "Firmas")

        canv.setFont("Helvetica", 11)
        canv.drawString(x0 + 55, 195, "Firma del interno")
        canv.drawString(x0 + 330, 195, "Firma del profesional")

        box_w = 210
        caja_altura = 90
        left_box_x = x0 + 5
        right_box_x = x0 + w - box_w - 5
        box_y = 95
        canv.setFillColor(DocumentoPDF.color_caja)
        canv.setStrokeColor(DocumentoPDF.color_borde)
        canv.roundRect(left_box_x, box_y, box_w, caja_altura, 12, stroke=1, fill=1)
        canv.roundRect(right_box_x, box_y, box_w, caja_altura, 12, stroke=1, fill=1)

        canv.setFillColor(colors.HexColor("#888888"))
        canv.setFont("Helvetica", 10)
        canv.drawString(left_box_x + 90, box_y + 28, "Fdo:")
        canv.drawString(right_box_x + 90, box_y + 28, "Fdo:")
        canv.save()
