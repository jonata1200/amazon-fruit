# modules/app_styles.py

# --- Paletas de Cores ---
dark_theme = {
    "PRIMARY_COLOR": "#4B0082", "SECONDARY_COLOR": "#FF8C00", "ACCENT_COLOR": "#2E8B57",
    "TEXT_COLOR": "#FFFFFF", "BACKGROUND_COLOR": "#2E2E2E", "NAV_BACKGROUND_COLOR": "#1C1C1C",
    "INPUT_BG_COLOR": "#3C3C3C", "KPI_BG_COLOR": "#1C1C1C", "KPI_TITLE_COLOR": "#CCCCCC",
    "ACTION_BUTTON_BG_COLOR": "#4A4A4A", "ACTION_BUTTON_TEXT_COLOR": "#FFFFFF",
    # Novas cores para os diálogos
    "DIALOG_BG_COLOR": "#2E2E2E",
    "DIALOG_BUTTON_BG_COLOR": "#4B0082"
}
light_theme = {
    "PRIMARY_COLOR": "#6A0DAD", "SECONDARY_COLOR": "#FFA500", "ACCENT_COLOR": "#3CB371",
    "TEXT_COLOR": "#000000", "BACKGROUND_COLOR": "#F0F0F0", "NAV_BACKGROUND_COLOR": "#FFFFFF",
    "INPUT_BG_COLOR": "#FFFFFF", "KPI_BG_COLOR": "#FFFFFF", "KPI_TITLE_COLOR": "#666666",
    "ACTION_BUTTON_BG_COLOR": "#6A0DAD", "ACTION_BUTTON_TEXT_COLOR": "#FFFFFF",
    # Novas cores para os diálogos
    "DIALOG_BG_COLOR": "#F0F0F0",
    "DIALOG_BUTTON_BG_COLOR": "#6A0DAD"
}

def get_stylesheet(theme_name='dark'):
    """Retorna a folha de estilos QSS para o tema escolhido."""
    theme = dark_theme if theme_name == 'dark' else light_theme
    
    return f"""
        /* Estilos Gerais */
        QWidget {{ color: {theme["TEXT_COLOR"]}; font-size: 14px; font-family: Arial, sans-serif; }}
        QMainWindow {{ background-color: {theme["BACKGROUND_COLOR"]}; }}

        /* Barra de Navegação */
        QFrame#NavFrame {{ background-color: {theme["NAV_BACKGROUND_COLOR"]}; }}
        QPushButton#NavButton {{
            background-color: transparent; color: {theme["TEXT_COLOR"]}; border: none; border-radius: 8px;
            padding: 12px; font-size: 16px; font-weight: bold; text-align: left;
        }}
        QPushButton#NavButton:hover {{ background-color: {theme["BACKGROUND_COLOR"]}; }}
        QPushButton#NavButton:checked {{
            background-color: {theme["PRIMARY_COLOR"]}; color: #FFFFFF;
            border-left: 4px solid {theme["SECONDARY_COLOR"]};
        }}

        /* Botões de Ação (Adicionar, Editar, etc.) */
        QPushButton#ActionButton {{
            background-color: {theme["ACTION_BUTTON_BG_COLOR"]};
            color: {theme["ACTION_BUTTON_TEXT_COLOR"]};
            border: none; border-radius: 5px; padding: 8px 12px;
            font-size: 14px; font-weight: bold;
        }}
        QPushButton#ActionButton:hover {{ background-color: {theme["SECONDARY_COLOR"]}; }}

        /* Outros Componentes */
        QLineEdit {{
            background-color: {theme["INPUT_BG_COLOR"]}; color: {theme["TEXT_COLOR"]};
            border: 1px solid {theme["PRIMARY_COLOR"]}; border-radius: 5px;
            padding: 8px; font-size: 14px;
        }}
        QTableWidget {{
            background-color: {theme["NAV_BACKGROUND_COLOR"]};
            gridline-color: {theme["BACKGROUND_COLOR"]};
        }}
        QHeaderView::section:horizontal {{
            background-color: {theme["PRIMARY_COLOR"]}; color: #FFFFFF;
            padding: 4px; border: 1px solid {theme["BACKGROUND_COLOR"]};
        }}
        QHeaderView::section:vertical {{
            background-color: {theme["NAV_BACKGROUND_COLOR"]};
            color: {theme["TEXT_COLOR"]};
            border: 1px solid {theme["BACKGROUND_COLOR"]};
        }}
        QFrame#KPIFrame {{ background-color: {theme["KPI_BG_COLOR"]}; border-radius: 8px; }}
        QLabel#KPITitleLabel {{ font-size: 14px; color: {theme["KPI_TITLE_COLOR"]}; font-weight: normal; }}
        QLabel#KPIValueLabel {{ font-size: 22px; font-weight: bold; color: {theme["TEXT_COLOR"]}; }}

        /* --- NOVOS ESTILOS PARA CAIXAS DE DIÁLOGO (QMessageBox) --- */
        QMessageBox {{
            background-color: {theme["DIALOG_BG_COLOR"]};
        }}
        QMessageBox QLabel {{
            color: {theme["TEXT_COLOR"]};
            font-size: 14px;
        }}
        QMessageBox QPushButton {{
            background-color: {theme["DIALOG_BUTTON_BG_COLOR"]};
            color: #FFFFFF; /* Texto do botão sempre branco para contraste */
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: {theme["SECONDARY_COLOR"]};
        }}
    """