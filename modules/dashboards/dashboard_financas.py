# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableView
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

# --- IMPORTAÇÕES CENTRALIZADAS ---
from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
# --- NOVA IMPORTAÇÃO DA CAMADA DE ANÁLISE ---
from modules.analysis.financial_analysis import calculate_financial_summary, get_expense_distribution


class DashboardFinancas(QWidget):
    """
    Dashboard Financeiro.
    - Utiliza a camada de análise para obter os dados calculados.
    - Focado apenas na apresentação dos dados.
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # Data
        self.df_financas = pd.DataFrame()

        # Widgets
        self.kpi_receita = None
        self.kpi_despesas = None
        self.kpi_lucro = None
        self.table_financas = None
        self.canvas_revexp = None
        self.canvas_pie = None

        # Layouts para os gráficos (holders)
        self.layout_revexp = None
        self.layout_pie = None

        self.build_ui()
        self.refresh()
    
    # ------------------------------------------------------------------
    # UI (Estrutura Estática)
    # ------------------------------------------------------------------
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard Financeiro")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)
        self.kpi_receita = KPIWidget("Receita Total", value_color="#2E8B57")
        self.kpi_despesas = KPIWidget("Despesas Totais", value_color="#C21807")
        self.kpi_lucro = KPIWidget("Lucro Líquido", value_color="#FF8C00")
        kpi_layout.addWidget(self.kpi_receita)
        kpi_layout.addWidget(self.kpi_despesas)
        kpi_layout.addWidget(self.kpi_lucro)
        root.addLayout(kpi_layout)

        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_financas = QTableView()
        table_layout.addWidget(self.table_financas)
        root.addWidget(table_frame)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)
        chart1_frame = QFrame()
        self.layout_revexp = QVBoxLayout(chart1_frame)
        self.layout_revexp.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart1_frame)
        chart2_frame = QFrame()
        self.layout_pie = QVBoxLayout(chart2_frame)
        self.layout_pie.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart2_frame)
        root.addLayout(charts_row)

    # ------------------------------------------------------------------
    # Ciclo de Atualização de Dados
    # ------------------------------------------------------------------
    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")

    def _rebuild_kpis(self):
        """Usa a camada de análise para obter os KPIs e os exibe."""
        summary = calculate_financial_summary(self.df_financas)
        
        self.kpi_receita.setValue(fmt_currency(summary['receita']))
        self.kpi_despesas.setValue(fmt_currency(summary['despesa']))
        self.kpi_lucro.setValue(fmt_currency(summary['lucro']))

    def _rebuild_tables(self):
        set_table_from_df(self.table_financas, self.df_financas)

    def _rebuild_charts(self):
        if self.canvas_revexp is not None:
            self.layout_revexp.removeWidget(self.canvas_revexp)
            self.canvas_revexp.setParent(None)
        if self.canvas_pie is not None:
            self.layout_pie.removeWidget(self.canvas_pie)
            self.canvas_pie.setParent(None)

        # Gráfico 1: Receita vs. Despesa (Usa a camada de análise)
        fig1 = Figure(figsize=(5.8, 3.8), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        summary = calculate_financial_summary(self.df_financas)
        ax1.bar(['Receita', 'Despesas'], [summary['receita'], summary['despesa']], color=['#2E8B57', '#C21807'])
        ax1.set_title("Receita vs. Despesas")
        fig1.tight_layout()
        self.canvas_revexp = FigureCanvas(fig1)
        self.layout_revexp.addWidget(self.canvas_revexp)

        # Gráfico 2: Pizza de despesas (Usa a camada de análise)
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        expense_series = get_expense_distribution(self.df_financas)
        if not expense_series.empty:
            ax2.pie(expense_series.values, labels=expense_series.index, autopct='%1.1f%%', startangle=90)
                
        ax2.set_title("Distribuição de Despesas")
        fig2.tight_layout()
        self.canvas_pie = FigureCanvas(fig2)
        self.layout_pie.addWidget(self.canvas_pie)

    # ------------------------------------------------------------------
    # Tema
    # ------------------------------------------------------------------
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()