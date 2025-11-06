# modules/dashboards/dashboard_recursos_humanos.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QTabWidget, QGridLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import matplotlib.pyplot as plt

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
# Importa as novas funções de análise
from modules.analysis.hr_analysis import (
    analyze_hr_kpis,
    get_headcount_by_department,
    get_cost_by_department,
    get_headcount_by_role,
    get_hiring_over_time
)

class DashboardRecursosHumanos(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_rh = pd.DataFrame()

        self.kpi_total_funcionarios = None; self.kpi_custo_mensal = None
        self.table_rh = None
        
        # Canvases e layouts para todos os gráficos
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

        # --- NOVA ESTRUTURA DE ABAS (GRÁFICOS PRIMEIRO) ---

        # Aba 1: Análise Departamental (2 gráficos)
        dept_analysis_widget = QWidget()
        dept_analysis_layout = QGridLayout(dept_analysis_widget)
        dept_analysis_layout.addLayout(self.layout_headcount, 0, 0)
        dept_analysis_layout.addLayout(self.layout_cost, 0, 1)
        main_tab_widget.addTab(dept_analysis_widget, "📊 Análise Departamental")

        # Aba 2: Análise Estrutural
        role_widget = QWidget(); role_widget.setLayout(self.layout_role)
        main_tab_widget.addTab(role_widget, "🔺 Análise Estrutural")

        # Aba 3: Análise de Contratações
        hiring_widget = QWidget(); hiring_widget.setLayout(self.layout_hiring)
        main_tab_widget.addTab(hiring_widget, "📈 Histórico de Contratações")

        # Aba 4: Tabela de Funcionários
        self.table_rh = QTableView()
        main_tab_widget.addTab(self.table_rh, "👥 Lista de Funcionários")
        
        root.addWidget(main_tab_widget)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()

    def _reload_data(self):
        # Apenas os dados de RH do período selecionado são necessários
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        # Usamos df_rh, que pode ser o DataFrame completo ou filtrado,
        # para que os KPIs reflitam o período selecionado.
        k = analyze_hr_kpis(self.data_handler.load_table("Recursos_Humanos"))
        self.kpi_total_funcionarios.setValue(str(k.get('total_employees',0)))
        self.kpi_custo_mensal.setValue(fmt_currency(k.get('total_monthly_cost',0.0)))
        
    def _rebuild_tables(self):
        # ... (código deste método permanece o mesmo) ...
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
        # Limpa todos os canvases
        if self.canvas_headcount: self.layout_headcount.removeWidget(self.canvas_headcount); self.canvas_headcount.deleteLater(); self.canvas_headcount = None
        if self.canvas_cost: self.layout_cost.removeWidget(self.canvas_cost); self.canvas_cost.deleteLater(); self.canvas_cost = None
        if self.canvas_role: self.layout_role.removeWidget(self.canvas_role); self.canvas_role.deleteLater(); self.canvas_role = None
        if self.canvas_hiring: self.layout_hiring.removeWidget(self.canvas_hiring); self.canvas_hiring.deleteLater(); self.canvas_hiring = None

        text_color = 'black'; bg_color = '#FFFFFF'

        # --- Geração dos 4 Gráficos ---

        # Gráfico 1: Headcount por Departamento
        fig1 = Figure(tight_layout=True); fig1.patch.set_facecolor(bg_color); ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        headcount = get_headcount_by_department(self.df_rh)
        if not headcount.empty: headcount.sort_values().plot(kind='barh', ax=ax1, color='#6A0DAD')
        ax1.set_title("Nº de Funcionários por Depto.", color=text_color)
        self.canvas_headcount = FigureCanvas(fig1); self.layout_headcount.addWidget(self.canvas_headcount)
        
        # Gráfico 2: Custo por Departamento
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color); ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        cost = get_cost_by_department(self.df_rh)
        if not cost.empty: cost.plot(kind='barh', ax=ax2, color='#3498DB')
        ax2.set_title("Custo Mensal por Depto.", color=text_color)
        self.canvas_cost = FigureCanvas(fig2); self.layout_cost.addWidget(self.canvas_cost)
        
        # Gráfico 3: Distribuição por Cargo
        fig3 = Figure(tight_layout=True); fig3.patch.set_facecolor(bg_color); ax3 = fig3.add_subplot(111); ax3.set_facecolor(bg_color)
        roles = get_headcount_by_role(self.df_rh)
        if not roles.empty: roles.sort_values().plot(kind='barh', ax=ax3, color='#2ECC71')
        ax3.set_title("Top 10 Cargos na Empresa", color=text_color)
        self.canvas_role = FigureCanvas(fig3); self.layout_role.addWidget(self.canvas_role)
        
        # Gráfico 4: Histórico de Contratações
        fig4 = Figure(tight_layout=True); fig4.patch.set_facecolor(bg_color); ax4 = fig4.add_subplot(111); ax4.set_facecolor(bg_color)
        hiring = get_hiring_over_time(self.df_rh)
        if not hiring.empty: hiring.plot(kind='line', ax=ax4, marker='o', color='#E67E22')
        ax4.set_title("Contratações ao Longo do Tempo", color=text_color)
        ax4.tick_params(axis='x', rotation=45, labelsize=8)
        self.canvas_hiring = FigureCanvas(fig4); self.layout_hiring.addWidget(self.canvas_hiring)