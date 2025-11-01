# modules/report/report_generator.py
import locale
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from .report_cover import add_cover
from .report_table import add_table
from .report_charts import (
    add_finance_charts, add_inventory_charts, add_public_charts,
    add_suppliers_charts, add_hr_charts
)
from .report_kpis import (
    add_kpis_estoque, add_kpis_financas, add_kpis_publico,
    add_kpis_fornecedores, add_kpis_rh
)

class ReportGenerator:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.story = []
        self.available_width = None

        self.colors = {
            'primary': colors.HexColor('#6A0DAD'),
            'secondary': colors.HexColor('#FF8C00'),
            'accent': colors.HexColor('#2E8B57'),
            'text': colors.HexColor('#333333'),
            'row_bg': colors.HexColor('#F7F7F9')
        }
        self.styles = self._setup_styles()

        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            pass

    def _setup_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='WrappedBody', parent=styles['Normal'], alignment=TA_LEFT,
            fontSize=10, leading=14, textColor=self.colors['text'], spaceAfter=6
        ))
        styles.add(ParagraphStyle(
            name='Cell', parent=styles['Normal'], fontSize=8, leading=10,
            textColor=self.colors['text']
        ))
        styles.add(ParagraphStyle(
            name='HeaderCell', parent=styles['Normal'], fontSize=9,
            leading=11, textColor=colors.white
        ))
        styles.add(ParagraphStyle(
            name='SectionTitle', parent=styles['Normal'], fontSize=14,
            textColor=self.colors['primary']
        ))
        styles.add(ParagraphStyle(
            name='ReportTitle', parent=styles['Normal'], fontSize=20,
            textColor=self.colors['primary']
        ))
        return styles

    def _section(self, title):
        self.story.append(Spacer(1, 8))
        self.story.append(Paragraph(title, self.styles['SectionTitle']))
        self.story.append(Spacer(1, 6))

    def _p(self, text): self.story.append(Paragraph(text, self.styles['WrappedBody']))

    def generate_report(self, file_path: str):
        # Letter (pontos): 612x792 — usando margins p/ boa área útil
        doc = SimpleDocTemplate(
            file_path, pagesize=(612, 792),
            leftMargin=45, rightMargin=45, topMargin=40, bottomMargin=40
        )
        self.available_width = doc.width
        self.story = []

        # Capa
        add_cover(self.story, self.styles, self.colors)

        # Resumo
        self._section("Resumo Geral")
        self._p(f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}.")

        # -------- ESTOQUE --------
        df_estoque = self.data_handler.load_table("Estoque")
        self._section("Estoque")
        add_kpis_estoque(self.story, df_estoque, self.colors)
        add_table(self.story, df_estoque, self.styles, self.available_width, self.colors)
        add_inventory_charts(self.story, df_estoque)
        self.story.append(PageBreak())

        # -------- FINANÇAS --------
        df_fin = self.data_handler.load_table("Financas")
        self._section("Finanças")
        add_kpis_financas(self.story, df_fin, self.colors)
        add_table(self.story, df_fin, self.styles, self.available_width, self.colors)
        add_finance_charts(self.story, df_fin)
        self.story.append(PageBreak())

        # -------- PÚBLICO-ALVO --------
        df_pub = self.data_handler.load_table("Publico_Alvo")
        self._section("Público-Alvo")
        add_kpis_publico(self.story, df_pub, self.colors)
        add_table(self.story, df_pub, self.styles, self.available_width, self.colors)
        add_public_charts(self.story, df_pub)
        self.story.append(PageBreak())

        # -------- FORNECEDORES --------
        df_forn = self.data_handler.load_table("Fornecedores")
        self._section("Fornecedores")
        add_kpis_fornecedores(self.story, df_forn, self.colors)
        add_table(self.story, df_forn, self.styles, self.available_width, self.colors)
        add_suppliers_charts(self.story, df_forn)
        self.story.append(PageBreak())

        # -------- RH --------
        df_rh = self.data_handler.load_table("Recursos_Humanos")
        self._section("Recursos Humanos")
        add_kpis_rh(self.story, df_rh, self.colors)
        add_table(self.story, df_rh, self.styles, self.available_width, self.colors)
        add_hr_charts(self.story, df_rh)

        doc.build(self.story)