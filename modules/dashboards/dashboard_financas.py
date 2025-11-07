# modules/dashboards/dashboard_financas.py

import pandas as pd
import matplotlib.pyplot as plt  # <-- MUDANÇA AQUI

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel,
    QTableView, QTabWidget, QHeaderView
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from modules.analysis.financial_analysis import calculate_financial_summary
from modules.ui.qt_utils import df_to_model
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from .chart_generator import (
    create_finance_evolution_chart,
    create_top_expenses_chart,
    create_top_revenues_chart
)

class DashboardFinancas(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_financas = pd.DataFrame()
        self.kpi_receita, self.kpi_despesas, self.kpi_lucro, self.kpi_margem_lucro = None, None, None, None
        self.table_extrato = None

        self.canvas_evolucao, self.canvas_top_despesas, self.canvas_top_receitas = None, None, None
        self.layout_evolucao, self.layout_top_despesas = QVBoxLayout(), QVBoxLayout()
        self.layout_top_receitas = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20, 20, 20, 20); root.setSpacing(16)
        title = QLabel("Dashboard Financeiro"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)
        
        kpi_layout = QGridLayout(); kpi_layout.setSpacing(16)
        self.kpi_receita = KPIWidget("Receita Total", value_color="#2E8B57"); self.kpi_despesas = KPIWidget("Despesas Totais", value_color="#C21807")
        self.kpi_lucro = KPIWidget("Lucro Líquido", value_color="#FF8C00"); self.kpi_margem_lucro = KPIWidget("Margem de Lucro", value_color="#6A0DAD")
        kpi_layout.addWidget(self.kpi_receita, 0, 0); kpi_layout.addWidget(self.kpi_despesas, 0, 1)
        kpi_layout.addWidget(self.kpi_lucro, 0, 2); kpi_layout.addWidget(self.kpi_margem_lucro, 0, 3)
        root.addLayout(kpi_layout)
        
        tab_widget = QTabWidget()
        evolucao_widget = QWidget(); evolucao_widget.setLayout(self.layout_evolucao)
        tab_widget.addTab(evolucao_widget, "📈 Evolução Mensal")

        top_despesas_widget = QWidget(); top_despesas_widget.setLayout(self.layout_top_despesas)
        tab_widget.addTab(top_despesas_widget, "📊 Top Despesas")

        top_receitas_widget = QWidget(); top_receitas_widget.setLayout(self.layout_top_receitas)
        tab_widget.addTab(top_receitas_widget, "💰 Top Receitas")

        self.table_extrato = QTableView()
        tab_widget.addTab(self.table_extrato, "📋 Extrato Detalhado")
        root.addWidget(tab_widget)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")

    def _rebuild_kpis(self):
        s = calculate_financial_summary(self.df_financas); receita = s.get('receita', 0.0); lucro = s.get('lucro', 0.0); margem = (lucro / receita) * 100 if receita > 0 else 0.0
        self.kpi_receita.setValue(fmt_currency(receita)); self.kpi_despesas.setValue(fmt_currency(s.get('despesa', 0.0))); self.kpi_lucro.setValue(fmt_currency(lucro)); self.kpi_margem_lucro.setValue(f"{margem:.1f}%")

    def _rebuild_tables(self):
        df = self.df_financas.copy()
        if df is None or df.empty: self.table_extrato.setModel(None); return
        if "Data" in df.columns: df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime('%d/%m/%Y')
        if "Valor" in df.columns: df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0).apply(fmt_currency)
        rename_map = {"Data": "Data", "Tipo": "Tipo", "Categoria": "Categoria", "Descricao": "Descrição", "Valor": "Valor", "Forma de Pagamento": "Forma de Pagamento"}
        df = df.rename(columns=rename_map)
        cols_to_show = ["Data", "Tipo", "Categoria", "Descrição", "Valor", "Forma de Pagamento"]; df_display = df[[col for col in cols_to_show if col in df.columns]]
        model = df_to_model(df_display); self.table_extrato.setModel(model); self.table_extrato.setAlternatingRowColors(True); header = self.table_extrato.horizontalHeader()
        if header.count() > 0:
            try:
                desc_index = df_display.columns.get_loc("Descrição")
                for i in range(header.count()): header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch if i == desc_index else QHeaderView.ResizeMode.ResizeToContents)
            except KeyError: header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _rebuild_charts(self):
        if self.canvas_evolucao: self.layout_evolucao.removeWidget(self.canvas_evolucao); self.canvas_evolucao.deleteLater(); self.canvas_evolucao = None
        if self.canvas_top_despesas: self.layout_top_despesas.removeWidget(self.canvas_top_despesas); self.canvas_top_despesas.deleteLater(); self.canvas_top_despesas = None
        if self.canvas_top_receitas: self.layout_top_receitas.removeWidget(self.canvas_top_receitas); self.canvas_top_receitas.deleteLater(); self.canvas_top_receitas = None

        # Gráfico 1: Evolução Mensal
        fig1 = create_finance_evolution_chart(self.df_financas)
        self.canvas_evolucao = FigureCanvas(fig1)
        self.layout_evolucao.addWidget(self.canvas_evolucao)
        plt.close(fig1)  # <-- MUDANÇA AQUI
        
        # Gráfico 2: Top 5 Despesas
        fig2 = create_top_expenses_chart(self.df_financas)
        self.canvas_top_despesas = FigureCanvas(fig2)
        self.layout_top_despesas.addWidget(self.canvas_top_despesas)
        plt.close(fig2)  # <-- MUDANÇA AQUI

        # Gráfico 3: Top 5 Receitas
        fig3 = create_top_revenues_chart(self.df_financas)
        self.canvas_top_receitas = FigureCanvas(fig3)
        self.layout_top_receitas.addWidget(self.canvas_top_receitas)
        plt.close(fig3)  # <-- MUDANÇA AQUI