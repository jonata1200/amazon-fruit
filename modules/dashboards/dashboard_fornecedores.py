# modules/dashboards/dashboard_fornecedores.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import pandas as pd
from modules.ui.qt_utils import set_table_from_df
import math

# Classe inteligente para ordenação numérica
class CustomTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except (ValueError, TypeError):
            return super().__lt__(other)

class DashboardFornecedores(QWidget):
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
        self.df_fornecedores = self.data_handler.get_dataframe('Fornecedores')
        title_label = QLabel("Dashboard de Fornecedores")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        content_layout.addWidget(title_label)
        kpi_layout = QHBoxLayout()
        total_fornecedores = len(self.df_fornecedores)
        avaliacao_media = self.df_fornecedores['Avaliacao'].mean()
        kpi_layout.addWidget(self._create_kpi_box("Total de Fornecedores", f"{total_fornecedores}"))
        kpi_layout.addWidget(self._create_kpi_box("Avaliação Média", f"{avaliacao_media:.1f} / 5 ★"))
        content_layout.addLayout(kpi_layout)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self._create_supplier_table())
        charts_layout = QVBoxLayout()
        charts_layout.addWidget(self._create_rating_chart())
        charts_layout.addWidget(self._create_products_supplied_chart())
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

    def _create_supplier_table(self):
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(len(self.df_fornecedores.columns))
        table.setRowCount(len(self.df_fornecedores))
        table.setHorizontalHeaderLabels(self.df_fornecedores.columns)
        for i, row in self.df_fornecedores.iterrows():
            for j, value in enumerate(row):
                item = CustomTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def _create_rating_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        df_sorted = self.df_fornecedores.sort_values('Avaliacao', ascending=True)
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.barh(df_sorted['Nome_Fornecedor'], df_sorted['Avaliacao'], color='#2E8B57')
        ax.set_title('Avaliação dos Fornecedores', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(bg_color)
        fig.tight_layout()
        return FigureCanvas(fig)

    def _create_products_supplied_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        product_series = self.df_fornecedores['Produtos_Fornecidos'].str.split(', ').explode().value_counts()
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.pie(product_series, labels=product_series.index, autopct='%1.1f%%', textprops={'color': text_color})
        ax.set_title('Tipos de Produtos Fornecidos', color=text_color)
        fig.tight_layout()
        return FigureCanvas(fig)
    
    def _reload_data(self):
        self.df_forn = self.data_handler.load_table("Fornecedores")

    def _rebuild_kpis(self):
        total = len(self.df_forn)
        aval = float(pd.to_numeric(self.df_forn.get('Avaliacao'), errors='coerce').mean()) \
            if 'Avaliacao' in self.df_forn else float('nan')
        self.kpi_total_forn.setText(str(total))
        self.kpi_media.setText(f"{aval:.1f} / 5 ★" if not math.isnan(aval) else "—")

    def _rebuild_tables(self):
        set_table_from_df(self.table_fornecedores, self.df_forn)

    def _rebuild_charts(self):
        # Avaliação (barra horizontal)
        if hasattr(self, "canvas_rate"):
            self.layout_rate.removeWidget(self.canvas_rate); self.canvas_rate.setParent(None)
        fig1 = Figure(figsize=(6.2, 3), dpi=100); ax1 = fig1.add_subplot(111)
        if {'Nome_Fornecedor','Avaliacao'}.issubset(self.df_forn.columns):
            dfx = self.df_forn.copy()
            dfx['Avaliacao'] = pd.to_numeric(dfx['Avaliacao'], errors='coerce')
            dfx = dfx.dropna(subset=['Avaliacao'])
            if not dfx.empty:
                ax1.barh(dfx['Nome_Fornecedor'].astype(str), dfx['Avaliacao'], color='#2E8B57')
                ax1.set_xlim(0, 5); ax1.invert_yaxis()
        ax1.set_title("Avaliação dos Fornecedores")
        self.canvas_rate = FigureCanvas(fig1); self.layout_rate.addWidget(self.canvas_rate)

        # Tipos de produtos (pizza)
        if hasattr(self, "canvas_types"):
            self.layout_types.removeWidget(self.canvas_types); self.canvas_types.setParent(None)
        fig2 = Figure(figsize=(5.2, 3), dpi=100); ax2 = fig2.add_subplot(111)
        if 'Produtos_Fornecidos' in self.df_forn:
            all_types = []
            for x in self.df_forn['Produtos_Fornecidos'].dropna().astype(str):
                all_types += [t.strip() for t in x.split(',')]
            import pandas as pd
            s = pd.Series(all_types).value_counts()
            if not s.empty:
                ax2.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Tipos de Produtos Fornecidos")
        self.canvas_types = FigureCanvas(fig2); self.layout_types.addWidget(self.canvas_types)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()