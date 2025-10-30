# modules/dashboards/dashboard_recursos_humanos.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class DashboardRecursosHumanos(QWidget):
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

        self.df_rh = self.data_handler.get_dataframe('Recursos_Humanos')
        
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        title_label = QLabel("Dashboard de Recursos Humanos")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        self.main_layout.addWidget(title_label)
        
        kpi_layout = QHBoxLayout()
        total_funcionarios = len(self.df_rh)
        custo_mensal_total = self.df_rh['Salario'].sum()
        kpi_layout.addWidget(self._create_kpi_box("Total de Funcionários", f"{total_funcionarios}"))
        kpi_layout.addWidget(self._create_kpi_box("Custo Mensal da Equipe", f"R$ {custo_mensal_total:,.2f}"))
        self.main_layout.addLayout(kpi_layout)
        
        content_layout = QHBoxLayout()
        content_layout.addWidget(self._create_employee_table())
        content_layout.addWidget(self._create_salary_chart())
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

    def _create_employee_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.df_rh.columns))
        table.setRowCount(len(self.df_rh))
        table.setHorizontalHeaderLabels(self.df_rh.columns)
        for i, row in self.df_rh.iterrows():
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))
        
        # --- LINHA ALTERADA ---
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