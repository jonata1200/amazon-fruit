# modules/dashboards/dashboard_geral.py

import pandas as pd
import matplotlib.pyplot as plt  # <-- MUDANÇA AQUI

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QFileDialog, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from .chart_generator import create_general_evolution_chart
from ..report.report_generator import ReportGenerator

class DashboardGeral(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.df_financas = pd.DataFrame()
        self.canvas_crescimento = None
        self.layout_crescimento = QVBoxLayout()

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(20, 20, 20, 20); root.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Visão Geral do Negócio"); title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #000000;")
        export_button = QPushButton("📄 Gerar Relatório"); export_button.setObjectName("ActionButton"); export_button.clicked.connect(self.export_full_report); export_button.setFixedWidth(220)
        header_layout.addWidget(title_label); header_layout.addStretch(); header_layout.addWidget(export_button)
        root.addLayout(header_layout)
        chart_frame = QFrame(); chart_frame.setLayout(self.layout_crescimento)
        root.addWidget(chart_frame)

    def refresh(self):
        self._reload_data()
        self._rebuild_charts()

    def _reload_data(self):
        self.df_financas = self.data_handler.load_table("Financas")

    def _rebuild_charts(self):
        if self.canvas_crescimento:
            self.layout_crescimento.removeWidget(self.canvas_crescimento)
            self.canvas_crescimento.deleteLater()
            self.canvas_crescimento = None
        
        fig = create_general_evolution_chart(self.df_financas)
        
        self.canvas_crescimento = FigureCanvas(fig)
        self.layout_crescimento.addWidget(self.canvas_crescimento)
        plt.close(fig) # <-- MUDANÇA AQUI

    def export_full_report(self):
        period = self.data_handler.get_period(); start, end = (period[0], period[1]) if period and len(period) >= 2 else (None, None)
        suffix = f"_{start.replace('/','')}_a_{end.replace('/','')}" if (start and end) else ""; default_name = f"Relatorio_Geral_Amazon_Fruit{suffix}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório", default_name, "PDF Files (*.pdf)")
        if not file_path: return
        try:
            report = ReportGenerator(self.data_handler); report.generate_report(file_path)
            QMessageBox.information(self, "Sucesso", f"Relatório salvo com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o relatório:\n{e}")