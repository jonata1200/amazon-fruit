# modules/dashboards/dashboard_insights.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QGridLayout, QLabel, QFrame, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import pandas as pd

# Importa TODAS as funções de análise necessárias de outros módulos
from modules.analysis.financial_analysis import calculate_financial_summary
from modules.analysis.inventory_analysis import analyze_inventory_kpis
from modules.analysis.public_analysis import analyze_public_kpis
from modules.analysis.suppliers_analysis import analyze_suppliers_kpis

# Importa os formatadores para consistência
from modules.utils.formatters import fmt_currency

# ======================================================================
# --- 1. NOVO COMPONENTE: UM CARD DE INSIGHT MODERNO E REUTILIZÁVEL ---
# ======================================================================
class InsightCard(QFrame):
    """
    Um widget de card redesenhado para exibir um KPI com ícone, título e valor,
    proporcionando uma hierarquia visual clara.
    """
    def __init__(self, icon_char: str, title: str, accent_color: str = "#6A0DAD"):
        super().__init__()
        self.setObjectName("InsightCardFrame")

        # Layout principal horizontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Ícone (à esquerda)
        icon_label = QLabel(icon_char)
        icon_label.setObjectName("InsightIconLabel")
        icon_label.setStyleSheet(f"color: {accent_color};")
        
        # Container para textos (à direita)
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        # Título e Valor
        self.title_label = QLabel(title)
        self.title_label.setObjectName("InsightTitleLabel")
        
        self.value_label = QLabel("—")
        self.value_label.setObjectName("InsightValueLabel")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.value_label)

        layout.addWidget(icon_label)
        layout.addWidget(text_container, 1) # O container de texto se expande

    def setValue(self, text: str):
        self.value_label.setText(text)

# ======================================================================
# --- 2. O DASHBOARD PRINCIPAL, AGORA MAIS LIMPO E INTELIGENTE ---
# ======================================================================
class DashboardInsights(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.cards = {}
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(25, 20, 25, 20)
        root.setSpacing(20)

        # --- MUDANÇA 1: Adicionar um 'ObjectName' para estilização específica ---
        title = QLabel("Insights do Negócio")
        title.setObjectName("InsightsTitleLabel") # Identificador para o CSS
        # A linha setFont foi removida para centralizar o estilo no QSS
        root.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(15)
        self.cards["lucro_total"] = InsightCard("💰", "Lucro Líquido", "#2E8B57")
        self.cards["receita_total"] = InsightCard("📈", "Receita Total", "#1E90FF")
        self.cards["despesa_total"] = InsightCard("📉", "Despesas Totais", "#DC143C")
        self.cards["rupturas"] = InsightCard("⚠️", "Itens em Ruptura", "#FF8C00")
        self.cards["pct_fem"]  = InsightCard("♀️", "% Público Feminino", "#FF69B4")
        self.cards["rating"]   = InsightCard("⭐", "Avaliação Média (Forn.)", "#4682B4")
        grid.addWidget(self.cards["lucro_total"],   0, 0); grid.addWidget(self.cards["receita_total"], 0, 1); grid.addWidget(self.cards["despesa_total"], 0, 2)
        grid.addWidget(self.cards["rupturas"], 1, 0); grid.addWidget(self.cards["pct_fem"],  1, 1); grid.addWidget(self.cards["rating"],   1, 2)
        root.addLayout(grid)

        self.highlights = QTextEdit()
        self.highlights.setReadOnly(True)
        self.highlights.setObjectName("HighlightsBox")
        root.addWidget(self.highlights, 1)
        
        # --- MUDANÇA 2: Adicionar a regra de estilo para o novo título ---
        self.setStyleSheet("""
            #InsightsTitleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 10px; /* Adiciona um espaço abaixo do título */
            }

            #InsightCardFrame { background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E0E0E0; }
            #InsightIconLabel { font-size: 32px; }
            #InsightTitleLabel { font-size: 13px; color: #666666; }
            #InsightValueLabel { font-size: 22px; font-weight: bold; color: #1A1A1A; }
            
            #HighlightsBox {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                font-size: 16px;
                padding: 15px;
            }
        """)

    # Nenhuma mudança necessária no método refresh. Ele já está correto.
    def refresh(self):
        df_fin = self._safe_load("Financas")
        df_est = self._safe_load("Estoque")
        df_pub = self._safe_load("Publico_Alvo")
        df_forn = self._safe_load("Fornecedores")

        fin_kpis = calculate_financial_summary(df_fin)
        inv_kpis = analyze_inventory_kpis(df_est)
        pub_kpis = analyze_public_kpis(df_pub)
        sup_kpis = analyze_suppliers_kpis(df_forn)

        self.cards["lucro_total"].setValue(fmt_currency(fin_kpis.get('lucro', 0)))
        self.cards["receita_total"].setValue(fmt_currency(fin_kpis.get('receita', 0)))
        self.cards["despesa_total"].setValue(fmt_currency(fin_kpis.get('despesa', 0)))
        self.cards["rupturas"].setValue(str(inv_kpis.get('low_stock_count', 0)))
        
        pct_fem_val = pub_kpis.get('pct_female')
        self.cards["pct_fem"].setValue(f"{pct_fem_val:.1f}%" if pd.notna(pct_fem_val) else "—")
        
        rating_val = sup_kpis.get('avg_rating')
        self.cards["rating"].setValue(f"{rating_val:.2f}" if pd.notna(rating_val) else "—")
        
        html = f"""
        <div style="line-height: 1.6;">
            <p><b>💰 Financeiro:</b> A receita total foi de 
            <span style="color: #1E90FF;"><b>{fmt_currency(fin_kpis.get('receita', 0))}</b></span>, 
            com despesas de <span style="color: #DC143C;"><b>{fmt_currency(fin_kpis.get('despesa', 0))}</b></span>, 
            resultando em um lucro de <span style="color: #2E8B57;"><b>{fmt_currency(fin_kpis.get('lucro', 0))}</b></span>.</p>

            <p><b>📦 Estoque:</b> Atualmente, há 
            <span style="color: #FF8C00;"><b>{inv_kpis.get('low_stock_count', 0)}</b></span> 
            itens em nível de ruptura (igual ou abaixo do estoque mínimo).</p>

            <p><b>👥 Público:</b> O perfil de clientes é composto por 
            <span style="color: #FF69B4;"><b>{f'{pct_fem_val:.1f}%' if pd.notna(pct_fem_val) else 'N/A'}</b></span> 
            do gênero feminino.</p>

            <p><b>⭐ Fornecedores:</b> A avaliação média geral dos fornecedores é de 
            <span style="color: #4682B4;"><b>{f'{rating_val:.2f}' if pd.notna(rating_val) else 'N/A'}</b></span>.</p>
        </div>
        """
        self.highlights.setHtml(html)

    def _safe_load(self, name: str) -> pd.DataFrame:
        try:
            df = self.data_handler.load_table(name)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception:
            return pd.DataFrame()