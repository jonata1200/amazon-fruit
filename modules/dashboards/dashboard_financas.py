# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableView
)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df


class DashboardFinancas(QWidget):
    """
    Dashboard Financeiro.
    - Respeita período global via DataHandler.load_table("Financas")
    - KPIs + Tabela + Gráficos (Receita vs. Despesa, Pizza de Despesas)
    - Segue o ciclo de vida padronizado (build_ui + refresh).
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # Data
        self.df_financas = pd.DataFrame()

        # Widgets (serão criados em build_ui)
        self.kpi_receita = None
        self.kpi_despesas = None
        self.kpi_lucro = None
        self.table_financas = None
        self.canvas_revexp = None
        self.canvas_pie = None

        # Layouts para os gráficos (holders)
        self.layout_revexp = None
        self.layout_pie = None

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
        title = QLabel("Dashboard Financeiro")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # ===== KPIs =====
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)

        self.kpi_receita = self._create_kpi_box("Receita Total", value_color="#2E8B57")
        self.kpi_despesas = self._create_kpi_box("Despesas Totais", value_color="#C21807")
        self.kpi_lucro = self._create_kpi_box("Lucro Líquido", value_color="#FF8C00")

        kpi_layout.addWidget(self.kpi_receita)
        kpi_layout.addWidget(self.kpi_despesas)
        kpi_layout.addWidget(self.kpi_lucro)
        root.addLayout(kpi_layout)

        # ===== Tabela =====
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_financas = QTableView()
        table_layout.addWidget(self.table_financas)
        root.addWidget(table_frame)

        # ===== Gráficos (Containers) =====
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        chart1_frame = QFrame()
        self.layout_revexp = QVBoxLayout(chart1_frame)
        self.layout_revexp.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart1_frame)

        chart2_frame = QFrame()
        self.layout_pie = QVBoxLayout(chart2_frame)
        self.layout_pie.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart2_frame)

        root.addLayout(charts_row)

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
        self.df_financas = self.data_handler.load_table("Financas")

    def _rebuild_kpis(self):
        """Calcula e atualiza os valores dos cards de KPI."""
        df = self.df_financas if self.df_financas is not None else pd.DataFrame()

        receita = despesa = 0.0
        if not df.empty and {'Valor', 'Tipo'}.issubset(df.columns):
            t = df['Tipo'].astype(str).str.lower()
            v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
            receita = float(v[t.str.contains('entrada', case=False)].sum())
            despesa = float(v[t.str.contains('saída', case=False)].sum())
        lucro = receita - despesa

        self._set_kpi_value(self.kpi_receita, self._fmt_currency(receita))
        self._set_kpi_value(self.kpi_despesas, self._fmt_currency(despesa))
        self._set_kpi_value(self.kpi_lucro, self._fmt_currency(lucro))

    def _rebuild_tables(self):
        """Atualiza a tabela com os novos dados."""
        set_table_from_df(self.table_financas, self.df_financas)

    def _rebuild_charts(self):
        """Remove os gráficos antigos e desenha os novos."""
        # Limpa canvas antigo (se existir)
        if self.canvas_revexp is not None:
            self.layout_revexp.removeWidget(self.canvas_revexp)
            self.canvas_revexp.setParent(None)
            self.canvas_revexp = None
        if self.canvas_pie is not None:
            self.layout_pie.removeWidget(self.canvas_pie)
            self.canvas_pie.setParent(None)
            self.canvas_pie = None

        df = self.df_financas
        
        # --- Gráfico 1: Receita vs. Despesa (barras) ---
        fig1 = Figure(figsize=(5.8, 3.8), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        receita = despesa = 0.0
        if not df.empty and {'Valor', 'Tipo'}.issubset(df.columns):
            t = df['Tipo'].astype(str).str.lower()
            v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
            receita = float(v[t.str.contains('entrada', case=False)].sum())
            despesa = float(v[t.str.contains('saída', case=False)].sum())
            
        ax1.bar(['Receita', 'Despesas'], [receita, despesa], color=['#2E8B57', '#C21807'])
        ax1.set_title("Receita vs. Despesas")
        fig1.tight_layout()
        self.canvas_revexp = FigureCanvas(fig1)
        self.layout_revexp.addWidget(self.canvas_revexp)

        # --- Gráfico 2: Pizza de despesas por categoria ---
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        if not df.empty and {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
            dd = df[df['Tipo'].astype(str).str.lower().str.contains('saída', case=False)]
            s = dd.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)
            if not s.empty:
                ax2.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
                
        ax2.set_title("Distribuição de Despesas")
        fig2.tight_layout()
        self.canvas_pie = FigureCanvas(fig2)
        self.layout_pie.addWidget(self.canvas_pie)

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
        # Apenas redesenha os gráficos, que podem ter cores dependentes do tema.
        # O resto da UI é atualizado pelo stylesheet global do app.
        self._rebuild_charts()