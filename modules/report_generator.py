# modules/report_generator.py
import io
import locale
from datetime import datetime
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


class ReportGenerator:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.story = []
        self.available_width = None  # setado ao gerar o doc

        self.colors = {
            'primary': colors.HexColor('#6A0DAD'),
            'secondary': colors.HexColor('#FF8C00'),
            'accent': colors.HexColor('#2E8B57'),
            'text': colors.HexColor('#333333'),
            'light_grey': colors.HexColor('#F0F0F0')
        }
        self._setup_styles()

        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            pass

    def _setup_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='WrappedBody',
            parent=styles['Normal'],
            alignment=TA_LEFT,
            fontSize=9,
            leading=13,
            textColor=self.colors['text'],
            spaceAfter=6
        ))
        styles.add(ParagraphStyle(
            name='Cell',
            parent=styles['Normal'],
            fontSize=8,
            leading=11,
            textColor=self.colors['text']
        ))
        styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=styles['Heading2'],
            alignment=TA_LEFT,
            textColor=self.colors['primary'],
            spaceAfter=8
        ))
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Title'],
            alignment=TA_CENTER,
            textColor=self.colors['primary']
        ))
        self.styles = styles

    # --------------------------
    # Geração principal
    # --------------------------
    def generate_report(self, file_path: str):
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            leftMargin=45,
            rightMargin=45,
            topMargin=40,
            bottomMargin=40,
        )
        self.available_width = doc.width

        self.story = []
        self._title("Relatório Consolidado - Amazon Fruit")

        self._section("Resumo Geral")
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        self._p(f"Relatório gerado em {now_str}.")

        # Seções
        self._make_section("Estoque")
        self._make_section("Financas")
        self._make_section("Publico_Alvo")
        self._make_section("Fornecedores")
        self._make_section("Recursos_Humanos")

        doc.build(self.story)

    # --------------------------
    # Seções
    # --------------------------
    def _make_section(self, name: str):
        df = self.data_handler.load_table(name)
        self._section(name.replace("_", " "))
        self._add_table(df, max_rows=12)
        if name == "Financas":
            self._add_revenue_vs_expense_chart(df)
        elif name == "Fornecedores":
            self._add_suppliers_rating_pie(df)
        self.story.append(PageBreak())

    # --------------------------
    # Helpers de texto
    # --------------------------
    def _title(self, text):
        self.story.append(Paragraph(text, self.styles['ReportTitle']))
        self.story.append(Spacer(1, 12))

    def _section(self, text):
        self.story.append(Spacer(1, 8))
        self.story.append(Paragraph(text, self.styles['SectionTitle']))
        self.story.append(Spacer(1, 4))

    def _p(self, text):
        self.story.append(Paragraph(text, self.styles['WrappedBody']))

    # --------------------------
    # TABELAS
    # --------------------------
    def _add_table(self, df, max_rows=10):
        if df is None or df.empty:
            self._p("Sem dados para exibir.")
            return

        headers = list(df.columns)

        # Converte todas as células para Paragraph para permitir wrap
        body = [ [Paragraph(str(h), self.styles['Cell']) for h in headers] ]
        for _, row in df.head(max_rows).iterrows():
            cells = []
            for v in row.values:
                txt = "" if v is None else str(v)
                cells.append(Paragraph(txt, self.styles['Cell']))
            body.append(cells)

        # Largura proporcional às colunas dentro da largura útil da página
        col_count = len(headers)
        col_width = self.available_width / max(col_count, 1)
        col_widths = [col_width] * col_count

        t = Table(body, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))
        self.story.append(t)
        self._p("*Exibindo as primeiras linhas.")
        self.story.append(Spacer(1, 10))

    # --------------------------
    # GRÁFICOS (fit com proporção preservada)
    # --------------------------
    def _image_fit(self, png_bytes: bytes, max_w_in=6.2, max_h_in=3.6):
        """
        Retorna um objeto Image redimensionado para caber em (max_w, max_h) em polegadas,
        preservando a proporção.
        """
        reader = ImageReader(io.BytesIO(png_bytes))
        iw, ih = reader.getSize()  # pixels
        max_w = max_w_in * inch
        max_h = max_h_in * inch
        scale = min(max_w / iw, max_h / ih)
        w = iw * scale
        h = ih * scale
        return Image(io.BytesIO(png_bytes), width=w, height=h)

    def _add_revenue_vs_expense_chart(self, df):
        if df is None or df.empty:
            return
        try:
            entradas = df[df['Categoria'].astype(str).str.contains('Venda', na=False)]['Valor'].sum()
            saidas = df[df['Categoria'].astype(str).str.contains('Compra', na=False)]['Valor'].sum()
        except Exception:
            return

        fig, ax = plt.subplots(figsize=(5.5, 3.0), dpi=120)
        ax.bar(['Entradas', 'Saídas'], [entradas, saidas], color=['#2E8B57', '#FF6347'])
        ax.set_title('Entradas vs. Saídas', fontsize=11)
        ax.set_ylabel('Valor (R$)')
        ax.grid(axis='y', alpha=0.3)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='PNG', dpi=200, bbox_inches='tight')
        plt.close(fig)
        png = buf.getvalue()
        self.story.append(self._image_fit(png, max_w_in=6.2, max_h_in=3.2))
        self.story.append(Spacer(1, 10))

    def _add_suppliers_rating_pie(self, df):
        if df is None or df.empty or 'Avaliacao' not in df.columns:
            return
        counts = df['Avaliacao'].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(5.0, 3.0), dpi=120)
        ax.pie(counts.values, labels=[str(x) for x in counts.index],
               autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribuição de Avaliações dos Fornecedores', fontsize=11)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='PNG', dpi=200, bbox_inches='tight')
        plt.close(fig)
        png = buf.getvalue()
        self.story.append(self._image_fit(png, max_w_in=6.0, max_h_in=3.2))
        self.story.append(Spacer(1, 10))