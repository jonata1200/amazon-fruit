# modules/dashboards/dashboard_geral.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QPushButton, QFileDialog, QMessageBox
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from ..report.report_generator import ReportGenerator
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from modules.analysis.financial_analysis import calculate_financial_summary
from modules.analysis.inventory_analysis import analyze_inventory_kpis

class DashboardGeral(QWidget):
    def __init__(self, data_handler): # Argumento de tema removido
        super().__init__()
        self.data_handler = data_handler
        # self.theme_name removido

        # DataFrames
        self.df_financas = pd.DataFrame()
        self.df_estoque = pd.DataFrame()
        self.df_clientes = pd.DataFrame()
        self.df_rh = pd.DataFrame()

        # Widgets de KPI
        self.kpi_lucro = None
        self.kpi_receita = None
        self.kpi_baixo = None
        self.kpi_valor_estoque = None
        self.kpi_total_clientes = None
        self.kpi_total_funcionarios = None

        # Canvas do gráfico
        self.canvas_revexp = None
        self.chart_holder_layout = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Visão Geral do Negócio")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #6A0DAD;")

        export_button = QPushButton("📄 Gerar Relatório")
        export_button.setObjectName("ActionButton")
        export_button.clicked.connect(self.export_full_report)
        export_button.setFixedWidth(220)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(export_button)
        main_layout.addLayout(header_layout)

        # KPIs
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)

        self.kpi_lucro = KPIWidget("Lucro Líquido")
        self.kpi_receita = KPIWidget("Receita Total", value_color="#2E8B57")
        self.kpi_baixo = KPIWidget("Itens com Estoque Baixo", value_color="#C21807")
        self.kpi_valor_estoque = KPIWidget("Valor do Estoque")
        self.kpi_total_clientes = KPIWidget("Total de Clientes")
        self.kpi_total_funcionarios = KPIWidget("Total de Funcionários")

        kpi_grid.addWidget(self.kpi_lucro, 0, 0)
        kpi_grid.addWidget(self.kpi_receita, 0, 1)
        kpi_grid.addWidget(self.kpi_total_clientes, 0, 2)
        kpi_grid.addWidget(self.kpi_baixo, 1, 0)
        kpi_grid.addWidget(self.kpi_valor_estoque, 1, 1)
        kpi_grid.addWidget(self.kpi_total_funcionarios, 1, 2)

        main_layout.addLayout(kpi_grid)

        # Área do gráfico
        chart_holder = QFrame()
        self.chart_holder_layout = QVBoxLayout(chart_holder)
        self.chart_holder_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(chart_holder)
        main_layout.addStretch()

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")
        self.df_estoque = self.data_handler.load_table("Estoque")
        self.df_clientes = self.data_handler.load_table("Publico_Alvo")
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        financial_data = calculate_financial_summary(self.df_financas)
        self.kpi_lucro.setValue(fmt_currency(financial_data.get('lucro', 0.0)))
        self.kpi_receita.setValue(fmt_currency(financial_data.get('receita', 0.0)))

        inventory_data = analyze_inventory_kpis(self.df_estoque)
        self.kpi_baixo.setValue(str(inventory_data.get('low_stock_count', 0)))
        self.kpi_valor_estoque.setValue(fmt_currency(inventory_data.get('total_value', 0.0)))

        total_clientes = len(self.df_clientes) if isinstance(self.df_clientes, pd.DataFrame) else 0
        total_funcionarios = len(self.df_rh) if isinstance(self.df_rh, pd.DataFrame) else 0
        self.kpi_total_clientes.setValue(str(total_clientes))
        self.kpi_total_funcionarios.setValue(str(total_funcionarios))

    def _rebuild_charts(self):
        if self.canvas_revexp is not None:
            self.chart_holder_layout.removeWidget(self.canvas_revexp)
            self.canvas_revexp.setParent(None)
            self.canvas_revexp = None

        df = self.df_financas.copy() if isinstance(self.df_financas, pd.DataFrame) else pd.DataFrame()

        # Agrega receita/despesa
        receita, despesa = 0.0, 0.0
        if {"Tipo", "Valor"}.issubset(df.columns):
            df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0)
            tipo = df["Tipo"].astype(str).str.lower()
            receita = df.loc[tipo.eq("receita"), "Valor"].sum()
            despesa = df.loc[tipo.eq("despesa"), "Valor"].sum()

        # Cores fixas para o tema claro
        text_color = 'black'
        bg_color = '#F0F0F0' # Cor de fundo do app

        # Figura
        fig = Figure(figsize=(5.8, 3.6), dpi=100, tight_layout=True)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        ax.bar(['Receita', 'Despesas'], [receita, despesa], color=['#2E8B57', '#C21807'])
        ax.set_title('Resumo Financeiro do Período', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.grid(axis='y', color='#999999', alpha=0.25)

        # Rótulos no topo das barras
        for x, v in enumerate([receita, despesa]):
            ax.text(x, v, fmt_currency(v), ha="center", va="bottom", fontsize=9, color=text_color)

        self.canvas_revexp = FigureCanvas(fig)
        self.chart_holder_layout.addWidget(self.canvas_revexp)

    def export_full_report(self):
        period = self.data_handler.get_period() if hasattr(self.data_handler, "get_period") else None
        start, end = (period[0], period[1]) if period and len(period) >= 2 else (None, None)

        suffix = f"_{start}_a_{end}" if (start and end) else ""
        default_name = f"Relatorio_Amazon_Fruit{suffix}.pdf"

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Relatório Completo", default_name, "PDF Files (*.pdf)"
        )
        if not file_path: return

        try:
            report = ReportGenerator(self.data_handler)
            report.generate_report(file_path)
            QMessageBox.information(self, "Sucesso", f"Relatório salvo em:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o relatório:\n{e}")