# modules/dashboards/dashboard_estoque.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QFrame, QTableView
)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df


class DashboardEstoque(QWidget):
    """
    Dashboard de Estoque.
    - Respeita período global via DataHandler.load_table("Estoque")
    - KPIs + Tabela + 2 gráficos (pizza por categoria e itens abaixo do mínimo)
    """

    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # Data
        self.df_estoque = pd.DataFrame()

        # KPIs (frames que guardam o _value_label internamente)
        self.kpi_produtos = None
        self.kpi_valor_estoque = None
        self.kpi_baixo = None

        # Tabela
        self.table_estoque = None

        # Gráficos
        self.canvas_categoria = None
        self.canvas_baixo = None

        # Layouts auxiliares para inserir os gráficos
        self.layout_categoria = None
        self.layout_baixo = None

        self.build_ui()
        self.refresh()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # Título
        title = QLabel("Estoque")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # ===== KPIs =====
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(16)

        self.kpi_produtos = self._create_kpi_box("Produtos Únicos")
        self.kpi_valor_estoque = self._create_kpi_box("Valor do Estoque (Custo)", value_color="#2E8B57")
        self.kpi_baixo = self._create_kpi_box("Itens com Estoque Baixo", value_color="#C21807")

        kpi_grid.addWidget(self.kpi_produtos,      0, 0)
        kpi_grid.addWidget(self.kpi_valor_estoque, 0, 1)
        kpi_grid.addWidget(self.kpi_baixo,         0, 2)

        root.addLayout(kpi_grid)

        # ===== Tabela =====
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_estoque = QTableView()
        table_layout.addWidget(self.table_estoque)
        root.addWidget(table_frame)

        # ===== Gráficos =====
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        # container 1
        chart1 = QFrame()
        self.layout_categoria = QVBoxLayout(chart1)
        self.layout_categoria.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart1)

        # container 2
        chart2 = QFrame()
        self.layout_baixo = QVBoxLayout(chart2)
        self.layout_baixo.setContentsMargins(0, 0, 0, 0)
        charts_row.addWidget(chart2)

        root.addLayout(charts_row)

    # ------------------------------------------------------------------
    # Ciclo de atualização
    # ------------------------------------------------------------------
    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        # usa o período global automaticamente
        self.df_estoque = self.data_handler.load_table("Estoque")

    def _rebuild_kpis(self):
        df = self.df_estoque if self.df_estoque is not None else pd.DataFrame()

        # produtos únicos
        if 'ID_Produto' in df.columns:
            total = int(df['ID_Produto'].nunique())
        else:
            total = int(len(df))

        # valor do estoque
        valor = 0.0
        if {'Quantidade_Estoque', 'Preco_Custo'}.issubset(df.columns):
            q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce').fillna(0)
            c = pd.to_numeric(df['Preco_Custo'], errors='coerce').fillna(0.0)
            valor = float((q * c).sum())

        # itens abaixo do mínimo
        baixo = 0
        req = {'Quantidade_Estoque', 'Nivel_Minimo_Estoque'}
        if req.issubset(df.columns):
            q2 = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce')
            n2 = pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')
            baixo = int((q2 <= n2).sum())

        # escreve nos cartões
        self._set_kpi_value(self.kpi_produtos, str(total))
        self._set_kpi_value(self.kpi_valor_estoque, self._fmt_currency(valor))
        self._set_kpi_value(self.kpi_baixo, str(baixo))

    def _rebuild_tables(self):
        set_table_from_df(self.table_estoque, self.df_estoque)

    def _rebuild_charts(self):
        # remove canvases antigos (se existirem)
        if self.canvas_categoria is not None:
            self.layout_categoria.removeWidget(self.canvas_categoria)
            self.canvas_categoria.setParent(None)
            self.canvas_categoria = None
        if self.canvas_baixo is not None:
            self.layout_baixo.removeWidget(self.canvas_baixo)
            self.canvas_baixo.setParent(None)
            self.canvas_baixo = None

        # --- Gráfico 1: Pizza por Categoria ---
        fig1 = Figure(figsize=(5.2, 3.2), dpi=100)
        ax1 = fig1.add_subplot(111)
        if not self.df_estoque.empty and 'Categoria' in self.df_estoque.columns:
            s = self.df_estoque['Categoria'].astype(str).value_counts()
            if not s.empty:
                ax1.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Distribuição por Categoria")
        fig1.tight_layout()
        self.canvas_categoria = FigureCanvas(fig1)
        self.layout_categoria.addWidget(self.canvas_categoria)

        # --- Gráfico 2: Itens abaixo do mínimo (barra horizontal) ---
        fig2 = Figure(figsize=(5.6, 3.2), dpi=100)
        ax2 = fig2.add_subplot(111)
        req = {'Nome_Produto', 'Quantidade_Estoque', 'Nivel_Minimo_Estoque'}
        if not self.df_estoque.empty and req.issubset(self.df_estoque.columns):
            dfx = self.df_estoque.copy()
            dfx['gap'] = pd.to_numeric(dfx['Nivel_Minimo_Estoque'], errors='coerce') - \
                         pd.to_numeric(dfx['Quantidade_Estoque'], errors='coerce')
            low = dfx[dfx['gap'] > 0].sort_values('gap', ascending=False).head(10)
            if not low.empty:
                ax2.barh(low['Nome_Produto'].astype(str), low['gap'])
                ax2.invert_yaxis()
        ax2.set_title("Itens com Estoque Baixo (gap)")
        fig2.tight_layout()
        self.canvas_baixo = FigureCanvas(fig2)
        self.layout_baixo.addWidget(self.canvas_baixo)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _create_kpi_box(self, title, value_color=None):
        box = QFrame()
        box.setObjectName("KPIFrame")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(12, 10, 12, 10)

        t = QLabel(title)
        t.setObjectName("KPITitleLabel")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)

        v = QLabel("—")
        v.setObjectName("KPIValueLabel")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if value_color:
            v.setStyleSheet(f"color: {value_color};")

        lay.addWidget(t)
        lay.addWidget(v)

        # guardamos a referência do label no próprio frame
        box._value_label = v
        return box

    def _set_kpi_value(self, kpi_frame: QFrame, text: str):
        if kpi_frame is None or not hasattr(kpi_frame, "_value_label"):
            return
        kpi_frame._value_label.setText(text)

    @staticmethod
    def _fmt_currency(v):
        try:
            return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return "R$ 0,00"

    # Tema (opcional)
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        # se necessário, ajustar cores de gráficos por tema
        self._rebuild_charts()