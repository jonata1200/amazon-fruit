# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import pandas as pd
from modules.ui.qt_utils import set_table_from_df

# Classe inteligente para ordenação numérica
class CustomTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except (ValueError, TypeError):
            return super().__lt__(other)

class DashboardFinancas(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_content_widget = None
        self.build_ui()

    def build_ui(self):
        if self.central_content_widget:
            self.central_content_widget.deleteLater()
        self.central_content_widget = QWidget()
        content_layout = QVBoxLayout(self.central_content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        self.df_financas = self.data_handler.get_dataframe('Financas')
        title_label = QLabel("Dashboard Financeiro")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        content_layout.addWidget(title_label)
        kpi_layout = QHBoxLayout()
        entradas = self.df_financas[self.df_financas['Tipo'] == 'Entrada']['Valor'].sum()
        saidas = self.df_financas[self.df_financas['Tipo'] == 'Saída']['Valor'].sum()
        lucro_liquido = entradas - saidas
        kpi_layout.addWidget(self._create_kpi_box("Receita Total", f"R$ {entradas:,.2f}", '#2E8B57'))
        kpi_layout.addWidget(self._create_kpi_box("Despesas Totais", f"R$ {saidas:,.2f}", '#C21807'))
        kpi_layout.addWidget(self._create_kpi_box("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", '#FF8C00'))
        content_layout.addLayout(kpi_layout)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self._create_transactions_table())
        charts_layout = QVBoxLayout()
        charts_layout.addWidget(self._create_revenue_vs_expenses_chart(entradas, saidas))
        charts_layout.addWidget(self._create_expenses_pie_chart())
        bottom_layout.addLayout(charts_layout)
        content_layout.addLayout(bottom_layout)
        self.main_layout.addWidget(self.central_content_widget)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self.build_ui()

    def _create_kpi_box(self, title, value, value_color=None):
        kpi_frame = QFrame()
        kpi_frame.setObjectName("KPIFrame")
        layout = QVBoxLayout(kpi_frame)
        title_label = QLabel(title)
        title_label.setObjectName("KPITitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label = QLabel(value)
        value_label.setObjectName("KPIValueLabel")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if value_color:
            value_label.setStyleSheet(f"color: {value_color};")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return kpi_frame

    def _create_transactions_table(self):
        df_sorted = self.df_financas.sort_values(by='Data', ascending=False)
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(len(df_sorted.columns))
        table.setRowCount(len(df_sorted))
        table.setHorizontalHeaderLabels(df_sorted.columns)
        for i, row in df_sorted.iterrows():
            for j, value in enumerate(row):
                item = CustomTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def _create_revenue_vs_expenses_chart(self, revenue, expenses):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.bar(['Receita', 'Despesas'], [revenue, expenses], color=['#2E8B57', '#C21807'])
        ax.set_title('Receita vs. Despesas', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(bg_color)
        fig.tight_layout()
        return FigureCanvas(fig)

    def _create_expenses_pie_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        df_saidas = self.df_financas[self.df_financas['Tipo'] == 'Saída']
        expense_counts = df_saidas.groupby('Categoria')['Valor'].sum()
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.pie(expense_counts, labels=expense_counts.index, autopct='%1.1f%%', textprops={'color': text_color})
        ax.set_title('Distribuição de Despesas', color=text_color)
        fig.tight_layout()
        return FigureCanvas(fig)
    
    def _reload_data(self):
        self.df_fin = self.data_handler.load_table("Financas")

    def _rebuild_kpis(self):
        df = self.df_fin
        receita = despesa = 0.0
        if {'Valor','Tipo'}.issubset(df.columns):
            t = df['Tipo'].astype(str).str.lower()
            v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
            receita = float(v[t.str.startswith('entrada')].sum())
            despesa = float(v[t.str.startswith('saída')].sum())
        lucro = receita - despesa
        self.kpi_receita.setText(f"R$ {receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.kpi_despesa.setText(f"R$ {despesa:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.kpi_lucro.setText(f"R$ {lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    def _rebuild_tables(self):
        set_table_from_df(self.table_financas, self.df_fin)

    def _rebuild_charts(self):
        # Receita vs. Despesa (barras)
        if hasattr(self, "canvas_revexp"):
            self.layout_revexp.removeWidget(self.canvas_revexp)
            self.canvas_revexp.setParent(None)
        fig1 = Figure(figsize=(6, 3), dpi=100); ax1 = fig1.add_subplot(111)
        receita = despesa = 0.0
        if {'Valor','Tipo'}.issubset(self.df_fin.columns):
            t = self.df_fin['Tipo'].astype(str).str.lower()
            v = pd.to_numeric(self.df_fin['Valor'], errors='coerce').fillna(0.0)
            receita = float(v[t.str.startswith('entrada')].sum())
            despesa = float(v[t.str.startswith('saída')].sum())
        ax1.bar(['Receita','Despesas'], [receita, despesa], color=['#2E8B57','#D62728'])
        ax1.set_title("Receita vs. Despesas")
        self.canvas_revexp = FigureCanvas(fig1); self.layout_revexp.addWidget(self.canvas_revexp)

        # Pizza de despesas por categoria
        if hasattr(self, "canvas_pie"):
            self.layout_pie.removeWidget(self.canvas_pie)
            self.canvas_pie.setParent(None)
        fig2 = Figure(figsize=(5, 3), dpi=100); ax2 = fig2.add_subplot(111)
        ok = {'Categoria','Tipo','Valor'}.issubset(self.df_fin.columns)
        if ok:
            dd = self.df_fin[self.df_fin['Tipo'].astype(str).str.lower().str.startswith('saída')]
            s = dd.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)
            if not s.empty:
                ax2.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Distribuição de Despesas")
        self.canvas_pie = FigureCanvas(fig2); self.layout_pie.addWidget(self.canvas_pie)

        # Série temporal (entradas - saídas)
        if hasattr(self, "canvas_ts"):
            self.layout_ts.removeWidget(self.canvas_ts)
            self.canvas_ts.setParent(None)
        fig3 = Figure(figsize=(6.2, 3), dpi=100); ax3 = fig3.add_subplot(111)
        if {'Data','Valor','Tipo'}.issubset(self.df_fin.columns):
            dfx = self.df_fin.copy()
            dfx['Data'] = pd.to_datetime(dfx['Data'], errors='coerce'); dfx = dfx.dropna(subset=['Data'])
            dfx['signed'] = dfx.apply(lambda r: r['Valor'] if str(r.get('Tipo','')).lower().startswith('entrada')
                                    else -abs(r['Valor']), axis=1)
            daily = dfx.groupby('Data')['signed'].sum().sort_index()
            if not daily.empty:
                ax3.plot(daily.index, daily.values, marker='o')
        ax3.set_title("Fluxo Diário (Entradas - Saídas)")
        self.canvas_ts = FigureCanvas(fig3); self.layout_ts.addWidget(self.canvas_ts)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()