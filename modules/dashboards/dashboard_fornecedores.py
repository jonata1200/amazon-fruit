# modules/dashboards/dashboard_fornecedores.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableView, QFrame, QTabWidget # QTabWidget é a peça central da mudança
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import seaborn as sns

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_rating
from modules.analysis.suppliers_analysis import (
    analyze_suppliers_kpis,
    create_supplier_product_matrix
)

class DashboardFornecedores(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_fornecedores = pd.DataFrame()

        # Widgets da UI
        self.kpi_total = None
        self.kpi_avaliacao_media = None
        self.table_fornecedores = None
        self.canvas_heatmap = None
        self.layout_heatmap = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        """
        --- MUDANÇA PRINCIPAL: Reintroduzindo o QTabWidget para organizar a UI ---
        """
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        title = QLabel("Dashboard de Fornecedores")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # KPIs permanecem no topo, fora das abas.
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Fornecedores")
        self.kpi_avaliacao_media = KPIWidget("Avaliação Média")
        kpi_layout.addWidget(self.kpi_total)
        kpi_layout.addWidget(self.kpi_avaliacao_media)
        root.addLayout(kpi_layout)

        # 1. Cria o widget de abas que vai conter a tabela e o gráfico.
        main_tab_widget = QTabWidget()

        # 2. Cria a Aba 1: Tabela de Fornecedores
        # A própria QTableView pode ser o widget da aba.
        self.table_fornecedores = QTableView()
        main_tab_widget.addTab(self.table_fornecedores, "📋 Lista de Fornecedores")

        # 3. Cria a Aba 2: Gráfico Heatmap
        # Para o gráfico, usamos um QWidget como container.
        chart_widget = QWidget()
        chart_widget.setLayout(self.layout_heatmap) # O layout do gráfico é aplicado a este widget.
        main_tab_widget.addTab(chart_widget, "📊 Matriz Fornecedor x Produto")
        
        # 4. Adiciona o conjunto de abas ao layout principal da janela.
        root.addWidget(main_tab_widget)


    # Nenhuma mudança necessária nos métodos abaixo. Eles já estão corretos.
    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_fornecedores = self.data_handler.load_table("Fornecedores")

    def _rebuild_kpis(self):
        k = analyze_suppliers_kpis(self.df_fornecedores)
        self.kpi_total.setValue(str(k.get('total_suppliers', 0)))
        self.kpi_avaliacao_media.setValue(fmt_rating(k.get('avg_rating', 0)))

    def _rebuild_tables(self):
        df = self.df_fornecedores.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_fornecedores, pd.DataFrame())
            return
        df = df.drop(columns=["ID_Fornecedor"], errors='ignore')
        # Renomeação simplificada para caber melhor na tabela
        rename_map = {"Nome_Fornecedor": "Nome", "Avaliacao": "Nota", "Produtos_Fornecidos": "Produtos"}
        df = df.rename(columns=rename_map)
        cols_order = ["Nome", "Nota", "E-mail", "Telefone", "Cidade", "Estado", "Produtos"]
        existing_cols = [col for col in cols_order if col in df.columns]
        set_table_from_df(self.table_fornecedores, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_heatmap: self.layout_heatmap.removeWidget(self.canvas_heatmap); self.canvas_heatmap.deleteLater()

        text_color = 'black'
        bg_color = '#FFFFFF'
        matrix = create_supplier_product_matrix(self.df_fornecedores)

        if not matrix.empty:
            fig = Figure(figsize=(10, 8), tight_layout=True)
            fig.patch.set_facecolor(bg_color)
            ax = fig.add_subplot(111)

            sns.heatmap(
                matrix, ax=ax, cmap="YlGn", linewidths=.5, 
                linecolor='lightgray', cbar=False
            )

            ax.set_title("Matriz de Fornecedores por Produtos", color=text_color, fontsize=14)
            ax.set_xlabel("Tipos de Produto", fontsize=10)
            ax.set_ylabel("Fornecedores", fontsize=10)
            ax.tick_params(axis='x', labelrotation=45, colors=text_color)
            ax.tick_params(axis='y', colors=text_color)

            self.canvas_heatmap = FigureCanvas(fig)
            self.layout_heatmap.addWidget(self.canvas_heatmap)