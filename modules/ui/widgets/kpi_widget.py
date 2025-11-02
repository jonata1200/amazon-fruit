# modules/ui/widgets/kpi_widget.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class KPIWidget(QFrame):
    """
    Um widget de card reutilizável para exibir um Indicador Chave de Performance (KPI).
    Encapsula o título e o valor, facilitando a atualização.
    """
    def __init__(self, title: str, value_color: str = None, parent=None):
        super().__init__(parent)
        self.setObjectName("KPIFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)

        title_label = QLabel(title)
        title_label.setObjectName("KPITitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label = QLabel("—") # Valor inicial é um placeholder
        self.value_label.setObjectName("KPIValueLabel")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if value_color:
            self.value_label.setStyleSheet(f"color: {value_color};")

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

    def setValue(self, text: str):
        """Atualiza o texto do valor exibido no KPI."""
        self.value_label.setText(text)