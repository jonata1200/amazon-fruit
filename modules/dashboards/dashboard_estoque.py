# modules/dashboards/dashboard_estoque.py

import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QFrame, QTableView, QTabWidget
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from modules.ui.qt_utils import (
    set_table_from_df,
    set_table_with_conditional_formatting
)
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency

class DashboardEstoque(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name
        self.df_estoque = pd.DataFrame()
        self.df_alertas = pd.DataFrame() # DataFrame para os alertas

        # KPIs
        self.kpi_produtos = None
        self.kpi_valor_estoque = None
        self.kpi_baixo = None
        self.kpi_compra_urgente = None # Novo KPI

        # Widgets da UI
        self.table_alertas = None   # Tabela para alertas
        self.table_completo = None  # Tabela para inventário completo
        self.canvas_categoria = None
        self.canvas_baixo = None
        self.layout_categoria = None
        self.layout_baixo = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,20,20,20); root.setSpacing(16)
        title = QLabel("Estoque: Painel de Controle"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)

        # Grade de KPIs com 4 colunas
        kpi_grid = QGridLayout(); kpi_grid.setSpacing(16)
        self.kpi_produtos = KPIWidget("📦 Produtos Únicos")
        self.kpi_valor_estoque = KPIWidget("💰 Valor do Estoque (Custo)")
        self.kpi_baixo = KPIWidget("⚠️ Itens em Alerta")
        self.kpi_compra_urgente = KPIWidget("🛒 Compra Urgente (Custo)") # Novo KPI

        kpi_grid.addWidget(self.kpi_produtos, 0, 0)
        kpi_grid.addWidget(self.kpi_valor_estoque, 0, 1)
        kpi_grid.addWidget(self.kpi_baixo, 0, 2)
        kpi_grid.addWidget(self.kpi_compra_urgente, 0, 3) # Adicionado à grade
        root.addLayout(kpi_grid)

        # Sistema de Abas para as tabelas
        tab_widget = QTabWidget()
        self.table_alertas = QTableView()
        self.table_completo = QTableView()
        
        tab_widget.addTab(self.table_alertas, "🚨 Alertas de Estoque")
        tab_widget.addTab(self.table_completo, "📋 Inventário Completo")
        root.addWidget(tab_widget)

        # Gráficos (mesma estrutura)
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
        # Carrega o DataFrame principal
        self.df_estoque = self.data_handler.load_table("Estoque")
        if self.df_estoque is None or self.df_estoque.empty:
            self.df_estoque = pd.DataFrame()
            self.df_alertas = pd.DataFrame()
            return
        
        # Cria o DataFrame de alertas a partir do principal
        q = pd.to_numeric(self.df_estoque['Quantidade_Estoque'], errors='coerce')
        n = pd.to_numeric(self.df_estoque['Nivel_Minimo_Estoque'], errors='coerce')
        self.df_alertas = self.df_estoque[q <= n].copy()


    def _rebuild_kpis(self):
        df = self.df_estoque
        
        # KPIs antigos
        total = int(df['ID_Produto'].nunique()) if 'ID_Produto' in df.columns else 0
        q = pd.to_numeric(df.get('Quantidade_Estoque'), errors='coerce').fillna(0)
        c = pd.to_numeric(df.get('Preco_Custo'), errors='coerce').fillna(0.0)
        valor = float((q * c).sum())
        
        # KPI 'Itens em Alerta' agora usa o df_alertas
        baixo = len(self.df_alertas)

        # Lógica para o novo KPI "Compra Urgente"
        valor_compra_urgente = 0.0
        if not self.df_alertas.empty:
            df_a = self.df_alertas
            q_a = pd.to_numeric(df_a['Quantidade_Estoque'], errors='coerce').fillna(0)
            n_a = pd.to_numeric(df_a['Nivel_Minimo_Estoque'], errors='coerce').fillna(0)
            c_a = pd.to_numeric(df_a['Preco_Custo'], errors='coerce').fillna(0.0)
            
            # Calcula a diferença necessária para atingir o mínimo e o custo disso
            gap = n_a - q_a
            valor_compra_urgente = float((gap * c_a).sum())

        self.kpi_produtos.setValue(str(total))
        self.kpi_valor_estoque.setValue(fmt_currency(valor))
        self.kpi_baixo.setValue(str(baixo))
        self.kpi_compra_urgente.setValue(fmt_currency(valor_compra_urgente))

    def _format_df_for_display(self, df_original: pd.DataFrame):
        """Função auxiliar para evitar repetição de código de formatação."""
        if df_original is None or df_original.empty:
            return pd.DataFrame()

        df = df_original.copy()
        
        # Formatar datas e valores
        if "Data_Validade" in df.columns:
            df["Data_Validade"] = pd.to_datetime(df["Data_Validade"], errors="coerce").dt.strftime("%d/%m/%Y")
        for col in ["Preco_Custo", "Preco_Venda"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).map(fmt_currency)

        # Ocultar colunas e Renomear cabeçalhos
        df = df.drop(columns=[c for c in ["ID_Produto", "ID_Fornecedor"] if c in df.columns], errors='ignore')
        rename_map = {
            "Nome_Produto": "Nome do Produto", "Categoria": "Categoria",
            "Quantidade_Estoque": "Quantidade em Estoque", "Nivel_Minimo_Estoque": "Nível Mínimo de Estoque",
            "Preco_Custo": "Preço de Custo", "Preco_Venda": "Preço de Venda", "Data_Validade": "Data de Validade",
        }
        df = df.rename(columns=rename_map)

        return df

    def _rebuild_tables(self):
        # --- Tabela de Alertas ---
        df_alertas_display = self.df_alertas.copy()
        if not df_alertas_display.empty:
            # Adiciona a coluna "Gap" para ser exibida na tabela de alertas
            q = pd.to_numeric(df_alertas_display['Quantidade_Estoque'], errors='coerce').fillna(0)
            n = pd.to_numeric(df_alertas_display['Nivel_Minimo_Estoque'], errors='coerce').fillna(0)
            df_alertas_display['Gap'] = n - q

        df_alertas_fmt = self._format_df_for_display(df_alertas_display)
        
        # Reordena colunas para a tabela de alertas, priorizando o Gap
        if 'Gap' in df_alertas_fmt.columns:
            cols_order = ['Nome do Produto', 'Gap', 'Quantidade em Estoque', 'Nível Mínimo de Estoque', 'Categoria', 'Preço de Custo']
            existing_cols = [c for c in cols_order if c in df_alertas_fmt.columns]
            df_alertas_fmt = df_alertas_fmt[existing_cols]
        
        # A tabela de alertas não precisa de formatação condicional, pois todos são vermelhos por definição
        set_table_from_df(self.table_alertas, df_alertas_fmt)


        # --- Tabela de Inventário Completo ---
        df_completo_fmt = self._format_df_for_display(self.df_estoque)
        set_table_with_conditional_formatting(self.table_completo, df_completo_fmt)

    def _rebuild_charts(self):
        if self.canvas_categoria: self.layout_categoria.removeWidget(self.canvas_categoria); self.canvas_categoria.setParent(None); self.canvas_categoria=None
        if self.canvas_baixo: self.layout_baixo.removeWidget(self.canvas_baixo); self.canvas_baixo.setParent(None); self.canvas_baixo=None

        # Cores baseadas no tema
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#1C1C1C' if self.theme_name == 'dark' else '#FFFFFF'

        # --- Gráfico 1: Valor de Estoque por Categoria (Barras) ---
        fig1 = Figure(figsize=(5.2, 3.2), dpi=100); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)

        if not self.df_estoque.empty and {'Categoria', 'Quantidade_Estoque', 'Preco_Custo'}.issubset(self.df_estoque.columns):
            dfx = self.df_estoque.copy()
            dfx['Valor_Total'] = pd.to_numeric(dfx['Quantidade_Estoque'], errors='coerce') * pd.to_numeric(dfx['Preco_Custo'], errors='coerce')
            valor_por_cat = dfx.groupby('Categoria')['Valor_Total'].sum().sort_values(ascending=True)
            if not valor_por_cat.empty:
                valor_por_cat.plot(kind='barh', ax=ax1, color='#FF8C00')

        ax1.set_title("Valor de Estoque por Categoria", color=text_color)
        ax1.tick_params(axis='x', colors=text_color)
        ax1.tick_params(axis='y', colors=text_color)
        for spine in ax1.spines.values():
            spine.set_color(text_color)
        fig1.tight_layout()
        self.canvas_categoria = FigureCanvas(fig1); self.layout_categoria.addWidget(self.canvas_categoria)

        # --- Gráfico 2: Maiores Rupturas de Estoque (Gap) ---
        fig2 = Figure(figsize=(5.6, 3.2), dpi=100); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        
        if not self.df_alertas.empty:
            dfx_a = self.df_alertas.copy()
            dfx_a['gap'] = pd.to_numeric(dfx_a['Nivel_Minimo_Estoque'], errors='coerce') - pd.to_numeric(dfx_a['Quantidade_Estoque'], errors='coerce')
            low = dfx_a[dfx_a['gap'] > 0].sort_values('gap', ascending=False).head(10)
            if not low.empty:
                ax2.barh(low['Nome_Produto'].astype(str), low['gap']); ax2.invert_yaxis()
        
        ax2.set_title("Maiores Rupturas de Estoque (Gap)", color=text_color)
        ax2.tick_params(axis='x', colors=text_color)
        ax2.tick_params(axis='y', colors=text_color)
        for spine in ax2.spines.values():
            spine.set_color(text_color)
        fig2.tight_layout()
        self.canvas_baixo = FigureCanvas(fig2); self.layout_baixo.addWidget(self.canvas_baixo)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()