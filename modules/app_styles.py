# modules/app_styles.py

# --- Paletas de Cores ---
dark_theme = {
    "PRIMARY_COLOR": "#4B0082", "SECONDARY_COLOR": "#FF8C00", "ACCENT_COLOR": "#2E8B57",
    "TEXT_COLOR": "#FFFFFF", "BACKGROUND_COLOR": "#2E2E2E", "NAV_BACKGROUND_COLOR": "#1C1C1C",
    "INPUT_BG_COLOR": "#3C3C3C", "KPI_BG_COLOR": "#1C1C1C", "KPI_TITLE_COLOR": "#CCCCCC",
    "ACTION_BUTTON_BG_COLOR": "#4A4A4A", "ACTION_BUTTON_TEXT_COLOR": "#FFFFFF",
    "DIALOG_BG_COLOR": "#2E2E2E", "DIALOG_BUTTON_BG_COLOR": "#4B0082"
}
light_theme = {
    "PRIMARY_COLOR": "#6A0DAD", "SECONDARY_COLOR": "#FFA500", "ACCENT_COLOR": "#3CB371",
    "TEXT_COLOR": "#000000", "BACKGROUND_COLOR": "#F0F0F0", "NAV_BACKGROUND_COLOR": "#FFFFFF",
    "INPUT_BG_COLOR": "#FFFFFF", "KPI_BG_COLOR": "#FFFFFF", "KPI_TITLE_COLOR": "#666666",
    "ACTION_BUTTON_BG_COLOR": "#6A0DAD", "ACTION_BUTTON_TEXT_COLOR": "#FFFFFF",
    "DIALOG_BG_COLOR": "#F0F0F0", "DIALOG_BUTTON_BG_COLOR": "#6A0DAD"
}

def get_stylesheet(theme_name='dark') -> str:
    """Retorna a folha de estilos QSS para o tema escolhido."""
    theme = dark_theme if theme_name == 'dark' else light_theme

    # Cores específicas para tabelas (garantem legibilidade)
    if theme_name == 'dark':
        table_bg = "#121418"
        table_alt = "#171A20"
        table_text = "#E6E6E6"
        table_grid = "#2B2F36"
        table_sel_bg = "#3A4A63"
        table_sel_text = "#FFFFFF"
        header_bg = "#2B2F3A"
        header_text = "#E6E6E6"
    else:
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
        /* QTableView (corrige legibilidade no tema escuro) */
        QTableView {{
            background-color: {table_bg};
            alternate-background-color: {table_alt};
            color: {table_text};
            gridline-color: {table_grid};
            selection-background-color: {table_sel_bg};
            selection-color: {table_sel_text};
        }}
        /* Fallback para QTableWidget (se usar em algum lugar) */
        QTableWidget {{
            background-color: {table_bg};
            alternate-background-color: {table_alt};
            color: {table_text};
            gridline-color: {table_grid};
            selection-background-color: {table_sel_bg};
            selection-color: {table_sel_text};
        }}
        /* Cabeçalho das tabelas */
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
        QFrame#KPIFrame {{ background-color: {theme["KPI_BG_COLOR"]}; border-radius: 8px; }}
        QLabel#KPITitleLabel {{ font-size: 14px; color: {theme["KPI_TITLE_COLOR"]}; font-weight: normal; }}
        QLabel#KPIValueLabel {{ font-size: 22px; font-weight: bold; color: {theme["TEXT_COLOR"]}; }}

        /* =================== DIÁLOGOS =================== */
        QMessageBox {{ background-color: {theme["DIALOG_BG_COLOR"]}; }}
        QMessageBox QLabel {{ color: {theme["TEXT_COLOR"]}; font-size: 14px; }}
        QMessageBox QPushButton {{
            background-color: {theme["DIALOG_BUTTON_BG_COLOR"]};
            color: #FFFFFF; border: none; border-radius: 5px;
            padding: 8px 16px; font-weight: bold; min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{ background-color: {theme["SECONDARY_COLOR"]}; }}

        /* QDialog genérico + botões */
        QDialog {{ background-color: {theme["DIALOG_BG_COLOR"]}; }}
        QDialogButtonBox QPushButton {{
            background-color: {theme["DIALOG_BUTTON_BG_COLOR"]};
            color: #FFFFFF; border: none; border-radius: 5px;
            padding: 8px 16px; font-weight: bold; min-width: 80px;
        }}
        QDialogButtonBox QPushButton:hover {{
            background-color: {theme["SECONDARY_COLOR"]};
        }}
    """