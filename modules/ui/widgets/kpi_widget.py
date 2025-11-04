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

    # dentro da classe KPIWidget
    def setText(self, value):
        """
        Aceita str/int/float, formata e escreve no label de valor.
        Mantém compatibilidade com chamadas existentes no app.
        """
        # tenta formatar número (pt-BR), senão vira string simples
        try:
            if isinstance(value, (int, float)):
                # formatação 1.234,56 (sem depender de locale do SO)
                txt = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:
                txt = str(value)
        except Exception:
            txt = str(value)

        # tenta achar o label principal
        lbl = getattr(self, "value_label", None) or getattr(self, "label_value", None)
        if lbl is not None:
            lbl.setText(txt)
        else:
            # última tentativa: se existir algum QLabel filho, usa o primeiro
            try:
                # funciona com PyQt6 ou PySide6
                for child in self.findChildren(type(getattr(self, "title_label", object()))):
                    # se title_label for QLabel, acima pode dar ruim; vamos só procurar por objetos com setText
                    pass
                # fallback genérico: percorre filhos e acha algo com setText
                for child in self.children():
                    if hasattr(child, "setText"):
                        child.setText(txt)
                        return
            except Exception:
                pass
            # se não houver nenhum label, evita quebrar o app
            setattr(self, "_last_text", txt)

    # opcional: alias mais explícito se em algum lugar chamarem set_value
    set_value = setText