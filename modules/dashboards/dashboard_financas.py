# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableView, QTabWidget, QGridLayout
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import set_table_from_df
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
from modules.analysis.financial_analysis import (
    calculate_financial_summary,
    get_expense_distribution
)

class DashboardFinancas(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler

        self.df_financas = pd.DataFrame()
        self.kpi_receita = None
        self.kpi_despesas = None
        self.kpi_lucro = None
        self.kpi_margem_lucro = None

        # Widgets da UI
        self.table_extrato = None
        self.canvas_evolucao = None
        self.canvas_top_despesas = None
        # Layouts que servirão de container para os gráficos
        self.layout_evolucao = QVBoxLayout()
        self.layout_top_despesas = QVBoxLayout()

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20); root.setSpacing(16)

        title = QLabel("Dashboard Financeiro")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        kpi_layout = QGridLayout(); kpi_layout.setSpacing(16)
        self.kpi_receita  = KPIWidget("Receita Total",  value_color="#2E8B57")
        self.kpi_despesas = KPIWidget("Despesas Totais", value_color="#C21807")
        self.kpi_lucro    = KPIWidget("Lucro Líquido",   value_color="#FF8C00")
        self.kpi_margem_lucro = KPIWidget("Margem de Lucro", value_color="#6A0DAD")
        kpi_layout.addWidget(self.kpi_receita, 0, 0)
        kpi_layout.addWidget(self.kpi_despesas, 0, 1)
        kpi_layout.addWidget(self.kpi_lucro, 0, 2)
        kpi_layout.addWidget(self.kpi_margem_lucro, 0, 3)
        root.addLayout(kpi_layout)

        # --- NOVO: Sistema de 3 Abas ---
        tab_widget = QTabWidget()

        # Aba 1: Gráfico de Evolução Mensal
        evolucao_widget = QWidget()
        evolucao_widget.setLayout(self.layout_evolucao) # Usa o layout pré-definido
        tab_widget.addTab(evolucao_widget, "📈 Evolução Mensal")

        # Aba 2: Gráfico de Top Despesas
        top_despesas_widget = QWidget()
        top_despesas_widget.setLayout(self.layout_top_despesas) # Usa o layout pré-definido
        tab_widget.addTab(top_despesas_widget, "📊 Top Despesas")

        # Aba 3: Extrato Detalhado (Tabela)
        self.table_extrato = QTableView()
        tab_widget.addTab(self.table_extrato, "📋 Extrato Detalhado")

        root.addWidget(tab_widget)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")

    def _rebuild_kpis(self):
        s = calculate_financial_summary(self.df_financas)
        receita = s.get('receita', 0.0)
        lucro = s.get('lucro', 0.0)
        margem = (lucro / receita) * 100 if receita > 0 else 0.0
        
        self.kpi_receita.setValue(fmt_currency(receita))
        self.kpi_despesas.setValue(fmt_currency(s.get('despesa', 0.0)))
        self.kpi_lucro.setValue(fmt_currency(lucro))
        self.kpi_margem_lucro.setValue(f"{margem:.1f}%")

    def _rebuild_tables(self):
        df = self.df_financas.copy()
        if df is None or df.empty:
            set_table_from_df(self.table_extrato, pd.DataFrame()); return

        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime('%d/%m/%Y')
        if "Valor" in df.columns:
            df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0).apply(fmt_currency)

        rename_map = {"Data": "Data", "Tipo": "Tipo", "Categoria": "Categoria", "Descricao": "Descrição", "Valor": "Valor", "Metodo_Pagamento": "Forma de Pagto."}
        df = df.rename(columns=rename_map)
        
        cols_to_show = ["Data", "Tipo", "Categoria", "Descrição", "Valor", "Forma de Pagto."]
        existing_cols = [col for col in cols_to_show if col in df.columns]
        
        set_table_from_df(self.table_extrato, df[existing_cols])

    def _rebuild_charts(self):
        # Limpa os canvases antigos se existirem
        if self.canvas_evolucao and self.canvas_evolucao.parent() is not None: self.layout_evolucao.removeWidget(self.canvas_evolucao); self.canvas_evolucao.deleteLater(); self.canvas_evolucao = None
        if self.canvas_top_despesas and self.canvas_top_despesas.parent() is not None: self.layout_top_despesas.removeWidget(self.canvas_top_despesas); self.canvas_top_despesas.deleteLater(); self.canvas_top_despesas = None

        text_color = 'black'
        bg_color = '#FFFFFF'

        # --- Gráfico 1: Evolução Financeira Mensal ---
        fig1 = Figure(tight_layout=True); fig1.patch.set_facecolor(bg_color)
        ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        
        df = self.df_financas.copy()
        if not df.empty and 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df['MesAno'] = df['Data'].dt.to_period('M').astype(str)
            
            monthly = df.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
            monthly['Lucro'] = monthly.get('Receita', 0) - monthly.get('Despesa', 0)
            if 'Receita' not in monthly.columns: monthly['Receita'] = 0
            if 'Despesa' not in monthly.columns: monthly['Despesa'] = 0

            monthly[['Receita', 'Despesa']].plot(kind='bar', ax=ax1, color=['#2E8B57', '#C21807'], width=0.8)
            ax1_lucro = ax1.twinx() # Cria eixo Y secundário para o lucro
            monthly['Lucro'].plot(kind='line', ax=ax1_lucro, color='#FF8C00', marker='o')

            ax1.set_title("Evolução Financeira Mensal", color=text_color)
            ax1.tick_params(axis='x', rotation=45, colors=text_color)
            ax1.tick_params(axis='y', colors=text_color)
            ax1_lucro.tick_params(axis='y', colors='#FF8C00')
            
        self.canvas_evolucao = FigureCanvas(fig1)
        self.layout_evolucao.addWidget(self.canvas_evolucao)

        # --- Gráfico 2: Top 5 Despesas por Categoria ---
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color)
        ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)

        ser = get_expense_distribution(self.df_financas).head(5)
        if not ser.empty:
            ser.sort_values().plot(kind='barh', ax=ax2, color='#C21807')
        
        ax2.set_title("Top 5 Despesas por Categoria", color=text_color)
        ax2.tick_params(axis='x', colors=text_color)
        ax2.tick_params(axis='y', colors=text_color)
        
        self.canvas_top_despesas = FigureCanvas(fig2)
        self.layout_top_despesas.addWidget(self.canvas_top_despesas)