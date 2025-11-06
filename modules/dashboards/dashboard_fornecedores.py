# modules/dashboards/dashboard_fornecedores.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QTabWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_rating
from modules.analysis.suppliers_analysis import (
    analyze_suppliers_kpis,
    create_supplier_product_matrix,
    get_top_bottom_suppliers,
    get_suppliers_by_state
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
        # Limpa todos os canvases
        if self.canvas_ranking: self.layout_ranking.removeWidget(self.canvas_ranking); self.canvas_ranking.deleteLater(); self.canvas_ranking = None
        if self.canvas_geografico: self.layout_geografico.removeWidget(self.canvas_geografico); self.canvas_geografico.deleteLater(); self.canvas_geografico = None
        if self.canvas_heatmap: self.layout_heatmap.removeWidget(self.canvas_heatmap); self.canvas_heatmap.deleteLater(); self.canvas_heatmap = None

        text_color = 'black'; bg_color = '#FFFFFF'

        # --- MUDANÇA 3: A lógica de plotagem é a mesma, só muda onde cada gráfico é adicionado ---

        # Gráfico 1: Top e Bottom 5 Fornecedores
        fig1, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(8, 8), tight_layout=True)
        fig1.patch.set_facecolor(bg_color)
        suppliers = get_top_bottom_suppliers(self.df_fornecedores, n=5)
        top5 = suppliers['top']; bottom5 = suppliers['bottom']
        if not top5.empty:
            top5.sort_values('Avaliacao', ascending=True).plot(kind='barh', x='Nome_Fornecedor', y='Avaliacao', ax=ax_top, color='#2ECC71', legend=False)
            ax_top.set_title("Top 5 Melhores Fornecedores", color=text_color); ax_top.set_xlim(0, 5)
        if not bottom5.empty:
            bottom5.sort_values('Avaliacao', ascending=False).plot(kind='barh', x='Nome_Fornecedor', y='Avaliacao', ax=ax_bottom, color='#E74C3C', legend=False)
            ax_bottom.set_title("Top 5 Piores Fornecedores", color=text_color); ax_bottom.set_xlim(0, 5)
        self.canvas_ranking = FigureCanvas(fig1); self.layout_ranking.addWidget(self.canvas_ranking)

        # Gráfico 2: Fornecedores por Estado
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color); ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        by_state = get_suppliers_by_state(self.df_fornecedores)
        if not by_state.empty:
            by_state.sort_values().plot(kind='barh', ax=ax2, color='#3498DB')
            ax2.set_title("Distribuição de Fornecedores por Estado", color=text_color)
        self.canvas_geografico = FigureCanvas(fig2); self.layout_geografico.addWidget(self.canvas_geografico)

        # Gráfico 3: Matriz (Heatmap)
        fig3 = Figure(figsize=(10, 8), tight_layout=True); fig3.patch.set_facecolor(bg_color); ax3 = fig3.add_subplot(111)
        matrix = create_supplier_product_matrix(self.df_fornecedores)
        if not matrix.empty:
            sns.heatmap(matrix, ax=ax3, cmap="YlGn", linewidths=.5, linecolor='lightgray', cbar=False)
            ax3.set_title("Matriz de Fornecedores por Produtos", color=text_color, fontsize=14)
            ax3.tick_params(axis='x', labelrotation=45, colors=text_color); ax3.tick_params(axis='y', colors=text_color)
        self.canvas_heatmap = FigureCanvas(fig3); self.layout_heatmap.addWidget(self.canvas_heatmap)