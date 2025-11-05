# modules/dashboards/dashboard_estoque.py

import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel,
    QTableView, QTabWidget
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from modules.ui.qt_utils import set_table_with_conditional_formatting
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency

class DashboardEstoque(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_estoque = pd.DataFrame()

        self.kpi_produtos = None
        self.kpi_valor_estoque = None
        self.kpi_baixo = None
        self.kpi_compra_urgente = None
        self.table_inventario = None
        self.canvas_categoria = None
        self.canvas_baixo = None
        self.layout_categoria = QVBoxLayout()
        self.layout_baixo = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Dashboard de Estoque"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)
        
        kpi_grid = QGridLayout(); kpi_grid.setSpacing(16)
        self.kpi_produtos = KPIWidget("📦 Produtos Únicos")
        self.kpi_valor_estoque = KPIWidget("💰 Valor do Estoque (Custo)")
        self.kpi_baixo = KPIWidget("⚠️ Itens em Alerta")
        self.kpi_compra_urgente = KPIWidget("🛒 Compra Urgente (Custo)")
        kpi_grid.addWidget(self.kpi_produtos, 0, 0); kpi_grid.addWidget(self.kpi_valor_estoque, 0, 1)
        kpi_grid.addWidget(self.kpi_baixo, 0, 2); kpi_grid.addWidget(self.kpi_compra_urgente, 0, 3)
        root.addLayout(kpi_grid)
        
        main_tab_widget = QTabWidget()

        categoria_widget = QWidget()
        categoria_widget.setLayout(self.layout_categoria)
        main_tab_widget.addTab(categoria_widget, "📊 Valor por Categoria")

        ruptura_widget = QWidget()
        ruptura_widget.setLayout(self.layout_baixo)
        main_tab_widget.addTab(ruptura_widget, "📉 Maiores Rupturas")
        
        self.table_inventario = QTableView()
        main_tab_widget.addTab(self.table_inventario, "📋 Inventário Completo")
        
        root.addWidget(main_tab_widget)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_estoque = self.data_handler.load_table("Estoque")

    def _rebuild_kpis(self):
        df = self.df_estoque if self.df_estoque is not None else pd.DataFrame()
        total = int(df['ID_Produto'].nunique()) if 'ID_Produto' in df.columns and not df.empty else 0
        q_total = pd.to_numeric(df.get('Quantidade_Estoque'), errors='coerce').fillna(0)
        c_total = pd.to_numeric(df.get('Preco_Custo'), errors='coerce').fillna(0.0)
        valor = float((q_total * c_total).sum())
        df_alertas = pd.DataFrame()
        if not df.empty:
            q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce')
            n = pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')
            df_alertas = df[q <= n]
        baixo = len(df_alertas)
        valor_compra_urgente = 0.0
        if not df_alertas.empty:
            q_a = pd.to_numeric(df_alertas['Quantidade_Estoque'], errors='coerce').fillna(0)
            n_a = pd.to_numeric(df_alertas['Nivel_Minimo_Estoque'], errors='coerce').fillna(0)
            c_a = pd.to_numeric(df_alertas['Preco_Custo'], errors='coerce').fillna(0.0)
            gap = n_a - q_a
            valor_compra_urgente = float((gap * c_a).sum())
        self.kpi_produtos.setValue(str(total))
        self.kpi_valor_estoque.setValue(fmt_currency(valor))
        self.kpi_baixo.setValue(str(baixo))
        self.kpi_compra_urgente.setValue(fmt_currency(valor_compra_urgente))

    def _format_df_for_display(self, df_original: pd.DataFrame):
        if df_original is None or df_original.empty: return pd.DataFrame()
        df = df_original.copy()
        if "Data_Validade" in df.columns:
            df["Data_Validade"] = pd.to_datetime(df["Data_Validade"], errors="coerce").dt.strftime("%d/%m/%Y")
        for col in ["Preco_Custo", "Preco_Venda"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).map(fmt_currency)
        cols_to_drop = ["ID_Produto", "ID_Fornecedor", "Ano", "Mes", "Data_Snapshot"]
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
        rename_map = {
            "Nome_Produto": "Nome do Produto", "Categoria": "Categoria", 
            "Quantidade_Estoque": "Estoque Atual", "Nivel_Minimo_Estoque": "Estoque Mínimo", 
            "Preco_Custo": "Preço de Custo", "Preco_Venda": "Preço de Venda", 
            "Data_Validade": "Data de Validade"
        }
        df = df.rename(columns=rename_map)
        return df

    def _rebuild_tables(self):
        df_completo_fmt = self._format_df_for_display(self.df_estoque)
        set_table_with_conditional_formatting(self.table_inventario, df_completo_fmt)
    
    def _rebuild_charts(self):
        if self.canvas_categoria and self.canvas_categoria.parent() is not None: self.layout_categoria.removeWidget(self.canvas_categoria); self.canvas_categoria.deleteLater(); self.canvas_categoria = None
        if self.canvas_baixo and self.canvas_baixo.parent() is not None: self.layout_baixo.removeWidget(self.canvas_baixo); self.canvas_baixo.deleteLater(); self.canvas_baixo = None
        text_color = 'black'
        bg_color = '#FFFFFF'
        
        # Gráfico 1: Valor de Estoque por Categoria
        fig1 = Figure(tight_layout=True); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        if self.df_estoque is not None and not self.df_estoque.empty:
            dfx = self.df_estoque.copy()
            dfx['Valor_Total'] = pd.to_numeric(dfx['Quantidade_Estoque'], errors='coerce') * pd.to_numeric(dfx['Preco_Custo'], errors='coerce')
            valor_por_cat = dfx.groupby('Categoria')['Valor_Total'].sum().sort_values(ascending=True)
            if not valor_por_cat.empty:
                # --- MUDANÇA AQUI: Cor do Gráfico Alterada ---
                valor_por_cat.plot(kind='barh', ax=ax1, color='#3498DB') # Laranja ('#FF8C00') alterado para Azul
                # --- FIM DA MUDANÇA ---
        ax1.set_title("Valor de Estoque por Categoria", color=text_color)
        ax1.tick_params(axis='x', colors=text_color); ax1.tick_params(axis='y', colors=text_color)
        self.canvas_categoria = FigureCanvas(fig1); self.layout_categoria.addWidget(self.canvas_categoria)
        
        # Gráfico 2: Maiores Rupturas de Estoque
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        if self.df_estoque is not None and not self.df_estoque.empty:
            q = pd.to_numeric(self.df_estoque['Quantidade_Estoque'], errors='coerce')
            n = pd.to_numeric(self.df_estoque['Nivel_Minimo_Estoque'], errors='coerce')
            df_alertas_chart = self.df_estoque[q <= n].copy()
            if not df_alertas_chart.empty:
                df_alertas_chart['gap'] = pd.to_numeric(df_alertas_chart['Nivel_Minimo_Estoque'], errors='coerce') - pd.to_numeric(df_alertas_chart['Quantidade_Estoque'], errors='coerce')
                low = df_alertas_chart[df_alertas_chart['gap'] > 0].sort_values('gap', ascending=False).head(10)
                if not low.empty:
                    low.sort_values('gap', ascending=True).plot(kind='barh', x='Nome_Produto', y='gap', ax=ax2, legend=False, color='#C21807')
        ax2.set_title("Maiores Rupturas de Estoque (Gap)", color=text_color)
        ax2.set_ylabel("")
        ax2.tick_params(axis='x', colors=text_color); ax2.tick_params(axis='y', colors=text_color)
        self.canvas_baixo = FigureCanvas(fig2); self.layout_baixo.addWidget(self.canvas_baixo)