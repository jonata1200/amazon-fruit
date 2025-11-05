# modules/dashboards/dashboard_geral.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QFileDialog, QMessageBox
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

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
        """
        Altera o tipo e as cores do gráfico para corresponder ao estilo do dashboard de Finanças.
        """
        if self.canvas_crescimento: self.layout_crescimento.removeWidget(self.canvas_crescimento); self.canvas_crescimento.deleteLater(); self.canvas_crescimento = None
        
        text_color = 'black'
        bg_color = '#FFFFFF'
        
        fig = Figure(figsize=(10, 6), tight_layout=True); fig.patch.set_facecolor(bg_color); ax1 = fig.add_subplot(111); ax1.set_facecolor(bg_color)

        df_fin = self.df_financas.copy()
        if not df_fin.empty and 'Data' in df_fin.columns:
            df_fin['MesAno'] = pd.to_datetime(df_fin['Data'], errors='coerce').dt.to_period('M').astype(str)
            monthly = df_fin.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
            if 'Receita' not in monthly: monthly['Receita'] = 0
            if 'Despesa' not in monthly: monthly['Despesa'] = 0
            monthly['Lucro'] = monthly['Receita'] - monthly['Despesa']
            
            # --- MUDANÇA APLICADA AQUI ---
            # O código hexadecimal foi alterado para um laranja mais escuro.
            cor_faturamento = '#E67E22'  # Laranja Escuro (antes era '#FFA500')
            cor_lucro = '#006400'      # Verde Escuro (permanece o mesmo)

            ax1.bar(monthly.index, monthly['Receita'], color=cor_faturamento, label='Faturamento (Receita)', width=0.8)
            ax1.set_xlabel("Mês/Ano", color=text_color)
            ax1.set_ylabel("Faturamento (R$)", color=cor_faturamento)
            ax1.tick_params(axis='y', labelcolor=cor_faturamento)
            ax1.tick_params(axis='x', rotation=45, labelsize=10)

            ax2 = ax1.twinx()
            ax2.plot(monthly.index, monthly['Lucro'], color=cor_lucro, marker='o', linestyle='-', label='Lucro Líquido')
            ax2.set_ylabel("Lucro (R$)", color=cor_lucro)
            ax2.tick_params(axis='y', labelcolor=cor_lucro)

            fig.suptitle("Evolução Mensal: Faturamento vs. Lucro", fontsize=16, color=text_color)
            
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc='upper right')

        self.canvas_crescimento = FigureCanvas(fig)
        self.layout_crescimento.addWidget(self.canvas_crescimento)

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