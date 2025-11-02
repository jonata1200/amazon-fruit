# modules/dashboards/dashboard_recursos_humanos.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableView
)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df


class DashboardRecursosHumanos(QWidget):
    """
    Dashboard de Recursos Humanos.
    - KPIs + Tabela + Gráfico de Salários
    - Segue o ciclo de vida padronizado (build_ui + refresh).
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # Data
        self.df_rh = pd.DataFrame()

        # Widgets
        self.kpi_total_funcionarios = None
        self.kpi_custo_mensal = None
        self.table_rh = None
        self.canvas_salary = None

        # Layout para o gráfico (holder)
        self.layout_salary = None

        # Inicia o ciclo de vida
        self.build_ui()
        self.refresh()

    # ------------------------------------------------------------------
    # UI (Criação da Estrutura Estática)
    # ------------------------------------------------------------------
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # Título
        title = QLabel("Dashboard de Recursos Humanos")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # ===== KPIs =====
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)

        self.kpi_total_funcionarios = self._create_kpi_box("Total de Funcionários")
        self.kpi_custo_mensal = self._create_kpi_box("Custo Mensal da Equipe")

        kpi_layout.addWidget(self.kpi_total_funcionarios)
        kpi_layout.addWidget(self.kpi_custo_mensal)
        root.addLayout(kpi_layout)

        # ===== Conteúdo Principal (Tabela e Gráfico) =====
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(16)

        # Tabela
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_rh = QTableView()
        table_layout.addWidget(self.table_rh)
        bottom_layout.addWidget(table_frame, 1) # Proporção 1

        # Gráfico (Container)
        chart_frame = QFrame()
        self.layout_salary = QVBoxLayout(chart_frame)
        self.layout_salary.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(chart_frame, 1) # Proporção 1

        root.addLayout(bottom_layout)

    # ------------------------------------------------------------------
    # Ciclo de Atualização de Dados
    # ------------------------------------------------------------------
    def refresh(self):
        """Orquestra a atualização completa do dashboard."""
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        """Carrega/recarrega os dados do DataHandler."""
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        """Calcula e atualiza os valores dos cards de KPI."""
        df = self.df_rh if self.df_rh is not None else pd.DataFrame()

        total = len(df)
        custo_mensal = 0.0
        if not df.empty and 'Salario' in df.columns:
            custo_mensal = pd.to_numeric(df['Salario'], errors='coerce').fillna(0.0).sum()

        self._set_kpi_value(self.kpi_total_funcionarios, str(total))
        self._set_kpi_value(self.kpi_custo_mensal, self._fmt_currency(custo_mensal))

    def _rebuild_tables(self):
        """Atualiza a tabela com os novos dados."""
        set_table_from_df(self.table_rh, self.df_rh)

    def _rebuild_charts(self):
        """Remove o gráfico antigo e desenha o novo."""
        if self.canvas_salary is not None:
            self.layout_salary.removeWidget(self.canvas_salary)
            self.canvas_salary.setParent(None)
            self.canvas_salary = None

        df = self.df_rh

        # --- Gráfico: Salários por funcionário ---
        fig = Figure(figsize=(6.2, 4), dpi=100)
        ax = fig.add_subplot(111)
        if not df.empty and {'Nome_Funcionario', 'Salario'}.issubset(df.columns):
            dfx = df.copy()
            dfx['Salario'] = pd.to_numeric(dfx['Salario'], errors='coerce')
            dfx = dfx.dropna(subset=['Salario']).sort_values('Salario', ascending=False).head(15)
            if not dfx.empty:
                ax.bar(dfx['Nome_Funcionario'].astype(str), dfx['Salario'], color='#4B0082')
                
                # --- CORREÇÃO APLICADA AQUI ---
                # 1. Rotaciona os labels usando tick_params (sem o 'ha')
                ax.tick_params(axis='x', rotation=45)
                
                # 2. Ajusta o alinhamento horizontal dos labels separadamente
                for label in ax.get_xticklabels():
                    label.set_ha('right')
                # --- FIM DA CORREÇÃO ---

        ax.set_title("Salários por Funcionário (Top 15)")
        # Usamos tight_layout(pad=...) para dar um pouco mais de espaço para os labels
        fig.tight_layout(pad=1.0) 
        self.canvas_salary = FigureCanvas(fig)
        self.layout_salary.addWidget(self.canvas_salary)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _create_kpi_box(self, title, value_color=None):
        box = QFrame()
        box.setObjectName("KPIFrame")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(12, 10, 12, 10)

        t = QLabel(title)
        t.setObjectName("KPITitleLabel")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)

        v = QLabel("—")
        v.setObjectName("KPIValueLabel")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if value_color:
            v.setStyleSheet(f"color: {value_color};")

        lay.addWidget(t)
        lay.addWidget(v)
        box._value_label = v
        return box

    def _set_kpi_value(self, kpi_frame: QFrame, text: str):
        if kpi_frame and hasattr(kpi_frame, "_value_label"):
            kpi_frame._value_label.setText(text)

    @staticmethod
    def _fmt_currency(v):
        try:
            return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (Exception,):
            return "R$ 0,00"

    # ------------------------------------------------------------------
    # Tema
    # ------------------------------------------------------------------
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()