# modules/dashboards/dashboard_recursos_humanos.py

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

class DashboardRecursosHumanos(QWidget):
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
        self.df_rh = self.data_handler.get_dataframe('Recursos_Humanos')
        title_label = QLabel("Dashboard de Recursos Humanos")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        content_layout.addWidget(title_label)
        kpi_layout = QHBoxLayout()
        total_funcionarios = len(self.df_rh)
        custo_mensal_total = self.df_rh['Salario'].sum()
        kpi_layout.addWidget(self._create_kpi_box("Total de Funcionários", f"{total_funcionarios}"))
        kpi_layout.addWidget(self._create_kpi_box("Custo Mensal da Equipe", f"R$ {custo_mensal_total:,.2f}"))
        content_layout.addLayout(kpi_layout)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self._create_employee_table())
        bottom_layout.addWidget(self._create_salary_chart())
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

    def _create_employee_table(self):
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(len(self.df_rh.columns))
        table.setRowCount(len(self.df_rh))
        table.setHorizontalHeaderLabels(self.df_rh.columns)
        for i, row in self.df_rh.iterrows():
            for j, value in enumerate(row):
                item = CustomTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def _create_salary_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        df_sorted = self.df_rh.sort_values('Salario', ascending=False)
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.bar(df_sorted['Nome_Funcionario'], df_sorted['Salario'], color='#4B0082')
        ax.set_title('Salários por Funcionário', color=text_color)
        ax.tick_params(axis='x', colors=text_color, rotation=45, labelsize=8)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(bg_color)
        fig.tight_layout()
        return FigureCanvas(fig)
    
    def _reload_data(self):
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        total = len(self.df_rh)
        custo = 0.0
        if 'Salario' in self.df_rh:
            custo = float(pd.to_numeric(self.df_rh['Salario'], errors='coerce').fillna(0.0).sum())
        self.kpi_total_func.setText(str(total))
        self.kpi_custo_mensal.setText(f"R$ {custo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    def _rebuild_tables(self):
        set_table_from_df(self.table_rh, self.df_rh)

    def _rebuild_charts(self):
        # Salários por funcionário
        if hasattr(self, "canvas_sal"):
            self.layout_sal.removeWidget(self.canvas_sal); self.canvas_sal.setParent(None)
        fig = Figure(figsize=(6.2, 3.2), dpi=100); ax = fig.add_subplot(111)
        req = {'Nome_Funcionario','Salario'}
        if req.issubset(self.df_rh.columns):
            dfx = self.df_rh.copy()
            dfx['Salario'] = pd.to_numeric(dfx['Salario'], errors='coerce')
            dfx = dfx.dropna(subset=['Salario'])
            if not dfx.empty:
                ax.bar(dfx['Nome_Funcionario'].astype(str), dfx['Salario'], color='#4B0082')
                ax.tick_params(axis='x', rotation=25)
        ax.set_title("Salários por Funcionário")
        self.canvas_sal = FigureCanvas(fig); self.layout_sal.addWidget(self.canvas_sal)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()