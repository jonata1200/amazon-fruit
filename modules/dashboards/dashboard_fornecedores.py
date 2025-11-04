from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_rating

# Camada de análise
from modules.analysis.suppliers_analysis import (
    analyze_suppliers_kpis,          # {'total_suppliers','avg_rating'}
    get_product_types_distribution   # Series com contagem por tipo (a partir de 'Produtos_Fornecidos')
)

class DashboardFornecedores(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

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
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()

    def _reload_data(self):
        self.df_fornecedores = self.data_handler.load_table("Fornecedores")

    def _rebuild_kpis(self):
        k = analyze_suppliers_kpis(self.df_fornecedores)
        self.kpi_total.setValue(str(k.get('total_suppliers', 0)))
        self.kpi_avaliacao_media.setValue(fmt_rating(k.get('avg_rating', 0)))

    def _rebuild_tables(self):
        df = self.df_fornecedores.copy()

        # 1) Ocultar colunas indesejadas
        drop_cols = [c for c in ["ID_Fornecedor"] if c in df.columns]
        if drop_cols:
            df = df.drop(columns=drop_cols)

        # 2) Reordenar colunas
        ordem = [c for c in [
            "Nome_Fornecedor", "CNPJ", "Telefone", "Email",
            "Endereco", "Estado", "Cidade", "Avaliacao", "Produtos_Fornecidos"
        ] if c in df.columns]
        outras = [c for c in df.columns if c not in ordem]
        if ordem:
            df = df[ordem + outras]

        # 3) Renomear colunas para português correto
        rename_map = {
            "Nome_Fornecedor": "Nome do Fornecedor",
            "CNPJ": "CNPJ",
            "Telefone": "Telefone",
            "Email": "E-mail",
            "Endereco": "Endereço",
            "Estado": "Estado",
            "Cidade": "Cidade",
            "Avaliacao": "Avaliação",
            "Produtos_Fornecidos": "Produtos Fornecidos"
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        set_table_from_df(self.table_fornecedores, df)

    def _rebuild_charts(self):
        if self.canvas_rating: self.layout_rating.removeWidget(self.canvas_rating); self.canvas_rating.setParent(None)
        if self.canvas_types:  self.layout_types.removeWidget(self.canvas_types);  self.canvas_types.setParent(None)

        df = self.df_fornecedores

        # Top 10 por avaliação
        fig1 = Figure(figsize=(6.2, 3.8), dpi=100); ax1 = fig1.add_subplot(111)
        if not df.empty and {'Nome_Fornecedor','Avaliacao'}.issubset(df.columns):
            dfx = df.copy(); dfx['Avaliacao'] = pd.to_numeric(dfx['Avaliacao'], errors='coerce')
            dfx = dfx.dropna(subset=['Avaliacao']).sort_values('Avaliacao', ascending=True).tail(10)
            if not dfx.empty:
                ax1.barh(dfx['Nome_Fornecedor'].astype(str), dfx['Avaliacao']); ax1.set_xlim(0, 5)
        ax1.set_title("Avaliação dos Fornecedores (Top 10)"); fig1.tight_layout()
        self.canvas_rating = FigureCanvas(fig1); self.layout_rating.addWidget(self.canvas_rating)

        # Pizza: tipos de produtos fornecidos
        fig2 = Figure(figsize=(5.2, 3.8), dpi=100); ax2 = fig2.add_subplot(111)
        ser = get_product_types_distribution(df)
        if not ser.empty:
            ax2.pie(ser.values, labels=ser.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Tipos de Produtos Fornecidos"); fig2.tight_layout()
        self.canvas_types = FigureCanvas(fig2); self.layout_types.addWidget(self.canvas_types)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()