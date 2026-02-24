import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

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


class RoundedTable(Table):
    """Tabla con fondo y borde redondeado para simular la caja del modelo."""

    def __init__(self, *args, radius=10, fill_color=colors.white, stroke_color=colors.black, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius
        self.fill_color = fill_color
        self.stroke_color = stroke_color

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.fill_color)
        self.canv.setStrokeColor(self.stroke_color)
        self.canv.setLineWidth(1)
        self.canv.roundRect(0, 0, self._width, self._height, self.radius, fill=1, stroke=1)
        self.canv.restoreState()
        super().draw()


class DocumentoPDF:
    color_pag = colors.white
    color_caja = colors.HexColor("#DEDEDE")
    color_borde = colors.HexColor("#B9B9B9")
    color_titulo_caja = colors.HexColor("#CFCFCF")

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
    def dibujar_logo(c, x, y, tam=42):
        path = DocumentoPDF.logo_inperia()
        if os.path.exists(path):
            c.drawImage(ImageReader(path), x, y, width=tam, height=tam, preserveAspectRatio=True, mask="auto")
        else:
            c.setFont("Times-Bold", 38)
            c.setFillColor(colors.black)
            c.drawString(x + 6, y + 2, "I")

    @staticmethod
    def _on_page(canvas, doc):
        """Callback para dibujar el fondo gris general y el encabezado en cada página."""
        canvas.saveState()
        
        # Fondo de la página
        canvas.setFillColor(DocumentoPDF.color_pag)
        canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
        
        alto = A4[1]
        
        # Encabezado dinámico dependiendo de si es la página 1 u otra
        if doc.page == 1:
            DocumentoPDF.dibujar_logo(canvas, 10, alto - 95, tam=92)
            canvas.setFillColor(colors.black)
            canvas.setFont("Helvetica", 16)
            canvas.drawString(74, alto - 42, "NPERIA")
            canvas.setFont("Helvetica-Bold", 31)
            canvas.drawString(74, alto - 67, "Comprobante de la solicitud")
        else:
            DocumentoPDF.dibujar_logo(canvas, 10, alto - 60, tam=42)
            
        canvas.restoreState()

    @staticmethod
    def generar_pdf_solicitud(solicitud, ruta_archivo, interno=None):
        # Configuramos el documento (los márgenes superiores e inferiores empujan el contenido)
        doc = SimpleDocTemplate(
            ruta_archivo, 
            pagesize=A4, 
            rightMargin=30, 
            leftMargin=30, 
            topMargin=110, 
            bottomMargin=40
        )

        # Hojas de estilo
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        style_normal.fontName = "Helvetica"
        style_normal.fontSize = 10
        style_normal.leading = 14

        style_bold = ParagraphStyle('Bold', parent=style_normal, fontName='Helvetica-Bold')
        style_justified = ParagraphStyle('Justify', parent=style_normal, alignment=TA_JUSTIFY)
        style_subtitle = ParagraphStyle('Sub', parent=style_bold, spaceBefore=10, spaceAfter=5)
        
        def p_field(label, value, justified=False):
            """Genera un párrafo con formato 'Negrita: Valor'."""
            val_str = DocumentoPDF.texto(value, " __________")
            st = style_justified if justified else style_normal
            return Paragraph(f"<b>{label}</b> {val_str}", st)

        def create_box(title, content_flowables):
            """Genera las cajas grises dinámicamente usando tablas y el renderizador redondeado."""
            title_p = Paragraph(f"<b>{title}</b>", ParagraphStyle('Title', parent=style_normal, fontSize=14, textColor=colors.black))
            
            # Pestaña superior redondeada (como en el modelo)
            t_title = RoundedTable(
                [[title_p]],
                colWidths=[220],
                rowHeights=[24],
                hAlign='LEFT',
                radius=11,
                fill_color=DocumentoPDF.color_titulo_caja,
                stroke_color=DocumentoPDF.color_titulo_caja,
            )
            t_title.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 28),
                ('RIGHTPADDING', (0,0), (-1,-1), 12),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            
            # Tabla para el contenido principal
            table_data = [[f] for f in content_flowables]
            t_content = RoundedTable(
                table_data,
                colWidths=[A4[0] - 60],
                hAlign='LEFT',
                radius=14,
                fill_color=DocumentoPDF.color_caja,
                stroke_color=DocumentoPDF.color_borde,
            )
            t_content.setStyle(TableStyle([
                ('LEFTPADDING', (0,0), (-1,-1), 18),
                ('RIGHTPADDING', (0,0), (-1,-1), 12),
                ('TOPPADDING', (0,0), (-1,0), 14),
                ('BOTTOMPADDING', (0,-1), (-1,-1), 14),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            
            return KeepTogether([t_title, t_content, Spacer(1, 15)])

        # Lista donde almacenaremos todos los elementos en orden (la "historia" del PDF)
        story = []

        # ---------------------------------------------------------------------
        # 1. Datos del interno
        # Usamos una tabla de 2 columnas para que los textos largos empujen el resto sin solaparse
        data_interno = [
            [p_field("Número RC:", getattr(interno, "num_RC", None)), p_field("Nombre:", getattr(interno, "nombre", None))],
            [p_field("Fecha Nacimiento:", getattr(interno, "fecha_nac", None)), p_field("Situación:", getattr(interno, "situacion_legal", None))],
            [p_field("Delito de última condena:", getattr(interno, "delito", None)), p_field("Fecha ingreso:", getattr(interno, "fecha_ingreso", None))],
            [p_field("Módulo:", getattr(interno, "modulo", None)), p_field("Duración condena (años):", getattr(interno, "condena", None))]
        ]
        t_interno = Table(data_interno, colWidths=[(A4[0]-84)/2]*2) # Ajuste ligero de ancho por padding
        t_interno.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(create_box("Datos del interno", [t_interno]))

        # ---------------------------------------------------------------------
        # 2. Datos de la solicitud
        t_sol_1 = Table([
            [p_field("Identificador:", getattr(solicitud, "id_solicitud", None)), p_field("Fecha Creación:", getattr(solicitud, "fecha_creacion", None))],
            [p_field("Tipo:", getattr(solicitud, "tipo", None)), p_field("Urgencia:", getattr(solicitud, "urgencia", None))],
        ], colWidths=[(A4[0]-84)/2]*2)
        t_sol_1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))

        t_sol_2 = Table([
            [p_field("Fecha inicio:", getattr(solicitud, "fecha_inicio", None)), p_field("Hora salida:", getattr(solicitud, "hora_salida", None))],
            [p_field("Fecha fin:", getattr(solicitud, "fecha_fin", None)), p_field("Hora entrada:", getattr(solicitud, "hora_llegada", None))],
        ], colWidths=[(A4[0]-84)/2]*2)
        t_sol_2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))

        # Formateo dinámico de la dirección para evitar comas sueltas
        partes_destino = [
            DocumentoPDF.texto(getattr(solicitud, "direccion", None), ""),
            DocumentoPDF.texto(getattr(solicitud, "destino", None), ""),
            DocumentoPDF.texto(getattr(solicitud, "provincia", None), ""),
            DocumentoPDF.texto(getattr(solicitud, "cod_pos", None), "")
        ]
        partes_destino = [p for p in partes_destino if p.strip() and p != "__________"]
        destino = ", ".join(partes_destino) if partes_destino else "__________"

        content_solicitud = [
            t_sol_1, 
            Spacer(1, 8),
            p_field("Motivo:", getattr(solicitud, "motivo", None), justified=True),
            Spacer(1, 8),
            p_field("Descripción:", getattr(solicitud, "descripcion", None), justified=True),
            Spacer(1, 8),
            t_sol_2,
            Spacer(1, 8),
            p_field("Dirección destino:", destino, justified=True)
        ]
        story.append(create_box("Datos de la solicitud", content_solicitud))

        # ---------------------------------------------------------------------
        # 3. Estado de la solicitud
        content_estado = [
            p_field("Estado:", getattr(solicitud, "estado", None)),
            Spacer(1, 8),
            p_field("Observaciones:", getattr(solicitud, "observaciones", None), justified=True),
            Spacer(1, 8),
            p_field("Fecha entrevista:", getattr(getattr(solicitud, "entrevista", None), "fecha", None)),
            Spacer(1, 8),
            p_field("Conclusiones del profesional:", getattr(solicitud, "conclusiones_profesional", None), justified=True)
        ]
        story.append(create_box("Estado de la solicitud", content_estado))

        # ---------------------------------------------------------------------
        # 4. Datos de contactos
        # Usamos tablas internas para alinear los campos de contacto
        t_cp = Table([
            [p_field("Nombre:", getattr(solicitud, "nombre_cp", None)), p_field("Teléfono:", getattr(solicitud, "telf_cp", None)), p_field("Relación:", getattr(solicitud, "relacion_cp", None))]
        ], colWidths=[(A4[0]-84)/3]*3)
        t_cp.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))

        t_cs = Table([
            [p_field("Nombre:", getattr(solicitud, "nombre_cs", None)), p_field("Teléfono:", getattr(solicitud, "telf_cs", None)), p_field("Relación:", getattr(solicitud, "relacion_cs", None))]
        ], colWidths=[(A4[0]-84)/3]*3)
        t_cs.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))

        content_contactos = [
            Paragraph("CONTACTO PRINCIPAL", style_subtitle),
            t_cp,
            Spacer(1, 4),
            p_field("Dirección:", getattr(solicitud, "direccion_cp", None)),
            Spacer(1, 8),
            Paragraph("CONTACTO SECUNDARIO", style_subtitle),
            t_cs
        ]
        story.append(create_box("Datos de contactos", content_contactos))

        # ---------------------------------------------------------------------
        # 5. Compromisos
        comp_intro = Paragraph("<b>Se ha comprometido a:</b>", style_normal)
        compromisos = decodificar(getattr(solicitud, "compromisos", 0), COMP_LABELS) or ["__________"]
        # Usamos un carácter de viñeta estándar
        comp_list = [Paragraph(f"• {comp}", style_normal) for comp in compromisos]
        story.append(create_box("Compromisos", [comp_intro, Spacer(1, 6)] + comp_list))

        # ---------------------------------------------------------------------
        # 6. Firmas
        # Añadimos espacio flexible antes de las firmas para intentar que queden al final si sobra sitio
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>Firmas</b>", ParagraphStyle('FirmaT', parent=style_normal, fontSize=20)))
        story.append(Spacer(1, 15))

        firma_box_left = RoundedTable(
            [[Paragraph("Fdo:", style_normal)]],
            colWidths=[230],
            rowHeights=[86],
            hAlign='CENTER',
            radius=12,
            fill_color=DocumentoPDF.color_caja,
            stroke_color=DocumentoPDF.color_borde,
        )
        firma_box_left.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))

        firma_box_right = RoundedTable(
            [[Paragraph("Fdo:", style_normal)]],
            colWidths=[230],
            rowHeights=[86],
            hAlign='CENTER',
            radius=12,
            fill_color=DocumentoPDF.color_caja,
            stroke_color=DocumentoPDF.color_borde,
        )
        firma_box_right.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))

        t_firmas = Table([
            [Paragraph("Firma del interno", style_normal), Paragraph("Firma del profesional", style_normal)],
            [firma_box_left, firma_box_right]
        ], colWidths=[(A4[0]-60)/2]*2)
        t_firmas.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(KeepTogether([t_firmas]))

        # ---------------------------------------------------------------------
        # Renderizado final del PDF
        # onFirstPage y onLaterPages dibujan el fondo gris general y los logos en cada página
        doc.build(story, onFirstPage=DocumentoPDF._on_page, onLaterPages=DocumentoPDF._on_page)
