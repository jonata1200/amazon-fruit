# modules/dashboards/dashboard_publico_alvo.py

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

class DashboardPublicoAlvo(QWidget):
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
        self.df_clientes = self.data_handler.get_dataframe('Publico_Alvo')
        title_label = QLabel("Dashboard de Público-Alvo")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        content_layout.addWidget(title_label)
        kpi_layout = QHBoxLayout()
        total_clientes = len(self.df_clientes)
        idade_media = self.df_clientes['Idade'].mean()
        gasto_medio_total = self.df_clientes['Gasto_Medio'].mean()
        kpi_layout.addWidget(self._create_kpi_box("Total de Clientes", f"{total_clientes}"))
        kpi_layout.addWidget(self._create_kpi_box("Idade Média", f"{idade_media:.1f} anos"))
        kpi_layout.addWidget(self._create_kpi_box("Gasto Médio por Cliente", f"R$ {gasto_medio_total:,.2f}"))
        content_layout.addLayout(kpi_layout)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self._create_customer_table())
        charts_layout = QVBoxLayout()
        charts_layout.addWidget(self._create_location_chart())
        charts_layout.addWidget(self._create_gender_chart())
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

    def _create_customer_table(self):
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(len(self.df_clientes.columns))
        table.setRowCount(len(self.df_clientes))
        table.setHorizontalHeaderLabels(self.df_clientes.columns)
        for i, row in self.df_clientes.iterrows():
            for j, value in enumerate(row):
                item = CustomTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def _create_location_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        location_counts = self.df_clientes['Localizacao'].value_counts()
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.bar(location_counts.index, location_counts.values, color='#4B0082')
        ax.set_title('Distribuição de Clientes por Localização', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(bg_color)
        fig.tight_layout()
        return FigureCanvas(fig)

    def _create_gender_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        gender_counts = self.df_clientes['Genero'].value_counts()
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', textprops={'color': text_color}, colors=['#FF8C00', '#2E8B57'])
        ax.set_title('Distribuição por Gênero', color=text_color)
        fig.tight_layout()
        return FigureCanvas(fig)
    
    def _reload_data(self):
        self.df_pub = self.data_handler.load_table("Publico_Alvo")

    def _rebuild_kpis(self):
        total = len(self.df_pub)
        idade_media = float(pd.to_numeric(self.df_pub.get('Idade'), errors='coerce').mean()) \
                    if 'Idade' in self.df_pub else float('nan')
        gasto_medio = float(pd.to_numeric(self.df_pub.get('Gasto_Medio'), errors='coerce').mean()) \
                    if 'Gasto_Medio' in self.df_pub else float('nan')
        self.kpi_total.setText(str(total))
        self.kpi_idade.setText(f"{idade_media:.1f} anos" if not math.isnan(idade_media) else "—")
        self.kpi_ticket.setText("R$ " + (f"{gasto_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                                if not math.isnan(gasto_medio) else "—")

    def _rebuild_tables(self):
        set_table_from_df(self.table_publico, self.df_pub)

    def _rebuild_charts(self):
        # Localização (barras)
        if hasattr(self, "canvas_loc"):
            self.layout_loc.removeWidget(self.canvas_loc); self.canvas_loc.setParent(None)
        fig1 = Figure(figsize=(6, 3), dpi=100); ax1 = fig1.add_subplot(111)
        if 'Localizacao' in self.df_pub:
            s = self.df_pub['Localizacao'].astype(str).value_counts()
            if not s.empty:
                ax1.bar(s.index, s.values, color='#4B0082'); ax1.tick_params(axis='x', rotation=15)
        ax1.set_title("Distribuição de Clientes por Localização")
        self.canvas_loc = FigureCanvas(fig1); self.layout_loc.addWidget(self.canvas_loc)

        # Gênero (pizza)
        if hasattr(self, "canvas_gender"):
            self.layout_gender.removeWidget(self.canvas_gender); self.canvas_gender.setParent(None)
        fig2 = Figure(figsize=(5, 3), dpi=100); ax2 = fig2.add_subplot(111)
        if 'Genero' in self.df_pub:
            s = self.df_pub['Genero'].astype(str).value_counts()
            if not s.empty:
                ax2.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Distribuição por Gênero")
        self.canvas_gender = FigureCanvas(fig2); self.layout_gender.addWidget(self.canvas_gender)

    def refresh(self):
        self._reload_data(); self._rebuild_kpis(); self._rebuild_tables(); self._rebuild_charts()