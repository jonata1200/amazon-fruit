from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from modules.analysis.hr_analysis import analyze_hr_kpis  # {'total_employees','total_monthly_cost'}

class DashboardRecursosHumanos(QWidget):
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

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Dashboard de Recursos Humanos"); title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(16)
        self.kpi_total_funcionarios = KPIWidget("Total de Funcionários")
        self.kpi_custo_mensal = KPIWidget("Custo Mensal da Equipe")
        kpi_layout.addWidget(self.kpi_total_funcionarios); kpi_layout.addWidget(self.kpi_custo_mensal)
        root.addLayout(kpi_layout)

        bottom = QHBoxLayout(); bottom.setSpacing(16)
        table_frame = QFrame(); table_layout = QVBoxLayout(table_frame); table_layout.setContentsMargins(0,0,0,0)
        self.table_rh = QTableView(); table_layout.addWidget(self.table_rh); bottom.addWidget(table_frame, 1)

        chart_frame = QFrame(); self.layout_salary = QVBoxLayout(chart_frame); self.layout_salary.setContentsMargins(0,0,0,0)
        bottom.addWidget(chart_frame, 1)
        root.addLayout(bottom)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()

    def _reload_data(self):
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        k = analyze_hr_kpis(self.df_rh)
        self.kpi_total_funcionarios.setValue(str(k.get('total_employees',0)))
        self.kpi_custo_mensal.setValue(fmt_currency(k.get('total_monthly_cost',0.0)))

    def _rebuild_tables(self):
        df = self.df_rh.copy()

        # 1) Data_Contratacao -> DD/MM/AAAA (sem 00:00:00)
        if "Data_Contratacao" in df.columns:
            df["Data_Contratacao"] = (
                pd.to_datetime(df["Data_Contratacao"], errors="coerce")
                .dt.strftime("%d/%m/%Y")
            )

        # 2) Ocultar colunas indesejadas
        drop_cols = [c for c in ["ID_Funcionario"] if c in df.columns]  # mantém Data_Contratacao formatada
        if drop_cols:
            df = df.drop(columns=drop_cols)

        # 3) Reordenar colunas
        ordem = [c for c in [
            "Nome", "Regime", "Departamento", "Cargo",
            "Salario", "Telefone", "Data_Contratacao"
        ] if c in df.columns]
        outras = [c for c in df.columns if c not in ordem]
        if ordem:
            df = df[ordem + outras]

        # 4) Renomear cabeçalhos para PT-BR correto
        rename_map = {
            "Nome": "Nome",
            "Regime": "Regime",
            "Departamento": "Departamento",
            "Cargo": "Cargo",
            "Salario": "Salário",
            "Telefone": "Telefone",
            "Data_Contratacao": "Data de Contratação",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        set_table_from_df(self.table_rh, df)

    def _rebuild_charts(self):
        if self.canvas_salary:
            self.layout_salary.removeWidget(self.canvas_salary); self.canvas_salary.setParent(None); self.canvas_salary = None

        df = self.df_rh
        fig = Figure(figsize=(6.2, 4), dpi=100); ax = fig.add_subplot(111)
        if not df.empty and {'Nome','Salario'}.issubset(df.columns):
            dfx = df.copy(); dfx['Salario'] = pd.to_numeric(dfx['Salario'], errors='coerce')
            dfx = dfx.dropna(subset=['Salario']).sort_values('Salario', ascending=False).head(15)
            if not dfx.empty:
                ax.bar(dfx['Nome'].astype(str), dfx['Salario'])
                ax.tick_params(axis='x', rotation=45)
                for label in ax.get_xticklabels(): label.set_ha('right')
        ax.set_title("Salários por Funcionário (Top 15)"); fig.tight_layout(pad=1.0)
        self.canvas_salary = FigureCanvas(fig); self.layout_salary.addWidget(self.canvas_salary)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()