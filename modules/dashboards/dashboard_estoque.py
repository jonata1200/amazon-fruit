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

from modules.analysis.financial_analysis import get_top_selling_items
from modules.analysis.inventory_analysis import get_low_stock_items

class DashboardEstoque(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_estoque = pd.DataFrame()
        self.df_financas = pd.DataFrame()

        self.kpi_produtos = None; self.kpi_valor_estoque = None; self.kpi_baixo = None; self.kpi_compra_urgente = None
        self.table_inventario = None
        self.canvas_top_vendidos = None
        self.layout_top_vendidos = QVBoxLayout()
        self.canvas_ruptura = None
        self.layout_ruptura = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Dashboard de Estoque"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)
        kpi_grid = QGridLayout(); kpi_grid.setSpacing(16)
        self.kpi_produtos = KPIWidget("📦 Produtos Únicos"); self.kpi_valor_estoque = KPIWidget("💰 Valor do Estoque (Custo)")
        self.kpi_baixo = KPIWidget("⚠️ Itens em Alerta"); self.kpi_compra_urgente = KPIWidget("🛒 Compra Urgente (Custo)")
        kpi_grid.addWidget(self.kpi_produtos, 0, 0); kpi_grid.addWidget(self.kpi_valor_estoque, 0, 1); kpi_grid.addWidget(self.kpi_baixo, 0, 2); kpi_grid.addWidget(self.kpi_compra_urgente, 0, 3)
        root.addLayout(kpi_grid)
        main_tab_widget = QTabWidget()
        top_vendidos_widget = QWidget(); top_vendidos_widget.setLayout(self.layout_top_vendidos)
        main_tab_widget.addTab(top_vendidos_widget, "🏆 Top Produtos Vendidos")
        ruptura_widget = QWidget(); ruptura_widget.setLayout(self.layout_ruptura)
        main_tab_widget.addTab(ruptura_widget, "📉 Maiores Rupturas")
        self.table_inventario = QTableView(); main_tab_widget.addTab(self.table_inventario, "📋 Inventário Completo")
        root.addWidget(main_tab_widget)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_estoque = self.data_handler.load_table("Estoque")
        self.df_financas = self.data_handler.load_table("Financas")

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

    # --- CORREÇÃO APLICADA AQUI ---
    def _format_df_for_display(self, df_original: pd.DataFrame):
        # A lógica de verificação foi separada em um bloco if claro.
        if df_original is None or df_original.empty:
            return pd.DataFrame()
        
        # A cópia do DataFrame agora é feita com segurança.
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
        if self.canvas_top_vendidos: self.layout_top_vendidos.removeWidget(self.canvas_top_vendidos); self.canvas_top_vendidos.deleteLater(); self.canvas_top_vendidos = None
        if self.canvas_ruptura: self.layout_ruptura.removeWidget(self.canvas_ruptura); self.canvas_ruptura.deleteLater(); self.canvas_ruptura = None
        text_color = 'black'; bg_color = '#FFFFFF'
        
        fig1 = Figure(tight_layout=True); fig1.patch.set_facecolor(bg_color); ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        ser_prod = get_top_selling_items(self.df_financas, self.df_estoque, top_n=10)
        if not ser_prod.empty:
            ser_prod.sort_values().plot(kind='barh', ax=ax1, color='#2ECC71')
        ax1.set_title("Top 10 Produtos por Faturamento de Vendas", color=text_color); ax1.set_ylabel(""); ax1.set_xlabel("Valor Total Vendido (R$)", color=text_color)
        ax1.tick_params(axis='x', colors=text_color); ax1.tick_params(axis='y', colors=text_color)
        self.canvas_top_vendidos = FigureCanvas(fig1); self.layout_top_vendidos.addWidget(self.canvas_top_vendidos)
        
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color); ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        df_ruptura = get_low_stock_items(self.df_estoque, top_n=10)
        if not df_ruptura.empty:
            df_ruptura.sort_values('gap', ascending=True).plot(kind='barh', x='Nome_Produto', y='gap', ax=ax2, legend=False, color='#E74C3C')
        ax2.set_title("Maiores Rupturas de Estoque (Gap)", color=text_color); ax2.set_ylabel("")
        ax2.tick_params(axis='x', colors=text_color); ax2.tick_params(axis='y', colors=text_color)
        self.canvas_ruptura = FigureCanvas(fig2); self.layout_ruptura.addWidget(self.canvas_ruptura)