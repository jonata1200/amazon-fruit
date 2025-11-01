# modules/widgets/period_bar.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDateEdit, QPushButton
from PyQt6.QtCore import QDate

class PeriodBar(QWidget):
    """
    Barra simples com dois QDateEdit e um botão Aplicar.
    Emite callback via handler passado no construtor.
    """
    def __init__(self, on_apply, parent=None):
        super().__init__(parent)
        self.on_apply = on_apply

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Período:"))
        self.dt_start = QDateEdit()
        self.dt_start.setCalendarPopup(True)
        self.dt_end = QDateEdit()
        self.dt_end.setCalendarPopup(True)

        # defaults: mês corrente
        today = QDate.currentDate()
        first = QDate(today.year(), today.month(), 1)
        self.dt_start.setDate(first)
        self.dt_end.setDate(today)

        btn = QPushButton("Aplicar")
        btn.clicked.connect(self._apply)

        layout.addWidget(self.dt_start)
        layout.addWidget(QLabel("até"))
        layout.addWidget(self.dt_end)
        layout.addWidget(btn)

    def _apply(self):
        s = self.dt_start.date().toString("yyyy-MM-dd")
        e = self.dt_end.date().toString("yyyy-MM-dd")
        if callable(self.on_apply):
            self.on_apply(s, e)