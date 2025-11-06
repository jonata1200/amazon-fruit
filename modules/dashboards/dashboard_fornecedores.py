# modules/dashboards/dashboard_fornecedores.py

import pandas as pd

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QTabWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from modules.analysis.suppliers_analysis import analyze_suppliers_kpis
from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_rating
from .chart_generator import (
    create_supplier_ranking_chart,
    create_supplier_geo_chart,
    create_supplier_heatmap
)

class DashboardFornecedores(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_fornecedores = pd.DataFrame()

        self.kpi_total = None; self.kpi_avaliacao_media = None
        self.table_fornecedores = None
        
        # --- MUDANÇA 1: Renomear layouts para maior clareza ---
        self.canvas_ranking = None; self.layout_ranking = QVBoxLayout()
        self.canvas_geografico = None; self.layout_geografico = QVBoxLayout()
        self.canvas_heatmap = None; self.layout_heatmap = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20, 20, 20, 20); root.setSpacing(16)
        title = QLabel("Dashboard de Fornecedores"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)
        
        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Fornecedores"); self.kpi_avaliacao_media = KPIWidget("Avaliação Média")
        kpi_layout.addWidget(self.kpi_total); kpi_layout.addWidget(self.kpi_avaliacao_media)
        root.addLayout(kpi_layout)

        main_tab_widget = QTabWidget()

        # --- MUDANÇA 2: Nova estrutura com uma aba para cada gráfico ---

        # Aba 1: Gráfico de Ranking (Top e Bottom)
        ranking_widget = QWidget(); ranking_widget.setLayout(self.layout_ranking)
        main_tab_widget.addTab(ranking_widget, "⭐ Ranking por Avaliação")

        # Aba 2: Gráfico de Distribuição Geográfica
        geografico_widget = QWidget(); geografico_widget.setLayout(self.layout_geografico)
        main_tab_widget.addTab(geografico_widget, "📍 Distribuição Geográfica")

        # Aba 3: Matriz Fornecedor x Produto
        heatmap_widget = QWidget(); heatmap_widget.setLayout(self.layout_heatmap)
        main_tab_widget.addTab(heatmap_widget, "📊 Matriz Fornecedor x Produto")

        # Aba 4: Tabela de Fornecedores
        self.table_fornecedores = QTableView()
        main_tab_widget.addTab(self.table_fornecedores, "📋 Lista de Fornecedores")
        
        root.addWidget(main_tab_widget)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()

    def _reload_data(self):
        self.df_fornecedores = self.data_handler.load_table("Fornecedores")

    def _rebuild_kpis(self):
        k = analyze_suppliers_kpis(self.df_fornecedores)
        self.kpi_total.setValue(str(k.get('total_suppliers', 0))); self.kpi_avaliacao_media.setValue(fmt_rating(k.get('avg_rating', 0)))

    def _rebuild_tables(self):
        df = self.df_fornecedores.copy()
        if df is None or df.empty: set_table_from_df(self.table_fornecedores, pd.DataFrame()); return
        df = df.drop(columns=["ID_Fornecedor"], errors='ignore')
        rename_map = {"Nome_Fornecedor": "Nome", "Avaliacao": "Nota", "Produtos_Fornecidos": "Produtos"}
        df = df.rename(columns=rename_map)
        cols_order = ["Nome", "Nota", "E-mail", "Telefone", "Cidade", "Estado", "Produtos"]
        existing_cols = [col for col in cols_order if col in df.columns]
        set_table_from_df(self.table_fornecedores, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_ranking: self.layout_ranking.removeWidget(self.canvas_ranking); self.canvas_ranking.deleteLater(); self.canvas_ranking = None
        if self.canvas_geografico: self.layout_geografico.removeWidget(self.canvas_geografico); self.canvas_geografico.deleteLater(); self.canvas_geografico = None
        if self.canvas_heatmap: self.layout_heatmap.removeWidget(self.canvas_heatmap); self.canvas_heatmap.deleteLater(); self.canvas_heatmap = None

        # Gráfico 1: Ranking (Top/Bottom)
        fig1 = create_supplier_ranking_chart(self.df_fornecedores)
        self.canvas_ranking = FigureCanvas(fig1)
        self.layout_ranking.addWidget(self.canvas_ranking)

        # Gráfico 2: Geográfico
        fig2 = create_supplier_geo_chart(self.df_fornecedores)
        self.canvas_geografico = FigureCanvas(fig2)
        self.layout_geografico.addWidget(self.canvas_geografico)

        # Gráfico 3: Heatmap
        fig3 = create_supplier_heatmap(self.df_fornecedores)
        self.canvas_heatmap = FigureCanvas(fig3)
        self.layout_heatmap.addWidget(self.canvas_heatmap)