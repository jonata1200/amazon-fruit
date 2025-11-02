# modules/widgets/period_bar.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDateEdit, QPushButton, QCalendarWidget
from PyQt6.QtCore import QDate, Qt, QLocale

class PeriodBar(QWidget):
    """
    Barra de período com dois QDateEdit (pt-BR), calendário popup estilizado e tema dinâmico.
    """
    def __init__(self, on_apply, parent=None):
        super().__init__(parent)
        self.on_apply = on_apply
        self._theme = "dark"  # atualizado via set_theme()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        layout.addWidget(QLabel("Período:"))

        self.dt_start = self._make_dateedit()
        self.dt_end   = self._make_dateedit()

        # defaults: mês corrente
        today = QDate.currentDate()
        first = QDate(today.year(), today.month(), 1)
        self.dt_start.setDate(first)
        self.dt_end.setDate(today)

        self.btn_apply = QPushButton("Aplicar")
        self.btn_apply.setObjectName("PeriodApplyButton")
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.clicked.connect(self._apply)

        layout.addWidget(self.dt_start)
        layout.addWidget(QLabel("até"))
        layout.addWidget(self.dt_end)
        layout.addWidget(self.btn_apply)
        layout.addStretch(1)

        # estilo inicial
        self._apply_theme_to_inputs()
        self._apply_calendar_style(self.dt_start.calendarWidget())
        self._apply_calendar_style(self.dt_end.calendarWidget())

    # ---------- API pública ----------
    def set_theme(self, theme: str):
        """Chame quando o app trocar de tema: 'dark' ou 'light'."""
        self._theme = (theme or "dark").lower()
        self._apply_theme_to_inputs()
        self._apply_calendar_style(self.dt_start.calendarWidget())
        self._apply_calendar_style(self.dt_end.calendarWidget())

    # ---------- internos ----------
    def _make_dateedit(self) -> QDateEdit:
        de = QDateEdit()
        de.setDisplayFormat("dd/MM/yyyy")
        de.setCalendarPopup(True)
        de.setLocale(QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil))

        cal = QCalendarWidget()
        cal.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        cal.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        cal.setGridVisible(True)
        cal.setMinimumSize(360, 280)  # maior
        de.setCalendarWidget(cal)
        return de

    def _apply(self):
        s = self.dt_start.date().toString("yyyy-MM-dd")
        e = self.dt_end.date().toString("yyyy-MM-dd")
        if callable(self.on_apply):
            self.on_apply(s, e)

    def _apply_theme_to_inputs(self):
        """Estiliza QDateEdit e botão por tema (resolve botão ilegível no dark)."""
        if self._theme == "light":
            dateedit_css = """
                QDateEdit { font-size: 14px; padding: 4px 6px; color: #202124; background: #FFFFFF; }
                QDateEdit::drop-down { width: 18px; }
            """
            button_css = """
                QPushButton#PeriodApplyButton {
                    background: #FFFFFF; color: #202124; border: 1px solid #C9C9C9; padding: 6px 12px; border-radius: 4px;
                }
                QPushButton#PeriodApplyButton:hover { background: #F3F4F6; }
                QPushButton#PeriodApplyButton:pressed { background: #E5E7EB; }
                QPushButton#PeriodApplyButton:disabled { background: #F3F4F6; color: #9CA3AF; border-color: #E5E7EB; }
            """
        else:  # dark
            dateedit_css = """
                QDateEdit { font-size: 14px; padding: 4px 6px; color: #E8EAED; background: #2B2B2B; border: 1px solid #444; }
                QDateEdit::drop-down { width: 18px; }
            """
            button_css = """
                QPushButton#PeriodApplyButton {
                    background: #3A3A3A; color: #FFFFFF; border: 1px solid #5A5A5A; padding: 6px 12px; border-radius: 4px;
                }
                QPushButton#PeriodApplyButton:hover  { background: #454545; }
                QPushButton#PeriodApplyButton:pressed{ background: #2F2F2F; }
                QPushButton#PeriodApplyButton:disabled { background: #2F2F2F; color: #9CA3AF; border-color: #555; }
            """
        self.dt_start.setStyleSheet(dateedit_css)
        self.dt_end.setStyleSheet(dateedit_css)
        self.btn_apply.setStyleSheet(button_css)

    def _apply_calendar_style(self, cal: QCalendarWidget):
        """Estilo ALTO CONTRASTE para o calendário popup (inclui header dos dias)."""
        if cal is None:
            return

        if self._theme == "light":
            bg = "#FFFFFF"; fg = "#202124"
            header_bg = "#1976D2"; header_fg = "#FFFFFF"
            grid = "#E0E0E0"
            sel_bg = "#6A0DAD"; sel_fg = "#FFFFFF"
            wkd = "#D32F2F"; disabled = "#9E9E9E"
            head_row_bg = "#F5F5F5"; head_row_fg = "#202124"
        else:
            bg = "#202124"; fg = "#E8EAED"
            header_bg = "#2B59C3"; header_fg = "#FFFFFF"
            grid = "#3C4043"
            sel_bg = "#9C27B0"; sel_fg = "#FFFFFF"
            wkd = "#FF6D6D"; disabled = "#80868B"
            head_row_bg = "#303134"; head_row_fg = "#FFFFFF"

        # alvo correto: a grade é um QTableView com objectName "qt_calendar_calendarview"
        # reforçamos também o header horizontal (nomes dos dias)
        cal.setStyleSheet(f"""
            QCalendarWidget {{
                background: {bg};
                color: {fg};
                border: 1px solid {grid};
            }}

            /* barra superior (mês/ano/setas) */
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background: {header_bg};
                color: {header_fg};
                font-weight: bold;
                border: none;
                min-height: 30px;
            }}
            QCalendarWidget QToolButton {{
                background: transparent;
                color: {header_fg};
                border: none;
                padding: 2px 8px;
                font-size: 14px;
            }}
            QCalendarWidget QToolButton:hover {{
                background: rgba(255,255,255,0.15);
            }}
            QCalendarWidget QMenu {{
                background: {bg};
                color: {fg};
                border: 1px solid {grid};
            }}
            QCalendarWidget QSpinBox {{
                color: {header_fg};
                background: transparent;
                border: none;
                font-size: 14px;
            }}

            /* grade de dias */
            QTableView#qt_calendar_calendarview {{
                background: {bg};
                color: {fg};
                gridline-color: {grid};
                selection-background-color: {sel_bg};
                selection-color: {sel_fg};
                font-size: 14px;
            }}
            QTableView#qt_calendar_calendarview::item {{ padding: 6px; }}

            /* domingos em vermelho quando não selecionados */
            QTableView#qt_calendar_calendarview::item:enabled:!selected:column(0) {{
                color: {wkd};
            }}

            /* dias de outro mês */
            QTableView#qt_calendar_calendarview::item:!enabled {{
                color: {disabled};
            }}

            /* CABEÇALHO dos dias da semana */
            QTableView#qt_calendar_calendarview QHeaderView::section {{
                background: {head_row_bg};
                color: {head_row_fg};
                padding: 6px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }}
            /* canto superior esquerdo (se existir) */
            QTableCornerButton::section {{
                background: {head_row_bg};
                border: none;
            }}
        """)