# modules/ui/widgets/kpi_widget.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import pandas as pd

class KPIWidget(QFrame):
    def __init__(self, title: str, value_color: str = None, parent=None):
        super().__init__(parent)
        self.setObjectName("KPIFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4) # Espaçamento menor para acomodar o novo texto

        self.title_label = QLabel(title)
        self.title_label.setObjectName("KPITitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label = QLabel("—")
        self.value_label.setObjectName("KPIValueLabel")
        if value_color:
            self.value_label.setStyleSheet(f"color: {value_color};")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- MUDANÇA 1: Adicionar um label para a comparação ---
        self.comparison_label = QLabel("") # Inicialmente vazio
        self.comparison_label.setObjectName("KPIComparisonLabel")
        self.comparison_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.comparison_label) # Adiciona o novo label ao layout

    def setValue(self, text: str):
        """Método antigo para compatibilidade com outros dashboards."""
        self.value_label.setText(text)
        self.comparison_label.setText("") # Limpa a comparação

    # --- MUDANÇA 2: Novo método para popular o widget com dados ricos ---
    def update_values(self, main_value, comparison_change: float | None, formatter_func):
        """
        Atualiza o KPI com um valor principal e uma variação percentual.
        - main_value: O valor a ser exibido (ex: 1500000)
        - comparison_change: A variação percentual (ex: 0.15 para +15%)
        - formatter_func: A função para formatar o valor principal (ex: fmt_currency)
        """
        # Formata e exibe o valor principal
        self.value_label.setText(formatter_func(main_value))

        # Lida com a variação
        if comparison_change is not None and pd.notna(comparison_change):
            # Formata o percentual com sinal de '+' ou '-'
            change_text = f"{comparison_change:+.1%}"
            
            # Define o ícone e a cor com base no valor
            if comparison_change > 0:
                icon = "▲"
                color = "#2E8B57" # Verde
            elif comparison_change < 0:
                icon = "▼"
                color = "#C21807" # Vermelho
            else:
                icon = ""
                color = "#666666" # Cinza
            
            self.comparison_label.setText(f"{icon} {change_text}")
            self.comparison_label.setStyleSheet(f"color: {color};")
        else:
            # Se não houver variação, limpa o texto
            self.comparison_label.setText("")