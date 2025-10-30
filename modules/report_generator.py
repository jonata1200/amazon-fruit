# modules/report_generator.py

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

class ReportGenerator:
    """
    Gera um relatório PDF profissional com dados de todas as áreas do negócio.
    """
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.styles = getSampleStyleSheet()
        self.story = [] 

    def generate_report(self, file_path):
        """Método principal para gerar e salvar o relatório."""
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        self._create_title_page()
        self._create_finance_section()
        self._create_stock_section()
        self._create_customer_section()
        doc.build(self.story)
        
    def _create_title_page(self):
        self.story.append(Paragraph("Relatório de Gestão", self.styles['h1']))
        self.story.append(Paragraph("Amazon Fruit", self.styles['h2']))
        self.story.append(Spacer(1, 0.5 * inch))
        now = datetime.now()
        date_str = now.strftime("%d de %B de %Y, %H:%M:%S")
        self.story.append(Paragraph(f"Gerado em: {date_str}", self.styles['Normal']))
        self.story.append(Spacer(1, 2 * inch))

    def _create_finance_section(self):
        self.story.append(Paragraph("Análise Financeira", self.styles['h2']))
        df = self.data_handler.get_dataframe('Financas')
        entradas = df[df['Tipo'] == 'Entrada']['Valor'].sum()
        saidas = df[df['Tipo'] == 'Saída']['Valor'].sum()
        lucro = entradas - saidas
        self.story.append(Paragraph(f"<b>Receita Total:</b> R$ {entradas:,.2f}", self.styles['Normal']))
        self.story.append(Paragraph(f"<b>Despesas Totais:</b> R$ {saidas:,.2f}", self.styles['Normal']))
        self.story.append(Paragraph(f"<b>Lucro Líquido:</b> R$ {lucro:,.2f}", self.styles['Normal']))
        self.story.append(Spacer(1, 0.2 * inch))
        self.story.append(Paragraph("Últimas Transações:", self.styles['h3']))
        df_recent = df.tail(10)
        table_data = [df_recent.columns.to_list()] + df_recent.values.tolist()
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 0.5 * inch))

    def _create_stock_section(self):
        self.story.append(Paragraph("Análise de Estoque", self.styles['h2']))
        df = self.data_handler.get_dataframe('Estoque')
        df_low_stock = df[df['Quantidade_Estoque'] <= df['Nivel_Minimo_Estoque']]
        self.story.append(Paragraph(f"<b>Itens com Estoque Baixo:</b> {len(df_low_stock)}", self.styles['Normal']))
        self.story.append(Spacer(1, 0.2 * inch))
        if not df_low_stock.empty:
            self.story.append(Paragraph("Detalhes dos Itens Críticos:", self.styles['h3']))
            table_data = [df_low_stock.columns.to_list()] + df_low_stock.values.tolist()
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('TEXTCOLOR', (4,1), (4,-1), colors.red),
            ]))
            self.story.append(t)
        self._add_matplotlib_chart_to_story(df)
        self.story.append(Spacer(1, 0.5 * inch))

    def _create_customer_section(self):
        self.story.append(Paragraph("Análise de Público-Alvo", self.styles['h2']))
        df = self.data_handler.get_dataframe('Publico_Alvo')
        total_clientes = len(df)
        idade_media = df['Idade'].mean()
        self.story.append(Paragraph(f"<b>Total de Clientes Cadastrados:</b> {total_clientes}", self.styles['Normal']))
        self.story.append(Paragraph(f"<b>Idade Média dos Clientes:</b> {idade_media:.1f} anos", self.styles['Normal']))
        self.story.append(Spacer(1, 0.2 * inch))
        self.story.append(Paragraph("Lista de Clientes:", self.styles['h3']))
        table_data = [df.columns.to_list()] + df.values.tolist()
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 0.5 * inch))

    def _add_matplotlib_chart_to_story(self, df_estoque):
        from matplotlib import pyplot as plt
        category_counts = df_estoque['Categoria'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 3.5)) # Aumentei um pouco a altura para a legenda
        ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribuição de Produtos por Categoria')
        ax.axis('equal') 
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='PNG', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        
        # --- LINHA CORRIGIDA ---
        # Definimos uma largura fixa para a imagem, e a altura será calculada proporcionalmente.
        chart_image = Image(img_buffer, width=6*inch, height=3.5*inch, kind='proportional')

        self.story.append(chart_image)
        plt.close(fig)