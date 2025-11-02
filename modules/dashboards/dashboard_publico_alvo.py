# modules/dashboards/dashboard_publico_alvo.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableView
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

# --- NOVAS IMPORTAÇÕES CENTRALIZADAS ---
from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_age, fmt_currency


class DashboardPublicoAlvo(QWidget):
    """
    Dashboard de Público-Alvo.
    - Utiliza componentes reutilizáveis (KPIWidget) e formatadores centralizados.
    - Segue o ciclo de vida padronizado (build_ui + refresh).
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # Data
        self.df_publico = pd.DataFrame()

        # Widgets
        self.kpi_total = None
        self.kpi_idade_media = None
        self.kpi_gasto_medio = None
        self.table_publico = None
        self.canvas_location = None
        self.canvas_gender = None

        # Layouts para os gráficos (holders)
        self.layout_location = None
        self.layout_gender = None

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

        title = QLabel("Dashboard de Público-Alvo")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # ===== KPIs (Agora usando KPIWidget) =====
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)

        self.kpi_total = KPIWidget("Total de Clientes")
        self.kpi_idade_media = KPIWidget("Idade Média")
        self.kpi_gasto_medio = KPIWidget("Gasto Médio por Cliente")

        kpi_layout.addWidget(self.kpi_total)
        kpi_layout.addWidget(self.kpi_idade_media)
        kpi_layout.addWidget(self.kpi_gasto_medio)
        root.addLayout(kpi_layout)

        # ===== Tabela =====
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_publico = QTableView()
        table_layout.addWidget(self.table_publico)
        root.addWidget(table_frame)

        # ===== Gráficos (Containers) =====
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        chart1_frame = QFrame()
        self.layout_location = QVBoxLayout(chart1_frame)
        self.layout_location.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart1_frame)

        chart2_frame = QFrame()
        self.layout_gender = QVBoxLayout(chart2_frame)
        self.layout_gender.setContentsMargins(0, 0, 0, 0)
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
        self.df_publico = self.data_handler.load_table("Publico_Alvo")

    def _rebuild_kpis(self):
        df = self.df_publico if self.df_publico is not None else pd.DataFrame()

        total = len(df)
        idade_media = float('nan')
        gasto_medio = float('nan')

        if not df.empty:
            if 'Idade' in df.columns:
                idade_media = pd.to_numeric(df['Idade'], errors='coerce').mean()
            
            gasto_col = 'Gasto_Medio' if 'Gasto_Medio' in df.columns else 'Ticket_Medio'
            if gasto_col in df.columns:
                gasto_medio = pd.to_numeric(df[gasto_col], errors='coerce').mean()

        # --- ATUALIZAÇÃO USANDO O MÉTODO .setValue() DO KPIWIDGET ---
        self.kpi_total.setValue(str(total))
        self.kpi_idade_media.setValue(fmt_age(idade_media))
        self.kpi_gasto_medio.setValue(fmt_currency(gasto_medio))

    def _rebuild_tables(self):
        set_table_from_df(self.table_publico, self.df_publico)

    def _rebuild_charts(self):
        if self.canvas_location is not None:
            self.layout_location.removeWidget(self.canvas_location)
            self.canvas_location.setParent(None)
        if self.canvas_gender is not None:
            self.layout_gender.removeWidget(self.canvas_gender)
            self.canvas_gender.setParent(None)

        df = self.df_publico

        # Gráfico 1: Localização
        fig1 = Figure(figsize=(6, 3.8), dpi=100)
        ax1 = fig1.add_subplot(111)
        if not df.empty and 'Localizacao' in df.columns:
            s = df['Localizacao'].astype(str).value_counts().head(10)
            if not s.empty:
                ax1.bar(s.index, s.values, color='#4B0082')
                ax1.tick_params(axis='x', rotation=25)
        ax1.set_title("Distribuição de Clientes por Localização")
        fig1.tight_layout()
        self.canvas_location = FigureCanvas(fig1)
        self.layout_location.addWidget(self.canvas_location)

        # Gráfico 2: Gênero
        fig2 = Figure(figsize=(5, 3.8), dpi=100)
        ax2 = fig2.add_subplot(111)
        if not df.empty and 'Genero' in df.columns:
            s = df['Genero'].astype(str).value_counts()
            if not s.empty:
                ax2.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Distribuição por Gênero")
        fig2.tight_layout()
        self.canvas_gender = FigureCanvas(fig2)
        self.layout_gender.addWidget(self.canvas_gender)

    # ------------------------------------------------------------------
    # Tema
    # ------------------------------------------------------------------
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()