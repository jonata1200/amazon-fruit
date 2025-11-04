# modules/dashboards/dashboard_insights.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import pandas as pd

# ---------------------------------------------------------
# Helper de Formatação (pode ser movido para formatters.py no futuro)
# ---------------------------------------------------------
def brl(v):
    if v is None or pd.isna(v): v = 0.0
    try: v = float(v)
    except Exception: v = 0.0
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---------------------------------------------------------
# Widget de Card de Insight (Simplificado para Tema Claro)
# ---------------------------------------------------------
class InsightCard(QFrame):
    def __init__(self, title: str, value: str = "", subtitle: str = "", accent: str = "#00BFFF"):
        super().__init__()
        self.title_lbl = QLabel(title)
        self.value_lbl = QLabel(value)
        self.subtitle_lbl = QLabel(subtitle)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14); lay.setSpacing(4)
        lay.addWidget(self.title_lbl)
        lay.addWidget(self.value_lbl)
        lay.addWidget(self.subtitle_lbl)
        
        # Estilo fixo para o tema claro
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }}
            QLabel:first-child {{ /* Título */
                color: {accent};
                font-size: 12pt;
                font-weight: 600;
            }}
            QLabel:nth-child(2) {{ /* Valor */
                color: #1A1A1A;
                font-size: 20pt;
                font-weight: 700;
            }}
            QLabel:last-child {{ /* Subtítulo */
                color: #666666;
                font-size: 10pt;
            }}
        """)

    def set_value(self, txt: str):
        self.value_lbl.setText(txt)

    def set_subtitle(self, txt: str):
        self.subtitle_lbl.setText(txt)


# ---------------------------------------------------------
# Dashboard Principal (Simplificado para Tema Claro)
# ---------------------------------------------------------
class DashboardInsights(QWidget):
    def __init__(self, data_handler): # Argumento de tema removido
        super().__init__()
        self.data_handler = data_handler
        # self.theme removido
        
        self.cards = {}
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18); root.setSpacing(14)

        title = QLabel("📊 Insights do Negócio")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        root.addWidget(title)

        # Grade de cards
        grid = QGridLayout()
        grid.setHorizontalSpacing(14); grid.setVerticalSpacing(14)

        self.cards["lucro_total"] = InsightCard("Lucro Total", accent="#14C38E")
        self.cards["receita_total"] = InsightCard("Receita Total", accent="#00BFFF")
        self.cards["despesa_total"] = InsightCard("Despesas Totais", accent="#FF6B6B")
        grid.addWidget(self.cards["lucro_total"],   0, 0)
        grid.addWidget(self.cards["receita_total"], 0, 1)
        grid.addWidget(self.cards["despesa_total"], 0, 2)

        self.cards["rupturas"] = InsightCard("Itens em Ruptura (<= mínimo)", accent="#FFD166")
        self.cards["pct_fem"]  = InsightCard("% Feminino (Clientes)", accent="#C77DFF")
        self.cards["rating"]   = InsightCard("Avaliação Média Fornecedores", accent="#4DD0E1")
        grid.addWidget(self.cards["rupturas"], 1, 0)
        grid.addWidget(self.cards["pct_fem"],  1, 1)
        grid.addWidget(self.cards["rating"],   1, 2)
        root.addLayout(grid)

        # Caixa de highlights
        self.highlights = QLabel("")
        self.highlights.setWordWrap(True)
        self.highlights.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.highlights.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        root.addWidget(self.highlights)
        
        # Estilo fixo do tema claro para o dashboard
        self.setStyleSheet("""
            QLabel {{ /* Estilo base para todos os QLabels neste widget */
                color: #1A1A1A;
            }}
            #HighlightsBox {{ /* ID para a caixa de texto */
                background-color: #FFFFFF;
                border: 1px solid #E6E6E6;
                border-radius: 10px;
                padding: 12px;
                color: #333333;
                font-size: 11pt;
            }}
        """)

    def refresh(self):
        # --- Carregamento seguro dos dados ---
        df_fin = self._safe_load("Financas")
        df_est = self._safe_load("Estoque")
        df_pub = self._safe_load("Publico_Alvo")
        df_forn = self._safe_load("Fornecedores")

        # --- Lógica de Análise (permanece a mesma) ---
        # Finanças
        receita_total, despesa_total, lucro_total = 0.0, 0.0, 0.0
        conclusao = ""
        if not df_fin.empty and "Valor" in df_fin.columns and "Tipo" in df_fin.columns:
            df_fin["Valor"] = pd.to_numeric(df_fin["Valor"], errors="coerce").fillna(0.0)
            receita_total = df_fin.loc[df_fin["Tipo"].astype(str).str.lower().eq("receita"), "Valor"].sum()
            despesa_total = df_fin.loc[df_fin["Tipo"].astype(str).str.lower().eq("despesa"), "Valor"].sum()
            lucro_total = receita_total - despesa_total
        
        # Estoque
        rupturas = 0
        if not df_est.empty and {"Quantidade_Estoque", "Nivel_Minimo_Estoque"}.issubset(df_est.columns):
            q = pd.to_numeric(df_est["Quantidade_Estoque"], errors="coerce")
            n = pd.to_numeric(df_est["Nivel_Minimo_Estoque"], errors="coerce")
            rupturas = int((q <= n).sum())

        # Público-alvo
        pct_fem = None
        if not df_pub.empty and "Genero" in df_pub.columns and not df_pub.empty:
            fem = (df_pub["Genero"].astype(str).str.lower() == "feminino").sum()
            pct_fem = 100.0 * fem / len(df_pub)

        # Fornecedores
        rating = None
        if not df_forn.empty and "Avaliacao" in df_forn.columns:
            rating = pd.to_numeric(df_forn["Avaliacao"], errors="coerce").mean()

        # --- Atualização dos Widgets ---
        self.cards["lucro_total"].set_value(brl(lucro_total))
        self.cards["receita_total"].set_value(brl(receita_total))
        self.cards["despesa_total"].set_value(brl(despesa_total))
        self.cards["rupturas"].set_value(str(rupturas))
        self.cards["pct_fem"].set_value(f"{pct_fem:.1f}%" if pct_fem is not None else "—")
        self.cards["rating"].set_value(f"{rating:.2f}" if rating is not None and pd.notna(rating) else "—")
        
        # Highlights em texto
        blocos = [
            f"💰 <b>Financeiro</b><br>Receita total: <b>{brl(receita_total)}</b> · Despesas totais: <b>{brl(despesa_total)}</b> · Lucro total: <b>{brl(lucro_total)}</b>",
            f"📦 <b>Estoque</b><br>Itens em ruptura (≤ mínimo): <b>{rupturas}</b>",
            f"👥 <b>Público</b><br>Clientes do gênero feminino: <b>{pct_fem:.1f}%</b>" if pct_fem is not None else "",
            f"🤝 <b>Fornecedores</b><br>Avaliação média: <b>{rating:.2f}</b>" if rating is not None and pd.notna(rating) else ""
        ]
        self.highlights.setText("<br><br>".join(filter(None, blocos)))

    def _safe_load(self, name: str) -> pd.DataFrame:
        try:
            df = self.data_handler.load_table(name)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception:
            return pd.DataFrame()