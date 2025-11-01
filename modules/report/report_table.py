from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
import pandas as pd

def add_table(story, df, styles, available_width, colors_dict, max_rows=10):
    """Gera uma tabela bonita e adaptável ao conteúdo."""
    if df is None or df.empty:
        story.append(Paragraph("Sem dados para exibir.", styles['WrappedBody']))
        return

    headers = list(df.columns)
    header_row = [Paragraph(str(h), styles['HeaderCell']) for h in headers]

    body = [header_row]
    for _, row in df.head(max_rows).iterrows():
        cells = [Paragraph(str(v) if v is not None else "", styles['Cell']) for v in row]
        body.append(cells)

    avg_lens = [max(df[c].astype(str).str.len().mean(), len(c)) for c in df.columns]
    total = max(sum(avg_lens), 1)
    col_widths = [(l / total) * available_width for l in avg_lens]

    # Normalização para caber na página
    scale = available_width / sum(col_widths)
    col_widths = [w * scale for w in col_widths]

    t = Table(body, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors_dict['primary']),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors_dict['row_bg'], colors.white]),
    ]))

    story.append(t)
    story.append(Paragraph("*Exibindo as primeiras linhas.", styles['WrappedBody']))
    story.append(Spacer(1, 10))