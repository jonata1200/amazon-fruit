# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from modules.analysis.financial_analysis import (
    calculate_financial_summary,
    get_expense_distribution
)

class DashboardFinancas(QWidget):
    def __init__(self, data_handler): # Argumento de tema removido
        super().__init__()
        self.data_handler = data_handler
        # self.theme_name removido

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
        root.setContentsMargins(20, 20, 20, 20); root.setSpacing(16)

        title = QLabel("Dashboard Financeiro")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(16)
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
        df = self.df_financas.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_financas, pd.DataFrame())
            return

        # Formatação para a tabela
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime('%d/%m/%Y')
        if "Valor" in df.columns:
            df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0).apply(fmt_currency)

        # Renomeia e seleciona colunas
        rename_map = {
            "Data": "Data", "Tipo": "Tipo", "Categoria": "Categoria",
            "Descricao": "Descrição", "Valor": "Valor",
            "Metodo_Pagamento": "Forma de Pagto."
        }
        df = df.rename(columns=rename_map)
        
        cols_to_show = ["Data", "Tipo", "Categoria", "Descrição", "Valor", "Forma de Pagto."]
        existing_cols = [col for col in cols_to_show if col in df.columns]
        
        set_table_from_df(self.table_financas, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_revexp: self.layout_revexp.removeWidget(self.canvas_revexp); self.canvas_revexp.setParent(None)
        if self.canvas_pie:    self.layout_pie.removeWidget(self.canvas_pie);      self.canvas_pie.setParent(None)

        # Cores fixas para o tema claro
        text_color = 'black'
        bg_color = '#FFFFFF'

        # Gráfico 1: Barra Receita vs Despesa
        fig1 = Figure(figsize=(5.8, 3.8), dpi=100); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        s = calculate_financial_summary(self.df_financas)
        ax1.bar(['Receita','Despesas'], [s.get('receita',0), s.get('despesa',0)], color=['#2E8B57', '#C21807'])
        ax1.set_title("Receita vs. Despesas", color=text_color)
        ax1.tick_params(axis='x', colors=text_color)
        ax1.tick_params(axis='y', colors=text_color)
        fig1.tight_layout()
        self.canvas_revexp = FigureCanvas(fig1); self.layout_revexp.addWidget(self.canvas_revexp)

        # Gráfico 2: Pizza de distribuição das despesas
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111)
        ser = get_expense_distribution(self.df_financas)
        if not ser.empty:
            wedges, texts, autotexts = ax2.pie(ser.values, autopct='%1.1f%%', startangle=90)
            ax2.legend(wedges, ser.index, title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        ax2.set_title("Distribuição de Despesas", color=text_color)
        fig2.tight_layout()
        self.canvas_pie = FigureCanvas(fig2); self.layout_pie.addWidget(self.canvas_pie)