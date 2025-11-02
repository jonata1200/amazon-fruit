# modules/dashboards/dashboard_fornecedores.py

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
from modules.utils.formatters import fmt_rating
# --- NOVA IMPORTAÇÃO DA CAMADA DE ANÁLISE ---
from modules.analysis.suppliers_analysis import analyze_suppliers_kpis, get_product_types_distribution

class DashboardFornecedores(QWidget):
    """
    Dashboard de Fornecedores.
    - Utiliza a camada de análise para obter os dados calculados.
    - Focado apenas na apresentação dos dados.
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # Data
        self.df_fornecedores = pd.DataFrame()

        # Widgets
        self.kpi_total = None
        self.kpi_avaliacao_media = None
        self.table_fornecedores = None
        self.canvas_rating = None
        self.canvas_types = None

        # Layouts para os gráficos (holders)
        self.layout_rating = None
        self.layout_types = None

        self.build_ui()
        self.refresh()

    # ------------------------------------------------------------------
    # UI (Estrutura Estática)
    # ------------------------------------------------------------------
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard de Fornecedores")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Fornecedores")
        self.kpi_avaliacao_media = KPIWidget("Avaliação Média")
        kpi_layout.addWidget(self.kpi_total)
        kpi_layout.addWidget(self.kpi_avaliacao_media)
        root.addLayout(kpi_layout)

        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_fornecedores = QTableView()
        table_layout.addWidget(self.table_fornecedores)
        root.addWidget(table_frame)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)
        chart1_frame = QFrame()
        self.layout_rating = QVBoxLayout(chart1_frame)
        self.layout_rating.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart1_frame)
        chart2_frame = QFrame()
        self.layout_types = QVBoxLayout(chart2_frame)
        self.layout_types.setContentsMargins(0, 0, 0, 0)
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
        self.df_fornecedores = self.data_handler.load_table("Fornecedores")

    def _rebuild_kpis(self):
        """Usa a camada de análise para obter os KPIs e os exibe."""
        kpi_data = analyze_suppliers_kpis(self.df_fornecedores)
        
        self.kpi_total.setValue(str(kpi_data['total_suppliers']))
        self.kpi_avaliacao_media.setValue(fmt_rating(kpi_data['avg_rating']))

    def _rebuild_tables(self):
        set_table_from_df(self.table_fornecedores, self.df_fornecedores)

    def _rebuild_charts(self):
        if self.canvas_rating is not None:
            self.layout_rating.removeWidget(self.canvas_rating)
            self.canvas_rating.setParent(None)
        if self.canvas_types is not None:
            self.layout_types.removeWidget(self.canvas_types)
            self.canvas_types.setParent(None)

        df = self.df_fornecedores

        # Gráfico 1: Avaliação (Lógica de apresentação permanece aqui)
        fig1 = Figure(figsize=(6.2, 3.8), dpi=100)
        ax1 = fig1.add_subplot(111)
        if not df.empty and {'Nome_Fornecedor', 'Avaliacao'}.issubset(df.columns):
            dfx = df.copy()
            dfx['Avaliacao'] = pd.to_numeric(dfx['Avaliacao'], errors='coerce')
            dfx = dfx.dropna(subset=['Avaliacao']).sort_values('Avaliacao', ascending=True).tail(10)
            if not dfx.empty:
                ax1.barh(dfx['Nome_Fornecedor'].astype(str), dfx['Avaliacao'], color='#2E8B57')
                ax1.set_xlim(0, 5)
        ax1.set_title("Avaliação dos Fornecedores (Top 10)")
        fig1.tight_layout()
        self.canvas_rating = FigureCanvas(fig1)
        self.layout_rating.addWidget(self.canvas_rating)

        # Gráfico 2: Tipos de produtos (Usa a camada de análise)
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        product_types_series = get_product_types_distribution(df)
        if not product_types_series.empty:
            ax2.pie(product_types_series.values, labels=product_types_series.index, autopct='%1.1f%%', startangle=90)
            
        ax2.set_title("Tipos de Produtos Fornecidos")
        fig2.tight_layout()
        self.canvas_types = FigureCanvas(fig2)
        self.layout_types.addWidget(self.canvas_types)

    # ------------------------------------------------------------------
    # Tema
    # ------------------------------------------------------------------
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()