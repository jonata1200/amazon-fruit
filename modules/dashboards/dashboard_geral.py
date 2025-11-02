# modules/dashboards/dashboard_geral.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import pandas as pd

from ..report.report_generator import ReportGenerator


class DashboardGeral(QWidget):
    """
    Visão geral do negócio:
    - KPIs principais (lucro, receita, estoque, clientes, funcionários)
    - Gráfico Receita vs. Despesas
    Compatível com período global definido no DataHandler (set_period).
    """
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name

        # DataFrames
        self.df_financas = pd.DataFrame()
        self.df_estoque = pd.DataFrame()
        self.df_clientes = pd.DataFrame()
        self.df_rh = pd.DataFrame()

        # Widgets de KPI
        self.kpi_lucro = None
        self.kpi_receita = None
        self.kpi_baixo = None
        self.kpi_valor_estoque = None
        self.kpi_total_clientes = None
        self.kpi_total_funcionarios = None

        # Canvas do gráfico
        self.canvas_revexp = None

        # Layout raiz
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Monta UI estática e faz primeira carga
        self._build_ui()
        self.refresh()

    # ---------------------------------------------------------------------
    # UI
    # ---------------------------------------------------------------------
    def _build_ui(self):
        self.central_content_widget = QWidget()
        content_layout = QVBoxLayout(self.central_content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Visão Geral do Negócio")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")

        export_button = QPushButton("📄 Gerar Relatório")
        export_button.setObjectName("ActionButton")
        export_button.clicked.connect(self.export_full_report)
        export_button.setFixedWidth(220)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(export_button)
        content_layout.addLayout(header_layout)

        # KPIs (placeholders — valores definidos em _rebuild_kpis)
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)

        self.kpi_lucro = self._create_kpi_box("Lucro Líquido")
        self.kpi_receita = self._create_kpi_box("Receita Total", value_color="#2E8B57")
        self.kpi_baixo = self._create_kpi_box("Itens com Estoque Baixo", value_color="#C21807")
        self.kpi_valor_estoque = self._create_kpi_box("Valor do Estoque")
        self.kpi_total_clientes = self._create_kpi_box("Total de Clientes")
        self.kpi_total_funcionarios = self._create_kpi_box("Total de Funcionários")

        kpi_grid.addWidget(self.kpi_lucro,              0, 0)
        kpi_grid.addWidget(self.kpi_receita,            0, 1)
        kpi_grid.addWidget(self.kpi_total_clientes,     0, 2)
        kpi_grid.addWidget(self.kpi_baixo,              1, 0)
        kpi_grid.addWidget(self.kpi_valor_estoque,      1, 1)
        kpi_grid.addWidget(self.kpi_total_funcionarios, 1, 2)

        content_layout.addLayout(kpi_grid)

        # Área do gráfico (o canvas é criado em _rebuild_charts)
        self.chart_holder = QFrame()
        self.chart_holder_layout = QVBoxLayout(self.chart_holder)
        self.chart_holder_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.chart_holder)

        self.main_layout.addWidget(self.central_content_widget)

    # ---------------------------------------------------------------------
    # Ações
    # ---------------------------------------------------------------------
    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self._rebuild_charts()

    def export_full_report(self):
        # Nome padrão inclui o período atual (se houver)
        period = getattr(self.data_handler, "get_period", lambda: None)()
        suffix = f"_{period[0]}_a_{period[1]}" if period else ""
        default_name = f"Relatorio_Amazon_Fruit{suffix}.pdf"

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Relatório Completo", default_name, "PDF Files (*.pdf)"
        )
        if not file_path:
            return
        try:
            report = ReportGenerator(self.data_handler)
            report.generate_report(file_path)
            QMessageBox.information(self, "Sucesso", f"Relatório salvo em:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o relatório:\n{e}")

    # ---------------------------------------------------------------------
    # Ciclo de atualização
    # ---------------------------------------------------------------------
    def refresh(self):
        """Recarrega dados + KPIs + gráfico respeitando o período atual."""
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_charts()

    def _reload_data(self):
        """Lê as tabelas já filtradas por período (se definido no DataHandler)."""
        # IMPORTANTe: use load_table (period-aware) e não get_dataframe
        self.df_financas = self.data_handler.load_table("Financas")
        self.df_estoque = self.data_handler.load_table("Estoque")
        self.df_clientes = self.data_handler.load_table("Publico_Alvo")
        self.df_rh = self.data_handler.load_table("Recursos_Humanos")

    def _rebuild_kpis(self):
        """Recalcula e escreve os KPIs na tela."""
        # Receita/Despesa/Lucro
        receita, despesa = 0.0, 0.0
        if not self.df_financas.empty and {'Valor', 'Tipo'}.issubset(self.df_financas.columns):
            t = self.df_financas['Tipo'].astype(str).str.lower()
            v = pd.to_numeric(self.df_financas['Valor'], errors='coerce').fillna(0.0)
            receita = float(v[t.str.startswith('entrada')].sum())
            despesa = float(v[t.str.startswith('saída')].sum())
        lucro = receita - despesa

        # Estoque — itens abaixo do mínimo e valor total de custo
        baixo = 0
        valor_total_custo = 0.0
        if not self.df_estoque.empty:
            if {'Quantidade_Estoque', 'Nivel_Minimo_Estoque'}.issubset(self.df_estoque.columns):
                q = pd.to_numeric(self.df_estoque['Quantidade_Estoque'], errors='coerce')
                n = pd.to_numeric(self.df_estoque['Nivel_Minimo_Estoque'], errors='coerce')
                baixo = int((q <= n).sum())
            if {'Quantidade_Estoque', 'Preco_Custo'}.issubset(self.df_estoque.columns):
                q2 = pd.to_numeric(self.df_estoque['Quantidade_Estoque'], errors='coerce').fillna(0)
                c2 = pd.to_numeric(self.df_estoque['Preco_Custo'], errors='coerce').fillna(0.0)
                valor_total_custo = float((q2 * c2).sum())

        # Clientes/Funcionários
        total_clientes = int(len(self.df_clientes)) if self.df_clientes is not None else 0
        total_funcionarios = int(len(self.df_rh)) if self.df_rh is not None else 0

        # Escreve nos cartões
        self._set_kpi_value(self.kpi_lucro,            self._fmt_currency(lucro))
        self._set_kpi_value(self.kpi_receita,          self._fmt_currency(receita), color="#2E8B57")
        self._set_kpi_value(self.kpi_baixo,            str(baixo),                  color="#C21807")
        self._set_kpi_value(self.kpi_valor_estoque,    self._fmt_currency(valor_total_custo))
        self._set_kpi_value(self.kpi_total_clientes,   str(total_clientes))
        self._set_kpi_value(self.kpi_total_funcionarios, str(total_funcionarios))

    def _rebuild_charts(self):
        """Desenha/atualiza o gráfico Receita vs Despesas."""
        # limpa canvas antigo
        if self.canvas_revexp is not None:
            self.chart_holder_layout.removeWidget(self.canvas_revexp)
            self.canvas_revexp.setParent(None)
            self.canvas_revexp = None

        # calcula dados do gráfico
        receita, despesa = 0.0, 0.0
        if not self.df_financas.empty and {'Valor', 'Tipo'}.issubset(self.df_financas.columns):
            t = self.df_financas['Tipo'].astype(str).str.lower()
            v = pd.to_numeric(self.df_financas['Valor'], errors='coerce').fillna(0.0)
            receita = float(v[t.str.startswith('entrada')].sum())
            despesa = float(v[t.str.startswith('saída')].sum())

        # cores por tema
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'

        # figura
        fig = Figure(figsize=(5.8, 3.6), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        ax.bar(['Receita', 'Despesas'], [receita, despesa], color=['#2E8B57', '#C21807'])
        ax.set_title('Resumo Financeiro do Período', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        for spine in ['bottom', 'left', 'right', 'top']:
            ax.spines[spine].set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.grid(axis='y', color='#999999', alpha=0.25)

        fig.tight_layout()
        self.canvas_revexp = FigureCanvas(fig)
        self.chart_holder_layout.addWidget(self.canvas_revexp)

    # ---------------------------------------------------------------------
    # Helpers de UI
    # ---------------------------------------------------------------------
    def _create_kpi_box(self, title, value_color=None):
        box = QFrame()
        box.setObjectName("KPIFrame")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 10, 12, 10)

        title_label = QLabel(title)
        title_label.setObjectName("KPITitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_label = QLabel("—")
        value_label.setObjectName("KPIValueLabel")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if value_color:
            value_label.setStyleSheet(f"color: {value_color};")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        # devolve o frame, mas guardamos o label de valor dentro do próprio frame
        box._value_label = value_label
        return box

    def _set_kpi_value(self, kpi_frame: QFrame, text: str, color: str | None = None):
        if not hasattr(kpi_frame, "_value_label"):
            return
        if color:
            kpi_frame._value_label.setStyleSheet(f"color: {color};")
        kpi_frame._value_label.setText(text)

    @staticmethod
    def _fmt_currency(v):
        try:
            return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return "R$ 0,00"