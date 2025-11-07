# modules/report/report_generator.py

from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from .report_cover import add_cover
from .report_table import add_table
from .report_kpis import add_kpis_estoque, add_kpis_financas, add_kpis_publico, add_kpis_fornecedores, add_kpis_rh
from .report_charts import add_finance_charts, add_inventory_charts, add_public_charts, add_suppliers_charts, add_hr_charts
from .report_formatter import format_df_for_report

class ReportGenerator:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.story = []
        self.styles = self._setup_styles()
        # --- CORREÇÃO APLICADA AQUI ---
        self.colors = {
            'primary': colors.HexColor('#6A0DAD'), 'text': colors.HexColor('#333333'),
            'row_bg': colors.HexColor('#F7F7F9')
        }
        # --- FIM DA CORREÇÃO ---

    def _setup_styles(self):
        styles = getSampleStyleSheet()
        base_style = dict(fontName='Helvetica', fontSize=10, leading=14, textColor=self.colors['text'])
        styles.add(ParagraphStyle(name='WrappedBody', **base_style))
        styles.add(ParagraphStyle(name='Cell', parent=styles['Normal'], fontSize=8))
        styles.add(ParagraphStyle(name='HeaderCell', parent=styles['Normal'], fontSize=8, textColor=colors.white, fontName='Helvetica-Bold'))
        styles.add(ParagraphStyle(name='SectionTitle', parent=styles['h2'], fontSize=14, textColor=self.colors['primary'], spaceBefore=12))
        return styles

    def generate_report(self, file_path: str):
        doc = SimpleDocTemplate(file_path, pagesize=(595.27, 841.89), leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45)
        self.story = []

        add_cover(self.story, self.styles, self.colors)
        
        # --- Resumo Geral ---
        self.story.append(Paragraph("Resumo Geral", self.styles['SectionTitle']))
        period = self.data_handler.get_period()
        period_str = f"de {period[0]} a {period[1]}" if period else "todos os dados"
        self.story.append(Paragraph(f"Relatório gerado em {datetime.now():%d/%m/%Y %H:%M}. Período selecionado: {period_str}.", self.styles['WrappedBody']))

        # --- Seção de Estoque ---
        self.story.append(PageBreak())
        self.story.append(Paragraph("Estoque", self.styles['SectionTitle']))
        df_est = self.data_handler.load_table("Estoque")
        df_fin = self.data_handler.load_table("Financas")
        df_est_full_unfiltered = self.data_handler.load_full_unfiltered_table("Estoque")
        add_kpis_estoque(self.story, df_est, self.colors)
        df_est_fmt = format_df_for_report(df_est, "Estoque")
        add_table(self.story, df_est_fmt, self.styles, doc.width, self.colors)
        add_inventory_charts(self.story, df_fin, df_est_full_unfiltered)

        # --- Seção de Finanças ---
        self.story.append(PageBreak())
        self.story.append(Paragraph("Finanças", self.styles['SectionTitle']))
        add_kpis_financas(self.story, df_fin, self.colors)
        df_fin_fmt = format_df_for_report(df_fin, "Financas")
        add_table(self.story, df_fin_fmt, self.styles, doc.width, self.colors)
        add_finance_charts(self.story, df_fin)

        # --- Seção de Público-Alvo ---
        self.story.append(PageBreak())
        self.story.append(Paragraph("Público-Alvo", self.styles['SectionTitle']))
        df_pub = self.data_handler.load_table("Publico_Alvo")
        add_kpis_publico(self.story, df_pub, self.colors)
        df_pub_fmt = format_df_for_report(df_pub, "Publico_Alvo")
        add_table(self.story, df_pub_fmt, self.styles, doc.width, self.colors)
        add_public_charts(self.story, df_pub)

        # --- Seção de Fornecedores ---
        self.story.append(PageBreak())
        self.story.append(Paragraph("Fornecedores", self.styles['SectionTitle']))
        df_forn = self.data_handler.load_table("Fornecedores")
        add_kpis_fornecedores(self.story, df_forn, self.colors)
        df_forn_fmt = format_df_for_report(df_forn, "Fornecedores")
        add_table(self.story, df_forn_fmt, self.styles, doc.width, self.colors)
        add_suppliers_charts(self.story, df_forn)

        # --- Seção de Recursos Humanos ---
        self.story.append(PageBreak())
        self.story.append(Paragraph("Recursos Humanos", self.styles['SectionTitle']))
        df_rh = self.data_handler.load_table("Recursos_Humanos")
        add_kpis_rh(self.story, df_rh, self.colors)
        df_rh_fmt = format_df_for_report(df_rh, "Recursos_Humanos")
        add_table(self.story, df_rh_fmt, self.styles, doc.width, self.colors)
        add_hr_charts(self.story, df_rh)

        doc.build(self.story)