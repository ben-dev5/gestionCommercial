from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime


class SalesOrderPDFService:
    def __init__(self):
        self.page_width = A4[0]
        self.page_height = A4[1]
        self.styles = getSampleStyleSheet()
        self.primary_color = HexColor('#2C5AA0')  # Bleu professionnel
        self.secondary_color = HexColor('#E8EEF7')  # Bleu clair

    def generate_pdf(self, sales_order, lines):
        """Générer un PDF pour un devis/commande"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )

        story = []

        # En-tête avec titre et infos devis
        story.extend(self._build_header(sales_order))
        story.append(Spacer(1, 0.5*cm))

        # Informations client
        story.extend(self._build_client_info(sales_order))
        story.append(Spacer(1, 0.5*cm))

        # Tableau des produits
        story.extend(self._build_products_table(lines))
        story.append(Spacer(1, 0.5*cm))

        # Totaux
        story.extend(self._build_totals(lines))
        story.append(Spacer(1, 1*cm))

        # Pied de page
        story.extend(self._build_footer())

        doc.build(story)
        buffer.seek(0)
        return buffer

    def _build_header(self, sales_order):
        """Construire l'en-tête du devis"""
        elements = []

        # Titre principal
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.primary_color,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        title = Paragraph(
            'HESTIA CRM',
            title_style
        )
        elements.append(title)

        # Sous-titre type de devis
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=self.primary_color,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        subtitle = Paragraph(
            f"{sales_order.type}",
            subtitle_style
        )
        elements.append(subtitle)

        # Infos devis et date
        info_style = ParagraphStyle(
            'Info',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#333333'),
            spaceAfter=10,
            alignment=TA_CENTER
        )

        date_str = sales_order.created_at.strftime('%d/%m/%Y') if sales_order.created_at else datetime.now().strftime('%d/%m/%Y')
        info_text = f"Genre: {sales_order.genre} | Date: {date_str}"
        info = Paragraph(info_text, info_style)
        elements.append(info)

        return elements

    def _build_client_info(self, sales_order):
        """Construire les infos client"""
        elements = []

        contact = sales_order.contact_id

        info_data = [
            ['FACTURER À:', f"{contact.first_name} {contact.last_name}"],
            ['Adresse:', f"{contact.address}"],
            ['Ville:', f"{contact.city} {contact.zip_code}"],
            ['Email:', f"{contact.email}"],
            ['Téléphone:', f"{contact.phone}"],
        ]

        if contact.siret:
            info_data.append(['SIRET:', f"{contact.siret}"])

        table = Table(info_data, colWidths=[3*cm, 12*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))

        elements.append(table)
        return elements

    def _build_products_table(self, lines):
        """Construire le tableau des produits"""
        elements = []

        # En-tête du tableau
        data = [[
            Paragraph('<b>Produit</b>', self.styles['Normal']),
            Paragraph('<b>Genre</b>', self.styles['Normal']),
            Paragraph('<b>Quantité</b>', self.styles['Normal']),
            Paragraph('<b>Prix HT</b>', self.styles['Normal']),
            Paragraph('<b>Taxe</b>', self.styles['Normal']),
            Paragraph('<b>Total HT</b>', self.styles['Normal']),
            Paragraph('<b>Total TTC</b>', self.styles['Normal']),
        ]]

        # Ajouter les lignes de produits
        total_ht = 0
        total_ttc = 0

        for line in lines:
            total_line_ht = line.price_ht * line.quantity
            total_line_ttc = total_line_ht * (1 + line.tax / 100)

            total_ht += total_line_ht
            total_ttc += total_line_ttc

            data.append([
                Paragraph(line.product_id.product_description, self.styles['Normal']),
                Paragraph(line.genre or '-', self.styles['Normal']),
                Paragraph(str(line.quantity), self.styles['Normal']),
                Paragraph(f"{line.price_ht:.2f}€", self.styles['Normal']),
                Paragraph(f"{line.tax:.2f}%", self.styles['Normal']),
                Paragraph(f"{total_line_ht:.2f}€", self.styles['Normal']),
                Paragraph(f"{total_line_ttc:.2f}€", self.styles['Normal']),
            ])

        # Créer le tableau
        colwidths = [3.5*cm, 2*cm, 1.5*cm, 1.8*cm, 1.3*cm, 1.8*cm, 1.8*cm]
        table = Table(data, colWidths=colwidths)

        # Style du tableau
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Lignes alternées
            ('BACKGROUND', (0, 1), (-1, -1), self.secondary_color),
            ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),

            # Bordures
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.secondary_color]),
        ]))

        elements.append(table)
        return elements

    def _build_totals(self, lines):
        """Construire la section des totaux"""
        elements = []

        # Calculer les totaux
        total_ht = sum(line.price_ht * line.quantity for line in lines)
        total_tax = sum(line.price_ht * line.quantity * line.tax / 100 for line in lines)
        total_ttc = total_ht + total_tax

        # Tableau des totaux
        totals_data = [
            ['', 'Total HT:', f"{total_ht:.2f}€"],
            ['', 'Total Taxe:', f"{total_tax:.2f}€"],
            ['', 'TOTAL TTC:', f"{total_ttc:.2f}€"],
        ]

        table = Table(totals_data, colWidths=[8*cm, 3*cm, 2*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (1, 0), (1, 1), 'Helvetica'),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 2), (-1, 2), 12),
            ('TEXTCOLOR', (1, 2), (-1, 2), white),
            ('BACKGROUND', (1, 2), (-1, 2), self.primary_color),
            ('TOPPADDING', (1, 2), (-1, 2), 8),
            ('BOTTOMPADDING', (1, 2), (-1, 2), 8),
        ]))

        elements.append(table)
        return elements

    def _build_footer(self):
        """Construire le pied de page"""
        elements = []

        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=5
        )

        footer_text = "Merci pour votre confiance | HESTIA CRM"
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)

        return elements

