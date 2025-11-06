# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel,
    QTableView, QTabWidget, QHeaderView
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

from modules.ui.qt_utils import df_to_model
from modules.ui.widgets.kpi_widget import KPIWidget
from modules.utils.formatters import fmt_currency
# --- MUDANÇA 1: Importar a nova função de análise ---
from modules.analysis.financial_analysis import (
    calculate_financial_summary,
    get_expense_distribution,
    get_revenue_distribution
)

class DashboardFinancas(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_financas = pd.DataFrame()
        self.kpi_receita, self.kpi_despesas, self.kpi_lucro, self.kpi_margem_lucro = None, None, None, None
        self.table_extrato = None

        # --- MUDANÇA 2: Inicializar variáveis para o novo gráfico ---
        self.canvas_evolucao, self.canvas_top_despesas, self.canvas_top_receitas = None, None, None
        self.layout_evolucao, self.layout_top_despesas = QVBoxLayout(), QVBoxLayout()
        self.layout_top_receitas = QVBoxLayout() # Novo layout

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20, 20, 20, 20); root.setSpacing(16)
        title = QLabel("Dashboard Financeiro"); title.setStyleSheet("font-size: 24px; font-weight: bold;"); root.addWidget(title)
        
        kpi_layout = QGridLayout(); kpi_layout.setSpacing(16)
        self.kpi_receita = KPIWidget("Receita Total", value_color="#2E8B57"); self.kpi_despesas = KPIWidget("Despesas Totais", value_color="#C21807")
        self.kpi_lucro = KPIWidget("Lucro Líquido", value_color="#FF8C00"); self.kpi_margem_lucro = KPIWidget("Margem de Lucro", value_color="#6A0DAD")
        kpi_layout.addWidget(self.kpi_receita, 0, 0); kpi_layout.addWidget(self.kpi_despesas, 0, 1)
        kpi_layout.addWidget(self.kpi_lucro, 0, 2); kpi_layout.addWidget(self.kpi_margem_lucro, 0, 3)
        root.addLayout(kpi_layout)
        
        tab_widget = QTabWidget()
        evolucao_widget = QWidget(); evolucao_widget.setLayout(self.layout_evolucao)
        tab_widget.addTab(evolucao_widget, "📈 Evolução Mensal")

        top_despesas_widget = QWidget(); top_despesas_widget.setLayout(self.layout_top_despesas)
        tab_widget.addTab(top_despesas_widget, "📊 Top Despesas")

        # --- MUDANÇA 3: Adicionar a nova aba para o gráfico de receitas ---
        top_receitas_widget = QWidget(); top_receitas_widget.setLayout(self.layout_top_receitas)
        tab_widget.addTab(top_receitas_widget, "💰 Top Receitas")

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
        # Este método não precisa de alterações
        s = calculate_financial_summary(self.df_financas); receita = s.get('receita', 0.0); lucro = s.get('lucro', 0.0); margem = (lucro / receita) * 100 if receita > 0 else 0.0
        self.kpi_receita.setValue(fmt_currency(receita)); self.kpi_despesas.setValue(fmt_currency(s.get('despesa', 0.0))); self.kpi_lucro.setValue(fmt_currency(lucro)); self.kpi_margem_lucro.setValue(f"{margem:.1f}%")

    def _rebuild_tables(self):
        # Este método não precisa de alterações
        df = self.df_financas.copy()
        if df is None or df.empty: self.table_extrato.setModel(None); return
        if "Data" in df.columns: df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime('%d/%m/%Y')
        if "Valor" in df.columns: df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0).apply(fmt_currency)
        rename_map = {"Data": "Data", "Tipo": "Tipo", "Categoria": "Categoria", "Descricao": "Descrição", "Valor": "Valor", "Forma de Pagamento": "Forma de Pagamento"}
        df = df.rename(columns=rename_map)
        cols_to_show = ["Data", "Tipo", "Categoria", "Descrição", "Valor", "Forma de Pagamento"]; df_display = df[[col for col in cols_to_show if col in df.columns]]
        model = df_to_model(df_display); self.table_extrato.setModel(model); self.table_extrato.setAlternatingRowColors(True); header = self.table_extrato.horizontalHeader()
        if header.count() > 0:
            try:
                desc_index = df_display.columns.get_loc("Descrição")
                for i in range(header.count()): header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch if i == desc_index else QHeaderView.ResizeMode.ResizeToContents)
            except KeyError: header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _rebuild_charts(self):
        # --- MUDANÇA 4: Adicionar limpeza e lógica de plotagem para o novo gráfico ---
        if self.canvas_evolucao: self.layout_evolucao.removeWidget(self.canvas_evolucao); self.canvas_evolucao.deleteLater(); self.canvas_evolucao = None
        if self.canvas_top_despesas: self.layout_top_despesas.removeWidget(self.canvas_top_despesas); self.canvas_top_despesas.deleteLater(); self.canvas_top_despesas = None
        if self.canvas_top_receitas: self.layout_top_receitas.removeWidget(self.canvas_top_receitas); self.canvas_top_receitas.deleteLater(); self.canvas_top_receitas = None

        text_color = 'black'; bg_color = '#FFFFFF'
        
        # Gráfico 1: Evolução Mensal (sem alterações)
        fig1 = Figure(tight_layout=True); fig1.patch.set_facecolor(bg_color); ax1 = fig1.add_subplot(111); ax1.set_facecolor(bg_color)
        df = self.df_financas.copy()
        if not df.empty and 'Data' in df.columns:
            df['MesAno'] = pd.to_datetime(df['Data'], errors='coerce').dt.to_period('M').astype(str); monthly = df.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0); monthly['Lucro'] = monthly.get('Receita', 0) - monthly.get('Despesa', 0)
            if 'Receita' not in monthly: monthly['Receita'] = 0;
            if 'Despesa' not in monthly: monthly['Despesa'] = 0;
            monthly[['Receita', 'Despesa']].plot(kind='bar', ax=ax1, color=['#2E8B57', '#C21807']); ax1_lucro = ax1.twinx(); monthly['Lucro'].plot(kind='line', ax=ax1_lucro, color='#FF8C00', marker='o')
            ax1.set_title("Evolução Financeira Mensal", color=text_color);
        self.canvas_evolucao = FigureCanvas(fig1); self.layout_evolucao.addWidget(self.canvas_evolucao)
        
        # Gráfico 2: Top 5 Despesas (sem alterações)
        fig2 = Figure(tight_layout=True); fig2.patch.set_facecolor(bg_color); ax2 = fig2.add_subplot(111); ax2.set_facecolor(bg_color)
        ser_exp = get_expense_distribution(self.df_financas).head(5)
        if not ser_exp.empty: ser_exp.sort_values().plot(kind='barh', ax=ax2, color='#C21807')
        ax2.set_title("Top 5 Despesas por Categoria", color=text_color)
        self.canvas_top_despesas = FigureCanvas(fig2); self.layout_top_despesas.addWidget(self.canvas_top_despesas)

        # Gráfico 3: Top 5 Receitas (NOVO)
        fig3 = Figure(tight_layout=True); fig3.patch.set_facecolor(bg_color); ax3 = fig3.add_subplot(111); ax3.set_facecolor(bg_color)
        ser_rev = get_revenue_distribution(self.df_financas, top_n=5)
        if not ser_rev.empty:
            # Usa a cor verde, consistente com o KPI de Receita
            ser_rev.sort_values().plot(kind='barh', ax=ax3, color='#2E8B57')
        ax3.set_title("Top 5 Receitas por Categoria", color=text_color)
        self.canvas_top_receitas = FigureCanvas(fig3); self.layout_top_receitas.addWidget(self.canvas_top_receitas)