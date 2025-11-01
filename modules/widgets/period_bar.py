# modules/widgets/period_bar.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDateEdit, QPushButton, QCalendarWidget
from PyQt6.QtCore import QDate, Qt, QLocale

class PeriodBar(QWidget):
    """
    Barra simples de período com dois QDateEdit.
    - Calendário popup estilizado (dark/light)
    - Locale pt-BR
    - Formato dd/MM/yyyy
    """
    def __init__(self, on_apply, parent=None):
        super().__init__(parent)
        self.on_apply = on_apply
        self._theme = "dark"  # padrão; trocado via set_theme()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        layout.addWidget(QLabel("Período:"))

        self.dt_start = self._make_dateedit()
        self.dt_end = self._make_dateedit()

        # defaults: mês corrente
        today = QDate.currentDate()
        first = QDate(today.year(), today.month(), 1)
        self.dt_start.setDate(first)
        self.dt_end.setDate(today)

        btn = QPushButton("Aplicar")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._apply)

        layout.addWidget(self.dt_start)
        layout.addWidget(QLabel("até"))
        layout.addWidget(self.dt_end)
        layout.addWidget(btn)
        layout.addStretch(1)

        # aplica estilo inicial
        self._apply_calendar_style(self.dt_start.calendarWidget())
        self._apply_calendar_style(self.dt_end.calendarWidget())

    # ---------- API pública ----------
    def set_theme(self, theme: str):
        """Chame quando o app trocar de tema: 'dark' ou 'light'."""
        self._theme = (theme or "dark").lower()
        self._apply_calendar_style(self.dt_start.calendarWidget())
        self._apply_calendar_style(self.dt_end.calendarWidget())

    # ---------- internos ----------
    def _make_dateedit(self) -> QDateEdit:
        de = QDateEdit()
        de.setDisplayFormat("dd/MM/yyyy")
        de.setCalendarPopup(True)

        # Locale BR para nomes de meses/dias
        de.setLocale(QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil))

        # Usa um calendário explícito para poder estilizar
        cal = QCalendarWidget()
        # (1) tirar números de semana para abrir espaço (evita "d..., s...")
        cal.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        # header com nomes abreviados (pt-BR já traz "dom, seg, ter, ...")
        cal.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        # opcional: comece na segunda (se preferir, troque para Sunday)
        # cal.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        de.setCalendarWidget(cal)

        # tamanho da fonte no campo
        de.setStyleSheet("QDateEdit { font-size: 14px; padding: 4px 6px; }")
        return de

    def _apply(self):
        s = self.dt_start.date().toString("yyyy-MM-dd")
        e = self.dt_end.date().toString("yyyy-MM-dd")
        if callable(self.on_apply):
            self.on_apply(s, e)

    def _apply_calendar_style(self, cal: QCalendarWidget):
        """Estilo alto contraste para o calendário popup."""
        if cal is None:
            return

        if self._theme == "light":
            bg = "#FFFFFF"
            fg = "#202124"
            header_bg = "#1976D2"
            header_fg = "#FFFFFF"
            grid = "#E0E0E0"
            sel_bg = "#6A0DAD"
            sel_fg = "#FFFFFF"
            wkd = "#D32F2F"
            disabled = "#9E9E9E"
            head_row_bg = "#F5F5F5"
            head_row_fg = "#202124"
        else:  # dark
            bg = "#202124"
            fg = "#E8EAED"
            header_bg = "#2B59C3"
            header_fg = "#FFFFFF"
            grid = "#3C4043"
            sel_bg = "#9C27B0"
            sel_fg = "#FFFFFF"
            wkd = "#FF6D6D"
            disabled = "#80868B"
            head_row_bg = "#303134"   # cabeçalho dos dias da semana
            head_row_fg = "#E8EAED"

        cal.setStyleSheet(f"""
            QCalendarWidget {{
                background: {bg};
                color: {fg};
                border: 1px solid {grid};
            }}

            /* barra de navegação (mês/ano, setas) */
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background: {header_bg};
                color: {header_fg};
                font-weight: bold;
                border: none;
                min-height: 28px;
            }}
            QCalendarWidget QToolButton {{
                background: transparent;
                color: {header_fg};
                border: none;
                padding: 2px 6px;
            }}
            QCalendarWidget QToolButton:hover {{
                background: rgba(255,255,255,0.15);
            }}
            QCalendarWidget QMenu {{
                background: {bg};
                color: {fg};
                border: 1px solid {grid};
            }}
            QCalendarWidget QSpinBox {{  /* ano */
                color: {header_fg};
                background: transparent;
                border: none;
            }}

            /* Tabela de dias */
            QCalendarWidget QTableView {{
                background: {bg};
                color: {fg};
                selection-background-color: {sel_bg};
                selection-color: {sel_fg};
                outline: none;
                gridline-color: {grid};
                font-size: 13px;
            }}
            QCalendarWidget QTableView:item {{
                padding: 4px;
            }}
            /* domingos (coluna 0) em vermelho quando não selecionados */
            QCalendarWidget QTableView::item:enabled:!selected:column(0) {{
                color: {wkd};
            }}
            /* dias de outro mês */
            QCalendarWidget QTableView::item:!enabled {{
                color: {disabled};
            }}

            /* Cabeçalho dos dias da semana (linha superior da tabela) */
            QCalendarWidget QTableView QHeaderView::section {{
                background: {head_row_bg};
                color: {head_row_fg};
                padding: 4px 6px;
                border: none;
                font-weight: 600;
            }}
        """)