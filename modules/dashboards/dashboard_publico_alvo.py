# modules/dashboards/dashboard_publico_alvo.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_age
from modules.analysis.public_analysis import (
    analyze_public_kpis,
    get_clients_by_location,
    get_clients_by_gender
)

class DashboardPublicoAlvo(QWidget):
    def __init__(self, data_handler): # Argumento de tema removido
        super().__init__()
        self.data_handler = data_handler
        # self.theme_name removido

        self.df_publico = pd.DataFrame()
        self.kpi_total = None
        self.kpi_idade_media = None
        self.kpi_gasto_medio = None # Renomeado de pct_fem para algo mais relevante
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
        self.kpi_gasto_medio = KPIWidget("Gasto Médio por Cliente") # KPI atualizado
        kpi_layout.addWidget(self.kpi_total)
        kpi_layout.addWidget(self.kpi_idade_media)
        kpi_layout.addWidget(self.kpi_gasto_medio)
        root.addLayout(kpi_layout)

        table_frame = QFrame(); table_layout = QVBoxLayout(table_frame); table_layout.setContentsMargins(0,0,0,0)
        self.table_publico = QTableView(); table_layout.addWidget(self.table_publico); root.addWidget(table_frame)

        charts_row = QHBoxLayout(); charts_row.setSpacing(16)
        chart1 = QFrame(); self.layout_location = QVBoxLayout(chart1); self.layout_location.setContentsMargins(0,0,0,0)
        chart2 = QFrame(); self.layout_gender   = QVBoxLayout(chart2); self.layout_gender.setContentsMargins(0,0,0,0)
        charts_row.addWidget(chart1); charts_row.addWidget(chart2); root.addLayout(charts_row)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_publico = self.data_handler.load_table("Publico_Alvo")

    def _rebuild_kpis(self):
        k = analyze_public_kpis(self.df_publico)
        self.kpi_total.setValue(str(k.get('total_clients', 0)))
        self.kpi_idade_media.setValue(fmt_age(k.get('avg_age', np.nan)))
        
        # O KPI de gasto médio é mais informativo que a porcentagem de gênero
        avg_spend_val = k.get('avg_spend', np.nan)
        self.kpi_gasto_medio.setValue(f"R$ {avg_spend_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


    def _rebuild_tables(self):
        df = self.df_publico.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_publico, pd.DataFrame())
            return

        rename_map = {
            "Nome": "Nome do Cliente", "Genero": "Gênero", "Idade": "Idade",
            "Localizacao": "Localização", "Preferencias": "Preferências",
            "Frequencia_Compra_Mensal": "Compras/Mês", "Gasto_Medio": "Gasto Médio (R$)"
        }
        df = df.rename(columns=rename_map)

        cols_to_show = [
            "Nome do Cliente", "Gênero", "Idade", "Localização",
            "Compras/Mês", "Gasto Médio (R$)", "Preferências"
        ]
        existing_cols = [col for col in cols_to_show if col in df.columns]
        
        set_table_from_df(self.table_publico, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_location: self.layout_location.removeWidget(self.canvas_location); self.canvas_location.setParent(None)
        if self.canvas_gender:   self.layout_gender.removeWidget(self.canvas_gender);     self.canvas_gender.setParent(None)

        # Cores fixas para o tema claro
        text_color = 'black'
        bg_color = '#FFFFFF'

        # Gráfico 1: Barras por Localização (Top 10)
        fig1 = Figure(figsize=(6, 3.8), dpi=100); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        
        ser_loc = get_clients_by_location(self.df_publico, top_n=10)
        if not ser_loc.empty:
            ser_loc.sort_values().plot(kind='barh', ax=ax1, color='#6A0DAD')
        
        ax1.set_title("Top 10 Clientes por Localização", color=text_color)
        ax1.tick_params(axis='x', colors=text_color)
        ax1.tick_params(axis='y', colors=text_color)
        fig1.tight_layout()
        self.canvas_location = FigureCanvas(fig1); self.layout_location.addWidget(self.canvas_location)

        # Gráfico 2: Pizza por Gênero
        fig2 = Figure(figsize=(5, 3.8), dpi=100); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111)
        
        ser_gen = get_clients_by_gender(self.df_publico)
        if not ser_gen.empty:
            ax2.pie(ser_gen.values, labels=ser_gen.index, autopct='%1.1f%%', startangle=90, colors=['#FFA500', '#3CB371', '#C77DFF'])

        ax2.set_title("Distribuição por Gênero", color=text_color)
        fig2.tight_layout()
        self.canvas_gender = FigureCanvas(fig2); self.layout_gender.addWidget(self.canvas_gender)