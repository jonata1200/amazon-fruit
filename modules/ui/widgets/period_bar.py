# modules/ui/widgets/period_bar.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDateEdit, QPushButton, QCalendarWidget
from PyQt6.QtCore import QDate, Qt, QLocale

class PeriodBar(QWidget):
    def __init__(self, on_apply, parent=None):
        super().__init__(parent)
        self.on_apply = on_apply

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6); layout.setSpacing(8)
        layout.addWidget(QLabel("Período:"))

        self.dt_start = self._make_dateedit()
        self.dt_end   = self._make_dateedit()
        
        today = QDate.currentDate()
        first = QDate(today.year(), today.month(), 1)
        self.dt_start.setDate(first); self.dt_end.setDate(today)

        self.btn_apply = QPushButton("Aplicar")
        self.btn_apply.setObjectName("PeriodApplyButton")
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.clicked.connect(self._apply)

        layout.addWidget(self.dt_start); layout.addWidget(QLabel("até"))
        layout.addWidget(self.dt_end); layout.addWidget(self.btn_apply)
        layout.addStretch(1)

        self._apply_styles()

    def _make_dateedit(self) -> QDateEdit:
        de = QDateEdit()
        de.setDisplayFormat("dd/MM/yyyy"); de.setCalendarPopup(True)
        de.setLocale(QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil))
        cal = QCalendarWidget()
        cal.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        cal.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        cal.setGridVisible(True); cal.setMinimumSize(360, 280)
        de.setCalendarWidget(cal)
        return de

    def _apply(self):
        s = self.dt_start.date().toString("yyyy-MM-dd")
        e = self.dt_end.date().toString("yyyy-MM-dd")
        if callable(self.on_apply):
            self.on_apply(s, e)
    
    def _apply_styles(self):
        # Estilos fixos do tema claro
        dateedit_css = """
            QDateEdit { font-size: 14px; padding: 4px 6px; color: #202124; background: #FFFFFF; }
            QDateEdit::drop-down { width: 18px; }
        """
        button_css = """
            QPushButton#PeriodApplyButton {
                background: #FFFFFF; color: #202124; border: 1px solid #C9C9C9; padding: 6px 12px; border-radius: 4px;
            }
            QPushButton#PeriodApplyButton:hover { background: #F3F4F6; }
        """
        self.dt_start.setStyleSheet(dateedit_css)
        self.dt_end.setStyleSheet(dateedit_css)
        self.btn_apply.setStyleSheet(button_css)
        self._apply_calendar_style(self.dt_start.calendarWidget())
        self._apply_calendar_style(self.dt_end.calendarWidget())

    def _apply_calendar_style(self, cal: QCalendarWidget):
        if cal is None: return
        cal.setStyleSheet("""
            QCalendarWidget { background: #FFFFFF; color: #202124; border: 1px solid #E0E0E0; }
            QCalendarWidget QWidget#qt_calendar_navigationbar { background: #1976D2; color: #FFFFFF; }
            QCalendarWidget QToolButton { background: transparent; color: #FFFFFF; }
            QCalendarWidget QMenu { background: #FFFFFF; color: #202124; }
            QCalendarWidget QSpinBox { color: #FFFFFF; background: transparent; border: none; }
            QTableView#qt_calendar_calendarview { background: #FFFFFF; color: #202124; gridline-color: #E0E0E0; selection-background-color: #6A0DAD; selection-color: #FFFFFF; }
            QTableView#qt_calendar_calendarview::item:enabled:!selected:column(0) { color: #D32F2F; }
            QTableView#qt_calendar_calendarview::item:!enabled { color: #9E9E9E; }
            QTableView#qt_calendar_calendarview QHeaderView::section { background: #F5F5F5; color: #202124; }
        """)