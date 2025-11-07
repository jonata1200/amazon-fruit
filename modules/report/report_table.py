# modules/report/report_table.py

from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors

def add_table(story, df, styles, available_width, colors_dict, max_rows=10):
    """Gera uma tabela bonita e adaptável ao conteúdo."""
    if df is None or df.empty:
        story.append(Paragraph("Sem dados para exibir no período selecionado.", styles['WrappedBody']))
        return

    # Limita o número de linhas para não estourar a página
    df_display = df.head(max_rows)

    headers = list(df_display.columns)
    header_row = [Paragraph(str(h), styles['HeaderCell']) for h in headers]

    body_data = [header_row]
    for _, row in df_display.iterrows():
        cells = [Paragraph(str(v) if v is not None else "", styles['Cell']) for v in row]
        body_data.append(cells)

    # --- MUDANÇA PRINCIPAL AQUI: Lógica de largura simplificada ---
    # Divide o espaço da página igualmente entre o número de colunas.
    # Isso evita a quebra incorreta de cabeçalhos.
    num_cols = len(headers)
    col_widths = [available_width / num_cols] * num_cols
    # --- FIM DA MUDANÇA ---

    t = Table(body_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors_dict['primary']),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors_dict['row_bg'], colors.white]),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    story.append(t)
    if len(df) > max_rows:
        story.append(Paragraph(f"*Exibindo as primeiras {max_rows} de {len(df)} linhas.", styles['WrappedBody']))
    story.append(Spacer(1, 10))