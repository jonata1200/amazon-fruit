from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget

# Camada de análise (ajuste os nomes se necessário)
from modules.analysis.public_analysis import (
    analyze_public_kpis,     # {'total_clients','avg_age','pct_feminino'}
    get_clients_by_location, # Series por Estado
    get_clients_by_gender    # Series por Gênero
)

class DashboardPublicoAlvo(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        self.df_publico = pd.DataFrame()
        self.kpi_total = None
        self.kpi_idade_media = None
        self.kpi_pct_fem = None
        self.table_publico = None
        self.canvas_location = None
        self.canvas_gender = None
        self.layout_location = None
        self.layout_gender = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Dashboard de Público-Alvo"); title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Clientes")
        self.kpi_idade_media = KPIWidget("Idade Média")
        self.kpi_pct_fem = KPIWidget("% Feminino")
        kpi_layout.addWidget(self.kpi_total); kpi_layout.addWidget(self.kpi_idade_media); kpi_layout.addWidget(self.kpi_pct_fem)
        root.addLayout(kpi_layout)

        table_frame = QFrame(); table_layout = QVBoxLayout(table_frame); table_layout.setContentsMargins(0,0,0,0)
        self.table_publico = QTableView(); table_layout.addWidget(self.table_publico); root.addWidget(table_frame)

        charts_row = QHBoxLayout(); charts_row.setSpacing(16)
        chart1 = QFrame(); self.layout_location = QVBoxLayout(chart1); self.layout_location.setContentsMargins(0,0,0,0)
        chart2 = QFrame(); self.layout_gender   = QVBoxLayout(chart2); self.layout_gender.setContentsMargins(0,0,0,0)
        charts_row.addWidget(chart1); charts_row.addWidget(chart2); root.addLayout(charts_row)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()

    def _reload_data(self):
        self.df_publico = self.data_handler.load_table("Publico_Alvo")

    def _rebuild_kpis(self):
        k = analyze_public_kpis(self.df_publico)
        self.kpi_total.setValue(str(k.get('total_clients', 0)))
        self.kpi_idade_media.setValue(f"{k.get('avg_age', 0):.1f}")
        self.kpi_pct_fem.setValue(f"{k.get('pct_feminino', 0):.1f}%")

    def _rebuild_tables(self):
        df = self.df_publico.copy()

        # 1) Ocultar colunas indesejadas
        drop_cols = [c for c in ["ID_Cliente", "Ano", "Mes"] if c in df.columns]
        if drop_cols:
            df = df.drop(columns=drop_cols)

        # 2) Reordenar colunas
        ordem = [c for c in [
            "Nome", "Idade", "Genero", "Estado", "Cidade", "Canal_de_venda"
        ] if c in df.columns]
        outras = [c for c in df.columns if c not in ordem]
        if ordem:
            df = df[ordem + outras]

        # 3) Corrigir cabeçalhos (nomes PT-BR)
        rename_map = {
            "Nome": "Nome",
            "Idade": "Idade",
            "Genero": "Gênero",
            "Estado": "Estado",
            "Cidade": "Cidade",
            "Canal_de_venda": "Canal de Venda",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        set_table_from_df(self.table_publico, df)

    def _rebuild_charts(self):
        if self.canvas_location: self.layout_location.removeWidget(self.canvas_location); self.canvas_location.setParent(None)
        if self.canvas_gender:   self.layout_gender.removeWidget(self.canvas_gender);     self.canvas_gender.setParent(None)

        # Barras por Estado
        fig1 = Figure(figsize=(6, 3.8), dpi=100); ax1 = fig1.add_subplot(111)
        ser_loc = get_clients_by_location(self.df_publico)
        if not ser_loc.empty:
            ax1.bar(ser_loc.index, ser_loc.values); ax1.tick_params(axis='x', rotation=25)
        ax1.set_title("Clientes por Estado"); fig1.tight_layout()
        self.canvas_location = FigureCanvas(fig1); self.layout_location.addWidget(self.canvas_location)

        # Pizza por Gênero
        fig2 = Figure(figsize=(5, 3.8), dpi=100); ax2 = fig2.add_subplot(111)
        ser_gen = get_clients_by_gender(self.df_publico)
        if not ser_gen.empty:
            ax2.pie(ser_gen.values, labels=ser_gen.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Distribuição por Gênero"); fig2.tight_layout()
        self.canvas_gender = FigureCanvas(fig2); self.layout_gender.addWidget(self.canvas_gender)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()