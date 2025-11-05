# modules/dashboards/dashboard_recursos_humanos.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QTableView, QTabWidget # QTabWidget importado para a nova estrutura
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from modules.analysis.hr_analysis import analyze_hr_kpis

class DashboardRecursosHumanos(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_rh = pd.DataFrame()

        # Widgets da UI
        self.kpi_total_funcionarios = None
        self.kpi_custo_mensal = None
        self.table_rh = None
        self.canvas_dept = None
        self.layout_dept = QVBoxLayout() # O layout do gráfico agora é um atributo da classe

        self.build_ui()
        self.refresh()

    def build_ui(self):
        """
        --- MUDANÇA PRINCIPAL: Reestruturação da UI com QTabWidget ---
        """
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard de Recursos Humanos")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # KPIs no topo, fora das abas
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)
        self.kpi_total_funcionarios = KPIWidget("Total de Funcionários")
        self.kpi_custo_mensal = KPIWidget("Custo Mensal da Equipe")
        kpi_layout.addWidget(self.kpi_total_funcionarios)
        kpi_layout.addWidget(self.kpi_custo_mensal)
        root.addLayout(kpi_layout)

        # 1. Cria o widget de abas
        main_tab_widget = QTabWidget()

        # 2. Cria a Aba 1: Tabela de Funcionários
        self.table_rh = QTableView()
        main_tab_widget.addTab(self.table_rh, "👥 Lista de Funcionários")

        # 3. Cria a Aba 2: Gráfico por Departamento
        chart_widget = QWidget()
        chart_widget.setLayout(self.layout_dept) # Aplica o layout do gráfico a este widget
        main_tab_widget.addTab(chart_widget, "📊 Funcionários por Departamento")
        
        # 4. Adiciona o widget de abas ao layout principal
        root.addWidget(main_tab_widget)

    # Nenhuma mudança necessária nos métodos abaixo
    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        k = analyze_hr_kpis(self.df_rh)
        self.kpi_total_funcionarios.setValue(str(k.get('total_employees', 0)))
        self.kpi_custo_mensal.setValue(fmt_currency(k.get('total_monthly_cost', 0.0)))

    def _rebuild_tables(self):
        df = self.df_rh.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_rh, pd.DataFrame())
            return
            
        if "Data_Contratacao" in df.columns:
            df["Data_Contratacao"] = pd.to_datetime(df["Data_Contratacao"], errors="coerce").dt.strftime("%d/%m/%Y")
        
        if "Salario" in df.columns:
            df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce").fillna(0.0).apply(fmt_currency)

        df = df.drop(columns=["ID_Funcionario"], errors='ignore')

        rename_map = { "Nome": "Nome", "Regime": "Regime", "Departamento": "Departamento", "Cargo": "Cargo", "Salario": "Salário", "Email": "E-mail", "Data_Contratacao": "Data de Contratação" }
        df = df.rename(columns=rename_map)
        
        cols_order = ["Nome", "Cargo", "Departamento", "Salário", "Data de Contratação", "E-mail"]
        existing_cols = [col for col in cols_order if col in df.columns]

        set_table_from_df(self.table_rh, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_dept:
            self.layout_dept.removeWidget(self.canvas_dept)
            self.canvas_dept.deleteLater()
            self.canvas_dept = None

        text_color = 'black'
        bg_color = '#FFFFFF'

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        
        df = self.df_rh
        if not df.empty and 'Departamento' in df.columns:
            dept_counts = df['Departamento'].value_counts().sort_values()
            if not dept_counts.empty:
                dept_counts.plot(kind='barh', ax=ax, color='#6A0DAD')

        ax.set_title("Funcionários por Departamento", color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        fig.tight_layout(pad=1.0)
        self.canvas_dept = FigureCanvas(fig)
        self.layout_dept.addWidget(self.canvas_dept)