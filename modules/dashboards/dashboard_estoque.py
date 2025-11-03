import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QTableView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency

class DashboardEstoque(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name
        self.df_estoque = pd.DataFrame()

        self.kpi_produtos = None
        self.kpi_valor_estoque = None
        self.kpi_baixo = None

        self.table_estoque = None
        self.canvas_categoria = None
        self.canvas_baixo = None
        self.layout_categoria = None
        self.layout_baixo = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Estoque"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)

        kpi_grid = QGridLayout(); kpi_grid.setSpacing(16)
        self.kpi_produtos = KPIWidget("Produtos Únicos")
        self.kpi_valor_estoque = KPIWidget("Valor do Estoque (Custo)")
        self.kpi_baixo = KPIWidget("Itens com Estoque Baixo")
        kpi_grid.addWidget(self.kpi_produtos, 0, 0); kpi_grid.addWidget(self.kpi_valor_estoque, 0, 1); kpi_grid.addWidget(self.kpi_baixo, 0, 2)
        root.addLayout(kpi_grid)

        table_frame = QFrame(); table_layout = QVBoxLayout(table_frame); table_layout.setContentsMargins(0,0,0,0)
        self.table_estoque = QTableView(); table_layout.addWidget(self.table_estoque); root.addWidget(table_frame)

        charts_row = QHBoxLayout(); charts_row.setSpacing(16)
        chart1 = QFrame(); self.layout_categoria = QVBoxLayout(chart1); self.layout_categoria.setContentsMargins(0,0,0,0); charts_row.addWidget(chart1)
        chart2 = QFrame(); self.layout_baixo = QVBoxLayout(chart2); self.layout_baixo.setContentsMargins(0,0,0,0); charts_row.addWidget(chart2)
        root.addLayout(charts_row)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        # carrega snapshot concatenado (com Data_Snapshot) do loader novo
        self.df_estoque = self.data_handler.load_table("Estoque")

    def _rebuild_kpis(self):
        df = self.df_estoque if self.df_estoque is not None else pd.DataFrame()
        total = int(df['ID_Produto'].nunique()) if 'ID_Produto' in df.columns else int(len(df))
        valor = 0.0
        if {'Quantidade_Estoque','Preco_Custo'}.issubset(df.columns):
            q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce').fillna(0)
            c = pd.to_numeric(df['Preco_Custo'], errors='coerce').fillna(0.0)
            valor = float((q*c).sum())
        baixo = 0
        if {'Quantidade_Estoque','Nivel_Minimo_Estoque'}.issubset(df.columns):
            q2 = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce')
            n2 = pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')
            baixo = int((q2 <= n2).sum())

        self.kpi_produtos.setValue(str(total))
        self.kpi_valor_estoque.setValue(fmt_currency(valor))
        self.kpi_baixo.setValue(str(baixo))

    def _rebuild_tables(self):
        set_table_from_df(self.table_estoque, self.df_estoque)

    def _rebuild_charts(self):
        if self.canvas_categoria: self.layout_categoria.removeWidget(self.canvas_categoria); self.canvas_categoria.setParent(None); self.canvas_categoria=None
        if self.canvas_baixo:     self.layout_baixo.removeWidget(self.canvas_baixo);       self.canvas_baixo.setParent(None);     self.canvas_baixo=None

        # Pizza por Categoria
        fig1 = Figure(figsize=(5.2, 3.2), dpi=100); ax1 = fig1.add_subplot(111)
        if not self.df_estoque.empty and 'Categoria' in self.df_estoque.columns:
            s = self.df_estoque['Categoria'].astype(str).value_counts()
            if not s.empty: ax1.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Distribuição por Categoria"); fig1.tight_layout()
        self.canvas_categoria = FigureCanvas(fig1); self.layout_categoria.addWidget(self.canvas_categoria)

        # Barra horizontal: Itens abaixo do mínimo (gap)
        fig2 = Figure(figsize=(5.6, 3.2), dpi=100); ax2 = fig2.add_subplot(111)
        req = {'Nome_Produto','Quantidade_Estoque','Nivel_Minimo_Estoque'}
        if not self.df_estoque.empty and req.issubset(self.df_estoque.columns):
            dfx = self.df_estoque.copy()
            dfx['gap'] = pd.to_numeric(dfx['Nivel_Minimo_Estoque'], errors='coerce') - pd.to_numeric(dfx['Quantidade_Estoque'], errors='coerce')
            low = dfx[dfx['gap'] > 0].sort_values('gap', ascending=False).head(10)
            if not low.empty:
                ax2.barh(low['Nome_Produto'].astype(str), low['gap']); ax2.invert_yaxis()
        ax2.set_title("Itens com Estoque Baixo (gap)"); fig2.tight_layout()
        self.canvas_baixo = FigureCanvas(fig2); self.layout_baixo.addWidget(self.canvas_baixo)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()