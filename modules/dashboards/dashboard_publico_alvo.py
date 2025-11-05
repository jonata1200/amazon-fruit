# modules/dashboards/dashboard_publico_alvo.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView, QTabWidget, QGridLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency, fmt_age
from modules.analysis.public_analysis import (
    analyze_public_kpis,
    get_clients_by_location,
    get_clients_by_gender
)

class DashboardPublicoAlvo(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_publico = pd.DataFrame()

        self.kpi_total = None
        self.kpi_idade_media = None
        self.kpi_gasto_medio = None
        
        self.table_clientes = None
        self.canvas_location = None
        self.canvas_gender = None
        self.layout_location = QVBoxLayout()
        self.layout_gender = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Dashboard de Público-Alvo"); title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QGridLayout(); kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Clientes")
        self.kpi_idade_media = KPIWidget("Idade Média")
        self.kpi_gasto_medio = KPIWidget("Gasto Médio por Cliente")
        kpi_layout.addWidget(self.kpi_total, 0, 0)
        kpi_layout.addWidget(self.kpi_idade_media, 0, 1)
        kpi_layout.addWidget(self.kpi_gasto_medio, 0, 2)
        root.addLayout(kpi_layout)

        # --- NOVO: Único QTabWidget para todo o conteúdo ---
        main_tab_widget = QTabWidget()

        # Aba 1: Tabela de Clientes
        self.table_clientes = QTableView()
        main_tab_widget.addTab(self.table_clientes, "👥 Clientes")

        # Aba 2: Gráfico de Clientes por Localização
        location_widget = QWidget()
        location_widget.setLayout(self.layout_location)
        main_tab_widget.addTab(location_widget, "📍 Clientes por Localização")

        # Aba 3: Gráfico de Distribuição por Gênero
        gender_widget = QWidget()
        gender_widget.setLayout(self.layout_gender)
        main_tab_widget.addTab(gender_widget, "🚻 Distribuição por Gênero")

        root.addWidget(main_tab_widget)

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
        
        # Correção do bug "R$ nan"
        self.kpi_gasto_medio.setValue(fmt_currency(k.get('avg_spend', np.nan)))

    def _rebuild_tables(self):
        df = self.df_publico.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_clientes, pd.DataFrame())
            return

        # Formata a coluna "Gasto Médio" para exibição
        if "Gasto_Medio" in df.columns:
            df["Gasto_Medio"] = pd.to_numeric(df["Gasto_Medio"], errors='coerce').apply(fmt_currency)
        
        # Renomeia colunas para melhor visualização
        rename_map = {
            "Nome": "Nome do Cliente", "Genero": "Gênero", "Idade": "Idade",
            "Localizacao": "Localização", "Preferencias": "Preferências",
            "Frequencia_Compra_Mensal": "Compras/Mês", "Gasto_Medio": "Gasto Médio"
        }
        df = df.rename(columns=rename_map)

        # --- MUDANÇA: Colunas a serem exibidas na tabela ---
        cols_to_show = [
            "Nome do Cliente", "Gênero", "Idade", "Localização",
            "Compras/Mês", "Gasto Médio", "Preferências"
        ]
        existing_cols = [col for col in cols_to_show if col in df.columns]
        
        set_table_from_df(self.table_clientes, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_location and self.canvas_location.parent() is not None: self.layout_location.removeWidget(self.canvas_location); self.canvas_location.deleteLater()
        if self.canvas_gender and self.canvas_gender.parent() is not None: self.layout_gender.removeWidget(self.canvas_gender); self.canvas_gender.deleteLater()

        text_color = 'black'
        bg_color = '#FFFFFF'

        # Gráfico 1: Barras por Localização (Top 10)
        fig1 = Figure(tight_layout=True); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        
        ser_loc = get_clients_by_location(self.df_publico, top_n=10)
        if not ser_loc.empty:
            ser_loc.sort_values().plot(kind='barh', ax=ax1, color='#6A0DAD')
        
        ax1.set_title("Top 10 Clientes por Localização", color=text_color)
        ax1.tick_params(axis='x', colors=text_color); ax1.tick_params(axis='y', colors=text_color)
        self.canvas_location = FigureCanvas(fig1); self.layout_location.addWidget(self.canvas_location)

        # Gráfico 2: Pizza por Gênero
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        
        ser_gen = get_clients_by_gender(self.df_publico)
        if not ser_gen.empty:
            ax2.pie(ser_gen.values, labels=ser_gen.index, autopct='%1.1f%%', startangle=90, colors=['#FFA500', '#3CB371', '#C77DFF'])

        ax2.set_title("Distribuição por Gênero", color=text_color)
        self.canvas_gender = FigureCanvas(fig2); self.layout_gender.addWidget(self.canvas_gender)