# modules/dashboards/dashboard_estoque.py

import pandas as pd
import matplotlib.pyplot as plt  # <-- MUDANÇA AQUI

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QTableView, QTabWidget, QHeaderView
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from modules.ui.qt_utils import set_table_with_conditional_formatting
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from .chart_generator import (
    create_top_selling_chart,
    create_least_selling_chart,
    create_stock_rupture_chart
)

class DashboardEstoque(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_estoque = pd.DataFrame()
        self.df_estoque_completo = pd.DataFrame()
        self.df_financas = pd.DataFrame()

        self.kpi_produtos = None; self.kpi_valor_estoque = None; self.kpi_baixo = None; self.kpi_compra_urgente = None
        self.table_inventario = None
        
        self.canvas_top_vendidos = None; self.layout_top_vendidos = QVBoxLayout()
        self.canvas_menos_vendidos = None; self.layout_menos_vendidos = QVBoxLayout()
        self.canvas_ruptura = None; self.layout_ruptura = QVBoxLayout()

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
        kpi_grid.addWidget(self.kpi_produtos, 0, 0)
        kpi_grid.addWidget(self.kpi_valor_estoque, 0, 1)
        kpi_grid.addWidget(self.kpi_baixo, 0, 2)
        kpi_grid.addWidget(self.kpi_compra_urgente, 0, 3)
        root.addLayout(kpi_grid)
        
        main_tab_widget = QTabWidget()
        top_vendidos_widget = QWidget(); top_vendidos_widget.setLayout(self.layout_top_vendidos)
        main_tab_widget.addTab(top_vendidos_widget, "🏆 Top Produtos Vendidos")
        menos_vendidos_widget = QWidget(); menos_vendidos_widget.setLayout(self.layout_menos_vendidos)
        main_tab_widget.addTab(menos_vendidos_widget, "📉 Produtos Menos Vendidos")
        ruptura_widget = QWidget(); ruptura_widget.setLayout(self.layout_ruptura)
        main_tab_widget.addTab(ruptura_widget, "⚠️ Maiores Rupturas")
        self.table_inventario = QTableView(); main_tab_widget.addTab(self.table_inventario, "📋 Inventário Completo")
        root.addWidget(main_tab_widget)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")
        self.df_estoque_completo = self.data_handler.load_full_unfiltered_table("Estoque")
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
        
        # --- MUDANÇAS APLICADAS AQUI ---

        # 1. Formata as colunas de data para o formato DD/MM/YYYY
        if "Data_Validade" in df.columns: 
            df["Data_Validade"] = pd.to_datetime(df["Data_Validade"], errors="coerce").dt.strftime("%d/%m/%Y")
        if "Data_Venda" in df.columns:
            df["Data_Venda"] = pd.to_datetime(df["Data_Venda"], errors="coerce").dt.strftime("%d/%m/%Y")

        # Formata colunas de moeda
        for col in ["Preco_Custo", "Preco_Venda"]:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).map(fmt_currency)
        
        # Remove colunas técnicas que não precisam ser exibidas
        cols_to_drop = ["ID_Produto", "ID_Fornecedor", "Ano", "Mes", "Data_Snapshot"]
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
        
        # 2. Renomeia as colunas para nomes mais amigáveis, incluindo as novas
        rename_map = {
            "Produto": "Produto",  # Corrigido de "Nome_Produto"
            "Categoria": "Categoria", 
            "Quantidade_Estoque": "Estoque Atual", 
            "Nivel_Minimo_Estoque": "Estoque Mínimo", 
            "Preco_Custo": "Preço de Custo", 
            "Preco_Venda": "Preço de Venda", 
            "Data_Validade": "Data de Validade",
            "Quantidade_Vendida": "Vendas", # Novo nome
            "Data_Venda": "Data da Venda"   # Novo nome
        }
        df = df.rename(columns=rename_map)
        
        return df

    def _rebuild_tables(self):
        df_completo_fmt = self._format_df_for_display(self.df_estoque)
        set_table_with_conditional_formatting(self.table_inventario, df_completo_fmt)

        # --- NOVA LÓGICA DE REDIMENSIONAMENTO INTELIGENTE ---
        if df_completo_fmt is None or df_completo_fmt.empty:
            return

        header = self.table_inventario.horizontalHeader()
        
        # Define quais colunas devem se esticar para preencher o espaço
        stretch_columns = ["Produto", "Categoria"]
        
        # Itera sobre todas as colunas no DataFrame que está sendo exibido
        for i, column_name in enumerate(df_completo_fmt.columns):
            if column_name in stretch_columns:
                # Estas colunas (Produto, Categoria) dividem o espaço restante
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                # Todas as outras colunas (numéricas, datas) se ajustam ao seu conteúdo
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

    def _rebuild_charts(self):
        if self.canvas_top_vendidos: self.layout_top_vendidos.removeWidget(self.canvas_top_vendidos); self.canvas_top_vendidos.deleteLater(); self.canvas_top_vendidos = None
        if self.canvas_menos_vendidos: self.layout_menos_vendidos.removeWidget(self.canvas_menos_vendidos); self.canvas_menos_vendidos.deleteLater(); self.canvas_menos_vendidos = None
        if self.canvas_ruptura: self.layout_ruptura.removeWidget(self.canvas_ruptura); self.canvas_ruptura.deleteLater(); self.canvas_ruptura = None
        
        # Gráfico 1: Top Produtos Vendidos
        fig1 = create_top_selling_chart(self.df_financas, self.df_estoque_completo)
        self.canvas_top_vendidos = FigureCanvas(fig1)
        self.layout_top_vendidos.addWidget(self.canvas_top_vendidos)
        plt.close(fig1)  # <-- MUDANÇA AQUI

        # Gráfico 2: Produtos Menos Vendidos
        fig2 = create_least_selling_chart(self.df_financas, self.df_estoque_completo)
        self.canvas_menos_vendidos = FigureCanvas(fig2)
        self.layout_menos_vendidos.addWidget(self.canvas_menos_vendidos)
        plt.close(fig2)  # <-- MUDANÇA AQUI
        
        # Gráfico 3: Maiores Rupturas
        fig3 = create_stock_rupture_chart(self.df_estoque)
        self.canvas_ruptura = FigureCanvas(fig3)
        self.layout_ruptura.addWidget(self.canvas_ruptura)
        plt.close(fig3)  # <-- MUDANÇA AQUI