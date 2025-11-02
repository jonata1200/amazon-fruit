# modules/dashboards/dashboard_canais_venda.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.widgets.kpi_widget import KPIWidget
from modules.analysis.sales_channel_analysis import get_sales_channel_distribution

class DashboardCanaisVenda(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        self.df_publico = pd.DataFrame()
        self.kpi_total_canais = None
        self.canvas_channels = None
        self.layout_channels = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard de Canais de Venda")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)
        
        kpi_layout = QHBoxLayout()
        self.kpi_total_canais = KPIWidget("Canais de Origem Únicos")
        kpi_layout.addWidget(self.kpi_total_canais)
        kpi_layout.addStretch()
        root.addLayout(kpi_layout)

        chart_frame = QFrame()
        self.layout_channels = QVBoxLayout(chart_frame)
        self.layout_channels.setContentsMargins(0, 0, 0, 0)
        root.addWidget(chart_frame)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_publico = self.data_handler.load_table("Publico_Alvo")

    def _rebuild_kpis(self):
        channels = get_sales_channel_distribution(self.df_publico)
        self.kpi_total_canais.setValue(str(len(channels)))

    def _rebuild_charts(self):
        if self.canvas_channels is not None:
            self.layout_channels.removeWidget(self.canvas_channels)
            self.canvas_channels.setParent(None)

        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        channel_series = get_sales_channel_distribution(self.df_publico)
        if not channel_series.empty:
            channel_series.sort_values().plot(kind='barh', ax=ax, color='#FF8C00')
            ax.set_title("Distribuição de Clientes por Canal de Origem")
        
        fig.tight_layout()
        self.canvas_channels = FigureCanvas(fig)
        self.layout_channels.addWidget(self.canvas_channels)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()