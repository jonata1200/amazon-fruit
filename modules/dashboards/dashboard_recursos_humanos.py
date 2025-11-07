# modules/dashboards/dashboard_recursos_humanos.py

import pandas as pd
import matplotlib.pyplot as plt  # <-- MUDANÇA AQUI

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QTabWidget, QGridLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from modules.analysis.hr_analysis import analyze_hr_kpis
from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from .chart_generator import (
    create_hr_headcount_chart,
    create_hr_cost_chart,
    create_hr_role_chart,
    create_hr_hiring_chart
)

class DashboardRecursosHumanos(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_rh = pd.DataFrame()

        self.kpi_total_funcionarios = None; self.kpi_custo_mensal = None
        self.table_rh = None
        
        self.canvas_headcount = None; self.layout_headcount = QVBoxLayout()
        self.canvas_cost = None; self.layout_cost = QVBoxLayout()
        self.canvas_role = None; self.layout_role = QVBoxLayout()
        self.canvas_hiring = None; self.layout_hiring = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20, 20, 20, 20); root.setSpacing(16)
        title = QLabel("Dashboard de Recursos Humanos"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)
        
        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(16)
        self.kpi_total_funcionarios = KPIWidget("Total de Funcionários"); self.kpi_custo_mensal = KPIWidget("Custo Mensal da Equipe")
        kpi_layout.addWidget(self.kpi_total_funcionarios); kpi_layout.addWidget(self.kpi_custo_mensal)
        root.addLayout(kpi_layout)

        main_tab_widget = QTabWidget()

        dept_analysis_widget = QWidget()
        dept_analysis_layout = QGridLayout(dept_analysis_widget)
        dept_analysis_layout.addLayout(self.layout_headcount, 0, 0)
        dept_analysis_layout.addLayout(self.layout_cost, 0, 1)
        main_tab_widget.addTab(dept_analysis_widget, "📊 Análise Departamental")

        role_widget = QWidget(); role_widget.setLayout(self.layout_role)
        main_tab_widget.addTab(role_widget, "🔺 Análise Estrutural")

        hiring_widget = QWidget(); hiring_widget.setLayout(self.layout_hiring)
        main_tab_widget.addTab(hiring_widget, "📈 Histórico de Contratações")

        self.table_rh = QTableView()
        main_tab_widget.addTab(self.table_rh, "👥 Lista de Funcionários")
        
        root.addWidget(main_tab_widget)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()

    def _reload_data(self):
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        k = analyze_hr_kpis(self.data_handler.load_table("Recursos_Humanos"))
        self.kpi_total_funcionarios.setValue(str(k.get('total_employees',0)))
        self.kpi_custo_mensal.setValue(fmt_currency(k.get('total_monthly_cost',0.0)))
        
    def _rebuild_tables(self):
        df = self.df_rh.copy()
        if df is None or df.empty: set_table_from_df(self.table_rh, pd.DataFrame()); return
        if "Data_Contratacao" in df.columns: df["Data_Contratacao"] = pd.to_datetime(df["Data_Contratacao"], errors="coerce").dt.strftime("%d/%m/%Y")
        if "Salario" in df.columns: df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce").fillna(0.0).apply(fmt_currency)
        df = df.drop(columns=["ID_Funcionario"], errors='ignore')
        rename_map = {"Nome": "Nome", "Regime": "Regime", "Departamento": "Departamento", "Cargo": "Cargo", "Salario": "Salário", "Email": "E-mail", "Data_Contratacao": "Data de Contratação"}
        df = df.rename(columns=rename_map)
        cols_order = ["Nome", "Cargo", "Departamento", "Salário", "Data de Contratação", "E-mail"]; existing_cols = [col for col in cols_order if col in df.columns]
        set_table_from_df(self.table_rh, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_headcount: self.layout_headcount.removeWidget(self.canvas_headcount); self.canvas_headcount.deleteLater(); self.canvas_headcount = None
        if self.canvas_cost: self.layout_cost.removeWidget(self.canvas_cost); self.canvas_cost.deleteLater(); self.canvas_cost = None
        if self.canvas_role: self.layout_role.removeWidget(self.canvas_role); self.canvas_role.deleteLater(); self.canvas_role = None
        if self.canvas_hiring: self.layout_hiring.removeWidget(self.canvas_hiring); self.canvas_hiring.deleteLater(); self.canvas_hiring = None

        # Gráfico 1: Headcount por Departamento
        fig1 = create_hr_headcount_chart(self.df_rh)
        self.canvas_headcount = FigureCanvas(fig1)
        self.layout_headcount.addWidget(self.canvas_headcount)
        plt.close(fig1)  # <-- MUDANÇA AQUI
        
        # Gráfico 2: Custo por Departamento
        fig2 = create_hr_cost_chart(self.df_rh)
        self.canvas_cost = FigureCanvas(fig2)
        self.layout_cost.addWidget(self.canvas_cost)
        plt.close(fig2)  # <-- MUDANÇA AQUI
        
        # Gráfico 3: Distribuição por Cargo
        fig3 = create_hr_role_chart(self.df_rh)
        self.canvas_role = FigureCanvas(fig3)
        self.layout_role.addWidget(self.canvas_role)
        plt.close(fig3)  # <-- MUDANÇA AQUI
        
        # Gráfico 4: Histórico de Contratações
        fig4 = create_hr_hiring_chart(self.df_rh)
        self.canvas_hiring = FigureCanvas(fig4)
        self.layout_hiring.addWidget(self.canvas_hiring)
        plt.close(fig4)  # <-- MUDANÇA AQUI