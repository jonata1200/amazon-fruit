# modules/dashboards/dashboard_publico_alvo.py

import pandas as pd
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QTableView, QTabWidget
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency, fmt_age
from modules.analysis.public_analysis import analyze_public_kpis
from .chart_generator import (
    create_public_location_chart,
    create_public_gender_chart,
    create_public_channel_chart
)

class DashboardPublicoAlvo(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_publico = pd.DataFrame()

        # Widgets da interface
        self.kpi_total = None
        self.kpi_idade_media = None
        self.kpi_gasto_medio = None
        
        self.table_clientes = None
        self.canvas_location = None
        self.canvas_gender = None
        self.layout_location = QVBoxLayout()
        self.layout_gender = QVBoxLayout()

        self.canvas_canal = None
        self.layout_canal = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        """Constrói a interface visual do dashboard."""
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard de Público-Alvo")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QGridLayout()
        kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Clientes")
        self.kpi_idade_media = KPIWidget("Idade Média")
        self.kpi_gasto_medio = KPIWidget("Gasto Médio por Cliente")
        kpi_layout.addWidget(self.kpi_total, 0, 0)
        kpi_layout.addWidget(self.kpi_idade_media, 0, 1)
        kpi_layout.addWidget(self.kpi_gasto_medio, 0, 2)
        root.addLayout(kpi_layout)

        main_tab_widget = QTabWidget()

        # Aba 1: Gráfico de Clientes por Localização
        location_widget = QWidget()
        location_widget.setLayout(self.layout_location)
        main_tab_widget.addTab(location_widget, "📍 Clientes por Localização")

        # Aba 2: Gráfico de Distribuição por Gênero
        gender_widget = QWidget()
        gender_widget.setLayout(self.layout_gender)
        main_tab_widget.addTab(gender_widget, "🚻 Distribuição por Gênero")

        # Aba 3: Gráfico de Distribuição por Canais de Venda
        canal_widget = QWidget()
        canal_widget.setLayout(self.layout_canal)
        main_tab_widget.addTab(canal_widget, "📊 Vendas por Canal")

        # Aba 4: Tabela de Clientes
        self.table_clientes = QTableView()
        main_tab_widget.addTab(self.table_clientes, "👥 Clientes")

        root.addWidget(main_tab_widget)

    def refresh(self):
        """Ponto de entrada para atualizar todos os dados do dashboard."""
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        """Carrega (ou recarrega) os dados do DataHandler."""
        self.df_publico = self.data_handler.load_table("Publico_Alvo")

    def _rebuild_kpis(self):
        """
        2. LÓGICA DE KPI SIMPLIFICADA
        Chama a função de análise e apenas exibe os resultados.
        """
        # A função analyze_public_kpis centraliza toda a lógica de cálculo.
        kpis = analyze_public_kpis(self.df_publico)
        
        self.kpi_total.setValue(str(kpis.get('total_clients', 0)))
        self.kpi_idade_media.setValue(fmt_age(kpis.get('avg_age', np.nan)))
        
        # Nota: O KPI de gasto médio funcionará automaticamente quando uma coluna
        # 'Gasto_Medio' ou 'Ticket_Medio' for adicionada ao seu arquivo Excel.
        self.kpi_gasto_medio.setValue(fmt_currency(kpis.get('avg_spend', np.nan)))

    def _rebuild_tables(self):
        """
        3. TABELA CORRIGIDA
        Prepara e exibe o DataFrame na tabela da UI com as colunas corretas.
        """
        df = self.df_publico.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_clientes, pd.DataFrame())
            return

        # Mapa de renomeação para nomes mais amigáveis na interface.
        rename_map = {
            "Nome": "Nome do Cliente", 
            "Genero": "Gênero", 
            "Idade": "Idade",
            "Cidade": "Cidade",
            "Estado": "UF",
            "Canal_de_venda": "Canal de Venda"
        }
        df = df.rename(columns=rename_map)

        # Lista define quais colunas e em que ordem aparecerão na tabela.
        cols_to_show = [
            "Nome do Cliente", "Gênero", "Idade", "Cidade", "UF", "Canal de Venda"
        ]
        
        # Filtra apenas as colunas que realmente existem para evitar erros.
        existing_cols = [col for col in cols_to_show if col in df.columns]
        
        set_table_from_df(self.table_clientes, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_location: self.layout_location.removeWidget(self.canvas_location); self.canvas_location.deleteLater()
        if self.canvas_gender: self.layout_gender.removeWidget(self.canvas_gender); self.canvas_gender.deleteLater()
        if self.canvas_canal: self.layout_canal.removeWidget(self.canvas_canal); self.canvas_canal.deleteLater()

        # Gráfico 1: Localização
        fig1 = create_public_location_chart(self.df_publico)
        self.canvas_location = FigureCanvas(fig1)
        self.layout_location.addWidget(self.canvas_location)

        # Gráfico 2: Gênero
        fig2 = create_public_gender_chart(self.df_publico)
        self.canvas_gender = FigureCanvas(fig2)
        self.layout_gender.addWidget(self.canvas_gender)

        # Gráfico 3: Canal de Venda
        fig3 = create_public_channel_chart(self.df_publico)
        self.canvas_canal = FigureCanvas(fig3)
        self.layout_canal.addWidget(self.canvas_canal)