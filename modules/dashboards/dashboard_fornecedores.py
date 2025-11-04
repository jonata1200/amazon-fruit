# modules/dashboards/dashboard_fornecedores.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_rating
from modules.analysis.suppliers_analysis import (
    analyze_suppliers_kpis,
    get_product_types_distribution
)

class DashboardFornecedores(QWidget):
    def __init__(self, data_handler): # Argumento de tema removido
        super().__init__()
        self.data_handler = data_handler
        # self.theme_name removido

        self.df_fornecedores = pd.DataFrame()
        self.kpi_total = None
        self.kpi_avaliacao_media = None
        self.table_fornecedores = None
        self.canvas_rating = None
        self.canvas_types = None
        self.layout_rating = None
        self.layout_types = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Dashboard de Fornecedores"); title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(16)
        self.kpi_total = KPIWidget("Total de Fornecedores")
        self.kpi_avaliacao_media = KPIWidget("Avaliação Média")
        kpi_layout.addWidget(self.kpi_total); kpi_layout.addWidget(self.kpi_avaliacao_media)
        root.addLayout(kpi_layout)

        table_frame = QFrame(); table_layout = QVBoxLayout(table_frame); table_layout.setContentsMargins(0,0,0,0)
        self.table_fornecedores = QTableView(); table_layout.addWidget(self.table_fornecedores)
        root.addWidget(table_frame)

        charts_row = QHBoxLayout(); charts_row.setSpacing(16)
        chart1 = QFrame(); self.layout_rating = QVBoxLayout(chart1); self.layout_rating.setContentsMargins(0,0,0,0)
        chart2 = QFrame(); self.layout_types  = QVBoxLayout(chart2); self.layout_types.setContentsMargins(0,0,0,0)
        charts_row.addWidget(chart1); charts_row.addWidget(chart2); root.addLayout(charts_row)

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

        # Ocultar, reordenar e renomear colunas
        df = df.drop(columns=[c for c in ["ID_Fornecedor"] if c in df.columns], errors='ignore')
        
        rename_map = {
            "Nome_Fornecedor": "Nome do Fornecedor", "CNPJ": "CNPJ",
            "Telefone": "Telefone", "Email": "E-mail", "Endereco": "Endereço",
            "Estado": "Estado", "Cidade": "Cidade", "Avaliacao": "Avaliação",
            "Produtos_Fornecidos": "Produtos Fornecidos"
        }
        df = df.rename(columns=rename_map)

        cols_order = [
            "Nome do Fornecedor", "Avaliação", "E-mail", "Telefone",
            "Cidade", "Estado", "Produtos Fornecidos"
        ]
        existing_cols = [col for col in cols_order if col in df.columns]

        set_table_from_df(self.table_fornecedores, df[existing_cols])

    def _rebuild_charts(self):
        if self.canvas_rating: self.layout_rating.removeWidget(self.canvas_rating); self.canvas_rating.setParent(None)
        if self.canvas_types:  self.layout_types.removeWidget(self.canvas_types);  self.canvas_types.setParent(None)

        # Cores fixas para o tema claro
        text_color = 'black'
        bg_color = '#FFFFFF'

        # Gráfico 1: Top 10 por avaliação (Barra Horizontal)
        fig1 = Figure(figsize=(6.2, 3.8), dpi=100); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)

        df_rating = self.df_fornecedores
        if not df_rating.empty and {'Nome_Fornecedor','Avaliacao'}.issubset(df_rating.columns):
            dfx = df_rating.copy()
            dfx['Avaliacao'] = pd.to_numeric(dfx['Avaliacao'], errors='coerce')
            dfx = dfx.dropna(subset=['Avaliacao']).sort_values('Avaliacao', ascending=True).tail(10)
            if not dfx.empty:
                ax1.barh(dfx['Nome_Fornecedor'].astype(str), dfx['Avaliacao'], color='#2E8B57')
                ax1.set_xlim(0, 5)
        
        ax1.set_title("Avaliação dos Fornecedores (Top 10)", color=text_color)
        ax1.tick_params(axis='x', colors=text_color)
        ax1.tick_params(axis='y', colors=text_color)
        fig1.tight_layout()
        self.canvas_rating = FigureCanvas(fig1); self.layout_rating.addWidget(self.canvas_rating)

        # Gráfico 2: Pizza de tipos de produtos fornecidos
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111)

        ser = get_product_types_distribution(self.df_fornecedores)
        if not ser.empty:
            wedges, texts, autotexts = ax2.pie(ser.values, autopct='%1.1f%%', startangle=90)
            ax2.legend(wedges, ser.index, title="Tipos de Produto", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        ax2.set_title("Tipos de Produtos Fornecidos", color=text_color)
        fig2.tight_layout()
        self.canvas_types = FigureCanvas(fig2); self.layout_types.addWidget(self.canvas_types)