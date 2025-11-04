from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency

# Camada de análise (ajuste estes nomes se seu módulo usar outros)
from modules.analysis.financial_analysis import (
    calculate_financial_summary,    # retorna dict {'receita','despesa','lucro'}
    get_expense_distribution        # retorna Series por categoria (somente despesas)
)

class DashboardFinancas(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        self.df_financas = pd.DataFrame()
        self.kpi_receita = None
        self.kpi_despesas = None
        self.kpi_lucro = None
        self.table_financas = None
        self.canvas_revexp = None
        self.canvas_pie = None
        self.layout_revexp = None
        self.layout_pie = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard Financeiro")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)
        self.kpi_receita  = KPIWidget("Receita Total",  value_color="#2E8B57")
        self.kpi_despesas = KPIWidget("Despesas Totais", value_color="#C21807")
        self.kpi_lucro    = KPIWidget("Lucro Líquido",   value_color="#FF8C00")
        kpi_layout.addWidget(self.kpi_receita)
        kpi_layout.addWidget(self.kpi_despesas)
        kpi_layout.addWidget(self.kpi_lucro)
        root.addLayout(kpi_layout)

        table_frame = QFrame(); table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_financas = QTableView()
        table_layout.addWidget(self.table_financas)
        root.addWidget(table_frame)

        charts_row = QHBoxLayout(); charts_row.setSpacing(16)
        chart1_frame = QFrame(); self.layout_revexp = QVBoxLayout(chart1_frame); self.layout_revexp.setContentsMargins(0,0,0,0)
        chart2_frame = QFrame(); self.layout_pie    = QVBoxLayout(chart2_frame); self.layout_pie.setContentsMargins(0,0,0,0)
        charts_row.addWidget(chart1_frame); charts_row.addWidget(chart2_frame)
        root.addLayout(charts_row)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")

    def _rebuild_kpis(self):
        s = calculate_financial_summary(self.df_financas)
        self.kpi_receita.setValue(fmt_currency(s.get('receita', 0.0)))
        self.kpi_despesas.setValue(fmt_currency(s.get('despesa', 0.0)))
        self.kpi_lucro.setValue(fmt_currency(s.get('lucro', 0.0)))

    def _rebuild_tables(self):
        # --- dados base ---
        df = self.df_financas.copy()

        # --- Formatação para a tabela ---
        if "Data" in df.columns:
            # Converte para datetime e depois formata como texto para exibição
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime('%d/%m/%Y')
        if "Valor" in df.columns:
            # Aplica a formatação de moeda
            df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0).apply(fmt_currency)

        # Renomeia as colunas para melhor visualização
        df = df.rename(columns={
            "Data": "Data",
            "Tipo": "Tipo",
            "Categoria": "Categoria",
            "Descricao": "Descrição",
            "Valor": "Valor (R$)",
            "Metodo_Pagamento": "Forma de Pagto."
        })

        # Define a ordem e quais colunas mostrar
        cols_to_show = ["Data", "Tipo", "Categoria", "Descrição", "Valor (R$)", "Forma de Pagto."]
        existing_cols = [col for col in cols_to_show if col in df.columns]

        # Atualiza a QTableView
        set_table_from_df(self.table_financas, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_revexp: self.layout_revexp.removeWidget(self.canvas_revexp); self.canvas_revexp.setParent(None)
        if self.canvas_pie:    self.layout_pie.removeWidget(self.canvas_pie);      self.canvas_pie.setParent(None)

        # Barra: Receita vs Despesa
        fig1 = Figure(figsize=(5.8, 3.8), dpi=100); ax1 = fig1.add_subplot(111)
        s = calculate_financial_summary(self.df_financas)
        ax1.bar(['Receita','Despesas'], [s.get('receita',0), s.get('despesa',0)])
        ax1.set_title("Receita vs. Despesas"); fig1.tight_layout()
        self.canvas_revexp = FigureCanvas(fig1); self.layout_revexp.addWidget(self.canvas_revexp)

        # Pizza: distribuição das despesas por categoria
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100); ax2 = fig2.add_subplot(111)
        ser = get_expense_distribution(self.df_financas)
        if not ser.empty:
            ax2.pie(ser.values, labels=ser.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Distribuição de Despesas"); fig2.tight_layout()
        self.canvas_pie = FigureCanvas(fig2); self.layout_pie.addWidget(self.canvas_pie)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()