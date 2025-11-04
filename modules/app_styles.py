# modules/app_styles.py

# --- Paleta de Cores Única (Tema Claro) ---
light_theme = {
    "PRIMARY_COLOR": "#6A0DAD", "SECONDARY_COLOR": "#FFA500", "ACCENT_COLOR": "#3CB371",
    "TEXT_COLOR": "#000000", "BACKGROUND_COLOR": "#F0F0F0", "NAV_BACKGROUND_COLOR": "#FFFFFF",
    "INPUT_BG_COLOR": "#FFFFFF", "KPI_BG_COLOR": "#FFFFFF", "KPI_TITLE_COLOR": "#666666",
    "ACTION_BUTTON_BG_COLOR": "#6A0DAD", "ACTION_BUTTON_TEXT_COLOR": "#FFFFFF",
    "DIALOG_BG_COLOR": "#F0F0F0", "DIALOG_BUTTON_BG_COLOR": "#6A0DAD"
}

def get_stylesheet() -> str:
    """Retorna a folha de estilos QSS para o tema claro padrão."""
    theme = light_theme

    # Cores específicas para tabelas (tema claro)
    table_bg = "#FFFFFF"
    table_alt = "#FAFAFA"
    table_text = "#1A1A1A"
    table_grid = "#DDDDDD"
    table_sel_bg = "#E6F0FF"
    table_sel_text = "#0D0D0D"
    header_bg = "#F1F3F5"
    header_text = "#1A1A1A"

    return f"""
        /* =================== GERAL =================== */
        QWidget {{
            color: {theme["TEXT_COLOR"]};
            font-size: 14px;
            font-family: Arial, sans-serif;
        }}
        QMainWindow {{ background-color: {theme["BACKGROUND_COLOR"]}; }}

        /* =================== ABAS (TABS) =================== */
        QTabWidget::pane {{
            border-top: 2px solid {theme["PRIMARY_COLOR"]};
            margin-top: -2px;
        }}
        QTabBar::tab {{
            background-color: {theme["BACKGROUND_COLOR"]};
            color: {theme["TEXT_COLOR"]};
            border: 1px solid {theme["PRIMARY_COLOR"]};
            border-bottom: none;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QTabBar::tab:hover {{
            background-color: {theme["SECONDARY_COLOR"]};
            color: #000000;
        }}
        QTabBar::tab:selected {{
            background-color: {theme["PRIMARY_COLOR"]};
            color: #FFFFFF;
            border-color: {theme["PRIMARY_COLOR"]};
        }}
        QTabBar::tab:!selected {{
            margin-top: 2px;
        }}

        /* =================== NAVEGAÇÃO =================== */
        QFrame#NavFrame {{ background-color: {theme["NAV_BACKGROUND_COLOR"]}; }}
        QPushButton#NavButton {{
            background-color: transparent;
            color: {theme["TEXT_COLOR"]};
            border: none; border-radius: 8px;
            padding: 12px; font-size: 16px; font-weight: bold; text-align: left;
        }}
        QPushButton#NavButton:hover {{ background-color: {theme["BACKGROUND_COLOR"]}; }}
        QPushButton#NavButton:checked {{
            background-color: {theme["PRIMARY_COLOR"]}; color: #FFFFFF;
            border-left: 4px solid {theme["SECONDARY_COLOR"]};
        }}

        QPushButton#ActionButton {{
            background-color: {theme["ACTION_BUTTON_BG_COLOR"]};
            color: {theme["ACTION_BUTTON_TEXT_COLOR"]};
            border: none; border-radius: 5px; padding: 8px 12px;
            font-size: 14px; font-weight: bold;
        }}
        QPushButton#ActionButton:hover {{ background-color: {theme["SECONDARY_COLOR"]}; }}

        /* =================== FORM / INPUTS =================== */
        QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
            background-color: {theme["INPUT_BG_COLOR"]};
            color: {theme["TEXT_COLOR"]};
            border: 1px solid {theme["PRIMARY_COLOR"]}; border-radius: 5px;
            padding: 8px; font-size: 14px;
        }}

        /* =================== TABELAS =================== */
        QTableView, QTableWidget {{
            background-color: {table_bg};
            alternate-background-color: {table_alt};
            color: {table_text};
            gridline-color: {table_grid};
            selection-background-color: {table_sel_bg};
            selection-color: {table_sel_text};
        }}
        QHeaderView::section {{
            background-color: {header_bg};
            color: {header_text};
            border: 0px;
            padding: 6px 8px;
            font-weight: 600;
        }}
        QTableCornerButton::section {{
            background-color: {header_bg};
            border: 0px;
        }}

        /* =================== KPIs =================== */
        QFrame#KPIFrame {{ background-color: {theme["KPI_BG_COLOR"]}; border-radius: 8px; border: 1px solid #E0E0E0; }}
        QLabel#KPITitleLabel {{ font-size: 14px; color: {theme["KPI_TITLE_COLOR"]}; font-weight: normal; }}
        QLabel#KPIValueLabel {{ font-size: 22px; font-weight: bold; color: {theme["TEXT_COLOR"]}; }}

        /* =================== DIÁLOGOS =================== */
        QMessageBox, QDialog {{ background-color: {theme["DIALOG_BG_COLOR"]}; }}
        QMessageBox QLabel {{ color: {theme["TEXT_COLOR"]}; font-size: 14px; }}
        QMessageBox QPushButton, QDialogButtonBox QPushButton {{
            background-color: {theme["DIALOG_BUTTON_BG_COLOR"]};
            color: #FFFFFF; border: none; border-radius: 5px;
            padding: 8px 16px; font-weight: bold; min-width: 80px;
        }}
        QMessageBox QPushButton:hover, QDialogButtonBox QPushButton:hover {{
            background-color: {theme["SECONDARY_COLOR"]};
        }}
    """