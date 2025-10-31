# modules/dashboards/dashboard_geral.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from ..report_generator import ReportGenerator

class DashboardGeral(QWidget):
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

        # Recarrega os dados
        self.df_financas = self.data_handler.get_dataframe('Financas')
        self.df_estoque = self.data_handler.get_dataframe('Estoque')
        self.df_clientes = self.data_handler.get_dataframe('Publico_Alvo')
        self.df_rh = self.data_handler.get_dataframe('Recursos_Humanos')

        header_layout = QHBoxLayout()
        title_label = QLabel("Visão Geral do Negócio")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        
        export_button = QPushButton("📄 Gerar Relatório Completo")
        export_button.setObjectName("ActionButton")
        export_button.clicked.connect(self.export_full_report)
        export_button.setFixedWidth(220) 

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(export_button)
        content_layout.addLayout(header_layout)

        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)
        entradas = self.df_financas[self.df_financas['Tipo'] == 'Entrada']['Valor'].sum()
        saidas = self.df_financas[self.df_financas['Tipo'] == 'Saída']['Valor'].sum()
        lucro_liquido = entradas - saidas
        kpi_grid.addWidget(self._create_kpi_box("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", '#FF8C00'), 0, 0)
        kpi_grid.addWidget(self._create_kpi_box("Receita Total", f"R$ {entradas:,.2f}", '#2E8B57'), 0, 1)
        itens_estoque_baixo = self.df_estoque[self.df_estoque['Quantidade_Estoque'] <= self.df_estoque['Nivel_Minimo_Estoque']].shape[0]
        valor_total_custo = (self.df_estoque['Preco_Custo'] * self.df_estoque['Quantidade_Estoque']).sum()
        kpi_grid.addWidget(self._create_kpi_box("Itens com Estoque Baixo", f"{itens_estoque_baixo}", '#C21807'), 1, 0)
        kpi_grid.addWidget(self._create_kpi_box("Valor do Estoque", f"R$ {valor_total_custo:,.2f}"), 1, 1)
        total_clientes = len(self.df_clientes)
        total_funcionarios = len(self.df_rh)
        kpi_grid.addWidget(self._create_kpi_box("Total de Clientes", f"{total_clientes}"), 0, 2)
        kpi_grid.addWidget(self._create_kpi_box("Total de Funcionários", f"{total_funcionarios}"), 1, 2)
        content_layout.addLayout(kpi_grid)
        content_layout.addWidget(self._create_revenue_vs_expenses_chart(entradas, saidas), 1)

        self.main_layout.addWidget(self.central_content_widget)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self.build_ui()

    def export_full_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório Completo", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                report_gen = ReportGenerator(self.data_handler)
                report_gen.generate_report(file_path)
                QMessageBox.information(self, "Sucesso", f"Relatório completo salvo com sucesso em:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o relatório:\n{e}")

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

    def _create_revenue_vs_expenses_chart(self, revenue, expenses):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.bar(['Receita', 'Despesas'], [revenue, expenses], color=['#2E8B57', '#C21807'])
        ax.set_title('Resumo Financeiro do Período', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(bg_color)
        fig.tight_layout()
        return FigureCanvas(fig)