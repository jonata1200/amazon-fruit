# modules/dashboards/dashboard_insights.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
from PyQt6.QtCore import Qt

from modules.analysis.insights_analysis import (
    find_most_profitable_products,
    find_top_customers_by_spend,
    analyze_monthly_financial_trend
)

class DashboardInsights(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name
        
        self.insight_label_1 = None
        self.insight_label_2 = None
        self.insight_label_3 = None

        self.build_ui()
        self.refresh()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        title = QLabel("Insights do Negócio")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # Usar uma área de rolagem para o caso de muitos insights
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        content_widget = QWidget()
        insights_layout = QVBoxLayout(content_widget)
        insights_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        insights_layout.setSpacing(25)

        self.insight_label_1 = self._create_insight_label()
        self.insight_label_2 = self._create_insight_label()
        self.insight_label_3 = self._create_insight_label()

        insights_layout.addWidget(self.insight_label_1)
        insights_layout.addWidget(self.insight_label_2)
        insights_layout.addWidget(self.insight_label_3)
        
        scroll_area.setWidget(content_widget)
        root.addWidget(scroll_area)

    def _create_insight_label(self):
        label = QLabel("Calculando insight...")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setStyleSheet("font-size: 16px; line-height: 1.5; background-color: #3c3c3c; border-radius: 8px; padding: 15px;")
        return label

    def refresh(self):
        # Carrega todos os dataframes necessários
        df_estoque = self.data_handler.load_table("Estoque")
        df_publico = self.data_handler.load_table("Publico_Alvo")
        df_financas = self.data_handler.load_table("Financas")

        # Gera e exibe cada insight
        insight1_text = find_most_profitable_products(df_estoque)
        self.insight_label_1.setText(insight1_text)

        insight2_text = find_top_customers_by_spend(df_publico)
        self.insight_label_2.setText(insight2_text)
        
        insight3_text = analyze_monthly_financial_trend(df_financas)
        self.insight_label_3.setText(insight3_text)

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        # Adapta o estilo dos cards de insight ao tema
        bg_color = "#3c3c3c" if self.theme_name == 'dark' else '#FFFFFF'
        style = f"font-size: 16px; line-height: 1.5; background-color: {bg_color}; border-radius: 8px; padding: 15px;"
        self.insight_label_1.setStyleSheet(style)
        self.insight_label_2.setStyleSheet(style)
        self.insight_label_3.setStyleSheet(style)