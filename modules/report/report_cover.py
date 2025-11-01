from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

def add_cover(story, styles, colors_dict):
    """Adiciona capa institucional ao relatório."""
    story.append(Spacer(1, 140))
    story.append(Paragraph("Amazon Fruit", ParagraphStyle(
        'CoverTitle',
        alignment=TA_CENTER,
        fontSize=28,
        leading=32,
        textColor=colors_dict['primary']
    )))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Relatório Consolidado", ParagraphStyle(
        'CoverSub',
        alignment=TA_CENTER,
        fontSize=16,
        leading=20,
        textColor=colors_dict['text']
    )))
    story.append(Spacer(1, 250))
    story.append(Paragraph(datetime.now().strftime("Gerado em %d/%m/%Y"),
                           ParagraphStyle('CoverDate', alignment=TA_CENTER,
                                          fontSize=10, textColor=colors.grey)))
    story.append(PageBreak())