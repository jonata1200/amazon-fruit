from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Helpers visuais
# ---------------------------------------------------------
def brl(v: float | int | None) -> str:
    if v is None or pd.isna(v):
        v = 0.0
    try:
        v = float(v)
    except Exception:
        v = 0.0
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class InsightCard(QFrame):
    def __init__(self, title: str, value: str = "", subtitle: str = "", accent: str = "#00BFFF"):
        super().__init__()
        self.title_lbl = QLabel(title)
        self.value_lbl = QLabel(value)
        self.subtitle_lbl = QLabel(subtitle)

        self.setObjectName("InsightCard")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(4)

        self.title_lbl.setObjectName("CardTitle")
        self.value_lbl.setObjectName("CardValue")
        self.subtitle_lbl.setObjectName("CardSubtitle")

        lay.addWidget(self.title_lbl)
        lay.addWidget(self.value_lbl)
        lay.addWidget(self.subtitle_lbl)

        # cor de destaque por card
        self.setProperty("accent", accent)
        self._apply_styles(accent)

    def _apply_styles(self, accent: str):
        self.setStyleSheet(f"""
            QFrame#InsightCard {{
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 10px;
                background-color: rgba(255,255,255,0.04);
            }}
            QLabel#CardTitle {{
                color: {accent};
                font-size: 12pt;
                font-weight: 600;
            }}
            QLabel#CardValue {{
                color: #FFFFFF;
                font-size: 20pt;
                font-weight: 700;
            }}
            QLabel#CardSubtitle {{
                color: #B8C0CC;
                font-size: 10pt;
            }}
        """)

    def set_value(self, txt: str):
        self.value_lbl.setText(txt)

    def set_subtitle(self, txt: str):
        self.subtitle_lbl.setText(txt)


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------
class DashboardInsights(QWidget):
    def __init__(self, data_handler, theme: str):
        super().__init__()
        self.data_handler = data_handler
        self.theme = theme if theme in ("dark", "light") else "dark"

        self.cards = {}
        self._setup_ui()
        self.update_theme(self.theme)   # aplica tema inicial
        self.refresh()

    # ---------- UI ----------
    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("📊 Insights do Negócio")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setObjectName("InsightsTitle")
        root.addWidget(title)

        # Grade de cards
        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        # Linha 1
        self.cards["lucro_total"] = InsightCard("Lucro Total", accent="#14C38E")
        self.cards["receita_total"] = InsightCard("Receita Total", accent="#00BFFF")
        self.cards["despesa_total"] = InsightCard("Despesas Totais", accent="#FF6B6B")
        grid.addWidget(self.cards["lucro_total"],   0, 0)
        grid.addWidget(self.cards["receita_total"], 0, 1)
        grid.addWidget(self.cards["despesa_total"], 0, 2)

        # Linha 2
        self.cards["rupturas"] = InsightCard("Itens em Ruptura (<= mínimo)", accent="#FFD166")
        self.cards["pct_fem"]  = InsightCard("% Feminino (Clientes)", accent="#C77DFF")
        self.cards["rating"]   = InsightCard("Avaliação Média Fornecedores", accent="#4DD0E1")
        grid.addWidget(self.cards["rupturas"], 1, 0)
        grid.addWidget(self.cards["pct_fem"],  1, 1)
        grid.addWidget(self.cards["rating"],   1, 2)

        root.addLayout(grid)

        # Caixa de highlights (texto)
        self.highlights = QLabel("")
        self.highlights.setWordWrap(True)
        self.highlights.setObjectName("HighlightsBox")
        self.highlights.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.highlights.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        root.addWidget(self.highlights)

        self.setLayout(root)

    # ---------- Tema ----------
    def update_theme(self, new_theme: str):
        self.theme = new_theme
        if self.theme == "dark":
            self.setStyleSheet("""
                QWidget#dummy{} /* placeholder para permitir várias regras */

                QLabel#InsightsTitle {
                    color: #E6E6E6;
                }
                QLabel#HighlightsBox {
                    background-color: #14181F;
                    border: 1px solid #2B2F36;
                    border-radius: 10px;
                    padding: 12px;
                    color: #D8DEE9;
                    font-size: 11pt;
                }
            """)
            # Ajustar cor do valor nos cards para dark
            for c in self.cards.values():
                c._apply_styles(c.property("accent"))
        else:
            self.setStyleSheet("""
                QWidget#dummy{}

                QLabel#InsightsTitle {
                    color: #1A1A1A;
                }
                QLabel#HighlightsBox {
                    background-color: #FFFFFF;
                    border: 1px solid #E6E6E6;
                    border-radius: 10px;
                    padding: 12px;
                    color: #333333;
                    font-size: 11pt;
                }
            """)
            for c in self.cards.values():
                c._apply_styles(c.property("accent"))

    # ---------- Dados / Insights ----------
    def refresh(self):
        # --- Finanças ---
        df_fin = self._safe_load("Financas")
        receita_total, despesa_total, lucro_total = 0.0, 0.0, 0.0
        lucros_ult_mes, lucros_ant_mes, conclusao = None, None, ""

        if not df_fin.empty:
            # Normaliza tipos
            if "Valor" in df_fin.columns:
                df_fin["Valor"] = pd.to_numeric(df_fin["Valor"], errors="coerce").fillna(0.0)
            if "Tipo" in df_fin.columns:
                receita_total = df_fin.loc[df_fin["Tipo"].astype(str).str.lower().eq("receita"), "Valor"].sum()
                despesa_total = df_fin.loc[df_fin["Tipo"].astype(str).str.lower().eq("despesa"), "Valor"].sum()
                lucro_total = receita_total - despesa_total

            # Lucro por mês (se houver Data)
            if "Data" in df_fin.columns:
                dfx = df_fin.dropna(subset=["Data"]).copy()
                try:
                    dfx["Data"] = pd.to_datetime(dfx["Data"], errors="coerce")
                    dfx["AnoMes"] = dfx["Data"].dt.to_period("M").astype(str)
                    grp = dfx.groupby(["AnoMes", "Tipo"])["Valor"].sum().unstack(fill_value=0)
                    grp["Lucro"] = grp.get("Receita", 0) - grp.get("Despesa", 0)
                    if not grp.empty:
                        lucros = grp["Lucro"].sort_index()
                        if len(lucros) >= 1:
                            lucros_ult_mes = float(lucros.iloc[-1])
                        if len(lucros) >= 2:
                            lucros_ant_mes = float(lucros.iloc[-2])
                        if lucros_ult_mes is not None and lucros_ant_mes is not None:
                            diff = lucros_ult_mes - lucros_ant_mes
                            sinal = "↑" if diff >= 0 else "↓"
                            conclusao = f"Tendência do lucro: {sinal} {brl(abs(diff))} vs. mês anterior."
                except Exception:
                    pass

        # --- Estoque ---
        df_est = self._safe_load("Estoque")
        rupturas = 0
        if not df_est.empty and {"Quantidade_Estoque", "Nivel_Minimo_Estoque"}.issubset(df_est.columns):
            q = pd.to_numeric(df_est["Quantidade_Estoque"], errors="coerce")
            n = pd.to_numeric(df_est["Nivel_Minimo_Estoque"], errors="coerce")
            rupturas = int((q <= n).sum())

        # --- Público-alvo ---
        df_pub = self._safe_load("Publico_Alvo")
        pct_fem = None
        if not df_pub.empty and "Genero" in df_pub.columns:
            total = len(df_pub)
            fem = (df_pub["Genero"].astype(str).str.lower() == "feminino").sum()
            if total > 0:
                pct_fem = 100.0 * fem / total

        # --- Fornecedores ---
        df_forn = self._safe_load("Fornecedores")
        rating = None
        if not df_forn.empty and "Avaliacao" in df_forn.columns:
            rating = pd.to_numeric(df_forn["Avaliacao"], errors="coerce").dropna()
            rating = float(rating.mean()) if not rating.empty else None

        # Atualiza cards
        self.cards["lucro_total"].set_value(brl(lucro_total))
        self.cards["lucro_total"].set_subtitle(conclusao or "Resumo consolidado do período carregado.")

        self.cards["receita_total"].set_value(brl(receita_total))
        self.cards["despesa_total"].set_value(brl(despesa_total))
        self.cards["rupturas"].set_value(str(rupturas))

        self.cards["pct_fem"].set_value(f"{pct_fem:.1f}%" if pct_fem is not None else "—")
        self.cards["pct_fem"].set_subtitle("Participação de clientes do gênero feminino.")

        self.cards["rating"].set_value(f"{rating:.2f}" if rating is not None else "—")
        self.cards["rating"].set_subtitle("Média das avaliações dos fornecedores.")

        # Highlights em texto
        blocos = []

        blocos.append(f"💰 <b>Financeiro</b><br>"
                      f"Receita total: <b>{brl(receita_total)}</b> · "
                      f"Despesas totais: <b>{brl(despesa_total)}</b> · "
                      f"Lucro total: <b>{brl(lucro_total)}</b>")

        if conclusao:
            blocos.append(f"📈 <b>Tendência</b><br>{conclusao}")

        blocos.append(f"📦 <b>Estoque</b><br>"
                      f"Itens em ruptura (≤ mínimo): <b>{rupturas}</b>")

        if pct_fem is not None:
            blocos.append(f"👥 <b>Público</b><br>"
                          f"Clientes do gênero feminino: <b>{pct_fem:.1f}%</b>")

        if rating is not None:
            blocos.append(f"🤝 <b>Fornecedores</b><br>"
                          f"Avaliação média: <b>{rating:.2f}</b>")

        self.highlights.setText("<br><br>".join(blocos))

    # ---------- Loader seguro ----------
    def _safe_load(self, name: str) -> pd.DataFrame:
        try:
            df = self.data_handler.load_table(name)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception:
            return pd.DataFrame()