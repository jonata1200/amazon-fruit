# modules/dashboards/dashboard_recursos_humanos.py

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
from modules.analysis.hr_analysis import analyze_hr_kpis

class DashboardRecursosHumanos(QWidget):
    """
    Dashboard de Recursos Humanos.
    - Utiliza a camada de análise para obter os dados calculados.
    - Focado apenas na apresentação dos dados.
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        self.df_rh = pd.DataFrame()
        self.kpi_total_funcionarios = None
        self.kpi_custo_mensal = None
        self.table_rh = None
        self.canvas_salary = None
        self.layout_salary = None

        self.build_ui()
        self.refresh()

    # ------------------------------------------------------------------
    # UI (Estrutura Estática)
    # ------------------------------------------------------------------
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard de Recursos Humanos")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)
        self.kpi_total_funcionarios = KPIWidget("Total de Funcionários")
        self.kpi_custo_mensal = KPIWidget("Custo Mensal da Equipe")
        kpi_layout.addWidget(self.kpi_total_funcionarios)
        kpi_layout.addWidget(self.kpi_custo_mensal)
        root.addLayout(kpi_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(16)
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_rh = QTableView()
        table_layout.addWidget(self.table_rh)
        bottom_layout.addWidget(table_frame, 1)

        chart_frame = QFrame()
        self.layout_salary = QVBoxLayout(chart_frame)
        self.layout_salary.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(chart_frame, 1)

        root.addLayout(bottom_layout)

    # ------------------------------------------------------------------
    # Ciclo de Atualização de Dados
    # ------------------------------------------------------------------
    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        """Usa a camada de análise para obter os KPIs e os exibe."""
        kpi_data = analyze_hr_kpis(self.df_rh)

        self.kpi_total_funcionarios.setValue(str(kpi_data['total_employees']))
        self.kpi_custo_mensal.setValue(fmt_currency(kpi_data['total_monthly_cost']))

    def _rebuild_tables(self):
        set_table_from_df(self.table_rh, self.df_rh)

    def _rebuild_charts(self):
        if self.canvas_salary is not None:
            self.layout_salary.removeWidget(self.canvas_salary)
            self.canvas_salary.setParent(None)
            self.canvas_salary = None

        df = self.df_rh

        fig = Figure(figsize=(6.2, 4), dpi=100)
        ax = fig.add_subplot(111)
        if not df.empty and {'Nome_Funcionario', 'Salario'}.issubset(df.columns):
            dfx = df.copy()
            dfx['Salario'] = pd.to_numeric(dfx['Salario'], errors='coerce')
            dfx = dfx.dropna(subset=['Salario']).sort_values('Salario', ascending=False).head(15)
            if not dfx.empty:
                ax.bar(dfx['Nome_Funcionario'].astype(str), dfx['Salario'], color='#4B0082')
                ax.tick_params(axis='x', rotation=45)
                for label in ax.get_xticklabels():
                    label.set_ha('right')

        ax.set_title("Salários por Funcionário (Top 15)")
        fig.tight_layout(pad=1.0)
        self.canvas_salary = FigureCanvas(fig)
        self.layout_salary.addWidget(self.canvas_salary)

    # ------------------------------------------------------------------
    # Tema
    # ------------------------------------------------------------------
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()