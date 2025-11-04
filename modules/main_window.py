# modules/main_window.py

from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QFrame, QStackedWidget, QApplication
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from .app_styles import get_stylesheet
from modules.ui.widgets.period_bar import PeriodBar
from modules.utils.data_handler import DataHandler

from .dashboards.dashboard_geral import DashboardGeral
from .dashboards.dashboard_estoque import DashboardEstoque
from .dashboards.dashboard_financas import DashboardFinancas
from .dashboards.dashboard_publico_alvo import DashboardPublicoAlvo
from .dashboards.dashboard_fornecedores import DashboardFornecedores
from .dashboards.dashboard_recursos_humanos import DashboardRecursosHumanos
from .dashboards.dashboard_insights import DashboardInsights

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app

        # --- Janela/tema ---
        self.setWindowTitle("Amazon Fruit")
        self.setGeometry(100, 100, 1280, 720)
        self.app.setStyleSheet(get_stylesheet()) # Aplica o tema claro padrão

        # --- Data handler ---
        data_dir = Path(__file__).resolve().parents[1] / "data"
        self.data_handler = DataHandler(base_dir=data_dir)

        # --- Layout principal ---
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0); main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== Navegação (esquerda) =====
        nav_frame = QFrame()
        nav_frame.setObjectName("NavFrame")
        nav_frame.setMaximumWidth(220)
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        nav_layout.setContentsMargins(10, 10, 10, 10); nav_layout.setSpacing(15)

        # Logo e Botões
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        logo_label.setPixmap(pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(logo_label); nav_layout.addSpacing(20)

        self.btn_geral = self.create_nav_button("Visão Geral")
        self.btn_estoque = self.create_nav_button("Estoque")
        self.btn_financas = self.create_nav_button("Finanças")
        self.btn_publico_alvo = self.create_nav_button("Público-Alvo")
        self.btn_fornecedores = self.create_nav_button("Fornecedores")
        self.btn_rh = self.create_nav_button("Recursos Humanos")
        self.btn_insights = self.create_nav_button("Insights")

        nav_layout.addWidget(self.btn_geral); nav_layout.addWidget(self.btn_estoque)
        nav_layout.addWidget(self.btn_financas); nav_layout.addWidget(self.btn_publico_alvo)
        nav_layout.addWidget(self.btn_fornecedores); nav_layout.addWidget(self.btn_rh)
        nav_layout.addWidget(self.btn_insights)
        nav_layout.addStretch()

        # ===== Conteúdo (direita) =====
        self.content_stack = QStackedWidget()

        # Instância dos dashboards (NÃO precisa mais passar o tema)
        self.dash_geral = DashboardGeral(self.data_handler)
        self.dash_estoque = DashboardEstoque(self.data_handler)
        self.dash_financas = DashboardFinancas(self.data_handler)
        self.dash_publico_alvo = DashboardPublicoAlvo(self.data_handler)
        self.dash_fornecedores = DashboardFornecedores(self.data_handler)
        self.dash_rh = DashboardRecursosHumanos(self.data_handler)
        self.dash_insights = DashboardInsights(self.data_handler)

        self.content_stack.addWidget(self.dash_geral); self.content_stack.addWidget(self.dash_estoque)
        self.content_stack.addWidget(self.dash_financas); self.content_stack.addWidget(self.dash_publico_alvo)
        self.content_stack.addWidget(self.dash_fornecedores); self.content_stack.addWidget(self.dash_rh)
        self.content_stack.addWidget(self.dash_insights)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0); right_layout.setSpacing(0)

        self.period_bar = PeriodBar(on_apply=self._on_period_apply)
        right_layout.addWidget(self.period_bar)
        right_layout.addWidget(self.content_stack)

        # Conexões dos botões
        self.btn_geral.clicked.connect(self.switch_to_geral)
        self.btn_estoque.clicked.connect(self.switch_to_estoque)
        self.btn_financas.clicked.connect(self.switch_to_financas)
        self.btn_publico_alvo.clicked.connect(self.switch_to_publico_alvo)
        self.btn_fornecedores.clicked.connect(self.switch_to_fornecedores)
        self.btn_rh.clicked.connect(self.switch_to_rh)
        self.btn_insights.clicked.connect(self.switch_to_insights)

        # Estado inicial
        self.btn_geral.setChecked(True)
        self.content_stack.setCurrentWidget(self.dash_geral)

        # Montagem final
        main_layout.addWidget(nav_frame)
        main_layout.addWidget(right_panel)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        return btn

    def update_button_states(self, clicked_button):
        all_buttons = [
            self.btn_geral, self.btn_estoque, self.btn_financas,
            self.btn_publico_alvo, self.btn_fornecedores, self.btn_rh, self.btn_insights
        ]
        for b in all_buttons:
            if b is not clicked_button:
                b.setChecked(False)

    def _on_period_apply(self, start_iso: str, end_iso: str):
        if not hasattr(self, "data_handler") or self.data_handler is None:
            data_dir = Path(__file__).resolve().parents[1] / "data"
            self.data_handler = DataHandler(base_dir=data_dir)
        if hasattr(self.data_handler, "set_period"):
            self.data_handler.set_period(start_iso, end_iso)
        for dash in self._dashboards():
            if hasattr(dash, "refresh"):
                dash.refresh()

    def _dashboards(self):
        return [
            self.dash_geral, self.dash_estoque, self.dash_financas,
            self.dash_publico_alvo, self.dash_fornecedores, self.dash_rh,
            self.dash_insights
        ]

    # Funções de troca de dashboards (permanecem iguais)
    def switch_to_geral(self): self.content_stack.setCurrentWidget(self.dash_geral); self.update_button_states(self.btn_geral)
    def switch_to_estoque(self): self.content_stack.setCurrentWidget(self.dash_estoque); self.update_button_states(self.btn_estoque)
    def switch_to_financas(self): self.content_stack.setCurrentWidget(self.dash_financas); self.update_button_states(self.btn_financas)
    def switch_to_publico_alvo(self): self.content_stack.setCurrentWidget(self.dash_publico_alvo); self.update_button_states(self.btn_publico_alvo)
    def switch_to_fornecedores(self): self.content_stack.setCurrentWidget(self.dash_fornecedores); self.update_button_states(self.btn_fornecedores)
    def switch_to_rh(self): self.content_stack.setCurrentWidget(self.dash_rh); self.update_button_states(self.btn_rh)
    def switch_to_insights(self): self.content_stack.setCurrentWidget(self.dash_insights); self.update_button_states(self.btn_insights)