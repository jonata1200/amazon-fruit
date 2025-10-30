# modules/main_window.py

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFrame, QStackedWidget, QApplication)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Módulos da aplicação
from .app_styles import get_stylesheet
from .data_handler import DataHandler
from .dashboards.dashboard_geral import DashboardGeral
from .dashboards.dashboard_estoque import DashboardEstoque
from .dashboards.dashboard_financas import DashboardFinancas
from .dashboards.dashboard_publico_alvo import DashboardPublicoAlvo
from .dashboards.dashboard_fornecedores import DashboardFornecedores
from .dashboards.dashboard_recursos_humanos import DashboardRecursosHumanos

class MainWindow(QMainWindow):
    """
    A classe da janela principal que organiza toda a interface do software,
    incluindo a barra de navegação, a área de conteúdo e a gestão de temas.
    """
    def __init__(self, app: QApplication):
        super().__init__()
        
        self.app = app # Armazena a instância da aplicação para aplicar estilos globais
        self.current_theme = 'dark' # Define o tema inicial

        # --- Configurações da Janela ---
        self.setWindowTitle("Amazon Fruit")
        self.setGeometry(100, 100, 1280, 720)
        self.app.setStyleSheet(get_stylesheet(self.current_theme))

        # Instancia o gerenciador de dados
        self.data_handler = DataHandler()

        # --- Layout Principal (Horizontal) ---
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- 1. Barra de Navegação (Esquerda) ---
        nav_frame = QFrame()
        nav_frame.setObjectName("NavFrame")
        nav_frame.setMaximumWidth(220)
        
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(15)
        
        # Logo da Empresa
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        logo_label.setPixmap(pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(logo_label)
        nav_layout.addSpacing(20)

        # Botões de Navegação dos Dashboards
        self.btn_geral = self.create_nav_button("Visão Geral")
        self.btn_estoque = self.create_nav_button("Estoque")
        self.btn_financas = self.create_nav_button("Finanças")
        self.btn_publico_alvo = self.create_nav_button("Público-Alvo")
        self.btn_fornecedores = self.create_nav_button("Fornecedores")
        self.btn_rh = self.create_nav_button("Recursos Humanos")
        
        nav_layout.addWidget(self.btn_geral)
        nav_layout.addWidget(self.btn_estoque)
        nav_layout.addWidget(self.btn_financas)
        nav_layout.addWidget(self.btn_publico_alvo)
        nav_layout.addWidget(self.btn_fornecedores)
        nav_layout.addWidget(self.btn_rh)
        
        # Espaçador para empurrar o botão de tema para baixo
        nav_layout.addStretch()

        # Botão de Troca de Tema
        self.theme_button = QPushButton("☀️ Tema Claro")
        self.theme_button.setObjectName("ActionButton") # ADICIONE ESTA LINHA
        self.theme_button.clicked.connect(self.toggle_theme)
        nav_layout.addWidget(self.theme_button)

        # --- 2. Área de Conteúdo (Direita) ---
        self.content_stack = QStackedWidget()

        # Instanciação de todos os dashboards, passando o tema atual
        # (Assumindo que todos os dashboards foram atualizados para aceitar 'theme_name')
        self.dash_geral = DashboardGeral(self.data_handler, self.current_theme)
        self.dash_estoque = DashboardEstoque(self.data_handler, self.current_theme)
        self.dash_financas = DashboardFinancas(self.data_handler, self.current_theme)
        self.dash_publico_alvo = DashboardPublicoAlvo(self.data_handler, self.current_theme)
        self.dash_fornecedores = DashboardFornecedores(self.data_handler, self.current_theme)
        self.dash_rh = DashboardRecursosHumanos(self.data_handler, self.current_theme)
        
        # Adicionando os dashboards ao QStackedWidget
        self.content_stack.addWidget(self.dash_geral)
        self.content_stack.addWidget(self.dash_estoque)
        self.content_stack.addWidget(self.dash_financas)
        self.content_stack.addWidget(self.dash_publico_alvo)
        self.content_stack.addWidget(self.dash_fornecedores)
        self.content_stack.addWidget(self.dash_rh)
        
        # Conectando os cliques dos botões às funções de troca de tela
        self.btn_geral.clicked.connect(self.switch_to_geral)
        self.btn_estoque.clicked.connect(self.switch_to_estoque)
        self.btn_financas.clicked.connect(self.switch_to_financas)
        self.btn_publico_alvo.clicked.connect(self.switch_to_publico_alvo)
        self.btn_fornecedores.clicked.connect(self.switch_to_fornecedores)
        self.btn_rh.clicked.connect(self.switch_to_rh)
        
        # Define o estado inicial da aplicação
        self.btn_geral.setChecked(True)
        self.content_stack.setCurrentWidget(self.dash_geral)

        # --- Montagem Final do Layout ---
        main_layout.addWidget(nav_frame)
        main_layout.addWidget(self.content_stack)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_nav_button(self, text):
        """Função auxiliar para criar e configurar os botões de navegação."""
        button = QPushButton(text)
        button.setObjectName("NavButton")
        button.setCheckable(True)
        return button

    def update_button_states(self, clicked_button):
        """Desmarca todos os botões de navegação, exceto o que foi clicado."""
        all_buttons = [self.btn_geral, self.btn_estoque, self.btn_financas, 
                       self.btn_publico_alvo, self.btn_fornecedores, self.btn_rh]
        for button in all_buttons:
            if button is not clicked_button:
                button.setChecked(False)

    def toggle_theme(self):
        """Alterna entre o tema claro e escuro e atualiza a aplicação INTEIRA."""
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            self.theme_button.setText("🌙 Tema Escuro")
        else:
            self.current_theme = 'dark'
            self.theme_button.setText("☀️ Tema Claro")
            
        # Aplica o novo estilo globalmente
        self.app.setStyleSheet(get_stylesheet(self.current_theme))
        
        # --- LÓGICA CORRIGIDA ---
        # Itera por TODOS os dashboards no QStackedWidget e os atualiza.
        for i in range(self.content_stack.count()):
            dashboard = self.content_stack.widget(i)
            if hasattr(dashboard, 'update_theme'):
                dashboard.update_theme(self.current_theme)
    
    # --- Funções para Troca de Dashboards ---
    def switch_to_geral(self):
        self.content_stack.setCurrentWidget(self.dash_geral)
        self.update_button_states(self.btn_geral)

    def switch_to_estoque(self):
        self.content_stack.setCurrentWidget(self.dash_estoque)
        self.update_button_states(self.btn_estoque)
    
    def switch_to_financas(self):
        self.content_stack.setCurrentWidget(self.dash_financas)
        self.update_button_states(self.btn_financas)

    def switch_to_publico_alvo(self):
        self.content_stack.setCurrentWidget(self.dash_publico_alvo)
        self.update_button_states(self.btn_publico_alvo)
        
    def switch_to_fornecedores(self):
        self.content_stack.setCurrentWidget(self.dash_fornecedores)
        self.update_button_states(self.btn_fornecedores)

    def switch_to_rh(self):
        self.content_stack.setCurrentWidget(self.dash_rh)
        self.update_button_states(self.btn_rh)