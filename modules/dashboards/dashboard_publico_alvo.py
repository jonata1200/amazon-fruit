# modules/dashboards/dashboard_publico_alvo.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class DashboardPublicoAlvo(QWidget):
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

        self.df_clientes = self.data_handler.get_dataframe('Publico_Alvo')
        
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        title_label = QLabel("Dashboard de Público-Alvo")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        self.main_layout.addWidget(title_label)
        
        kpi_layout = QHBoxLayout()
        total_clientes = len(self.df_clientes)
        idade_media = self.df_clientes['Idade'].mean()
        gasto_medio_total = self.df_clientes['Gasto_Medio'].mean()
        kpi_layout.addWidget(self._create_kpi_box("Total de Clientes", f"{total_clientes}"))
        kpi_layout.addWidget(self._create_kpi_box("Idade Média", f"{idade_media:.1f} anos"))
        kpi_layout.addWidget(self._create_kpi_box("Gasto Médio por Cliente", f"R$ {gasto_medio_total:,.2f}"))
        self.main_layout.addLayout(kpi_layout)
        
        content_layout = QHBoxLayout()
        content_layout.addWidget(self._create_customer_table())
        charts_layout = QVBoxLayout()
        charts_layout.addWidget(self._create_location_chart())
        charts_layout.addWidget(self._create_gender_chart())
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

    def _create_customer_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.df_clientes.columns))
        table.setRowCount(len(self.df_clientes))
        table.setHorizontalHeaderLabels(self.df_clientes.columns)
        for i, row in self.df_clientes.iterrows():
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))
        
        # --- LINHA ALTERADA ---
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    # ... (_create_location_chart e _create_gender_chart permanecem os mesmos) ...
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