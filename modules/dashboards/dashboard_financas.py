# modules/dashboards/dashboard_financas.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class DashboardFinancas(QWidget):
    # ... (__init__, build_ui, update_theme, _create_kpi_box permanecem os mesmos) ...
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name
        self.main_layout = QVBoxLayout(self)
        self.build_ui()

    def build_ui(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.df_financas = self.data_handler.get_dataframe('Financas')
        
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        title_label = QLabel("Dashboard Financeiro")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        self.main_layout.addWidget(title_label)
        
        kpi_layout = QHBoxLayout()
        entradas = self.df_financas[self.df_financas['Tipo'] == 'Entrada']['Valor'].sum()
        saidas = self.df_financas[self.df_financas['Tipo'] == 'Saída']['Valor'].sum()
        lucro_liquido = entradas - saidas
        kpi_layout.addWidget(self._create_kpi_box("Receita Total", f"R$ {entradas:,.2f}", '#2E8B57'))
        kpi_layout.addWidget(self._create_kpi_box("Despesas Totais", f"R$ {saidas:,.2f}", '#C21807'))
        kpi_layout.addWidget(self._create_kpi_box("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", '#FF8C00'))
        self.main_layout.addLayout(kpi_layout)
        
        content_layout = QHBoxLayout()
        content_layout.addWidget(self._create_transactions_table())
        charts_layout = QVBoxLayout()
        charts_layout.addWidget(self._create_revenue_vs_expenses_chart(entradas, saidas))
        charts_layout.addWidget(self._create_expenses_pie_chart())
        content_layout.addLayout(charts_layout)
        self.main_layout.addLayout(content_layout)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self.build_ui()

    def _create_kpi_box(self, title, value, value_color=None):
        kpi_frame = QFrame()
        kpi_frame.setObjectName("KPIFrame") # Define o nome do objeto para o estilo global
        
        layout = QVBoxLayout(kpi_frame)
        title_label = QLabel(title)
        title_label.setObjectName("KPITitleLabel") # Define o nome do objeto
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setObjectName("KPIValueLabel") # Define o nome do objeto
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Se uma cor específica for passada (ex: para lucro/despesa),
        # aplica-a como um estilo 'in-line' que sobrescreve apenas a cor.
        if value_color:
            value_label.setStyleSheet(f"color: {value_color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return kpi_frame

    def _create_transactions_table(self):
        df_sorted = self.df_financas.sort_values(by='Data', ascending=False)
        table = QTableWidget()
        table.setColumnCount(len(df_sorted.columns))
        table.setRowCount(len(df_sorted))
        table.setHorizontalHeaderLabels(df_sorted.columns)
        for i, row in df_sorted.iterrows():
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        # --- LINHA ALTERADA ---
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    # ... (_create_revenue_vs_expenses_chart e _create_expenses_pie_chart permanecem os mesmos) ...
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