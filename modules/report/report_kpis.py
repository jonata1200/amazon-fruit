# modules/report/report_kpis.py
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
import math

# ---------- util ----------
def _fmt_currency(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"

def _kpi_table(story, items, colors_dict):
    """
    items: lista de dicts [{title, value, color?}]
    Renderiza cards KPI lado a lado.
    """
    data = []
    row = []
    # cada card é uma mini-tabela para título e valor centralizados
    for it in items:
        title = it["title"]
        value = it["value"]
        color = it.get("color", colors_dict["text"])

        card = [
            [Paragraph(f"<para align=center><font size=9 color='#AAAAAA'>{title}</font></para>")],
            [Paragraph(f"<para align=center><b><font size=12 color='{color}'>" +
                       (value if isinstance(value, str) else str(value)) +
                       "</font></b></para>")]
        ]
        t = Table(card, colWidths=[2.2*inch], rowHeights=[0.35*inch, 0.45*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.Color(0.97,0.97,0.98)),
            ('BOX', (0,0), (-1,-1), 0.7, colors.Color(0.88,0.88,0.92)),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        row.append(t)

    data.append(row)
    wrapper = Table(data, hAlign='LEFT', colWidths=[2.2*inch]*len(items))
    wrapper.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),
                                 ('RIGHTPADDING',(0,0),(-1,-1),12)]))
    story.append(wrapper)
    story.append(Spacer(1, 10))

# ---------- KPIs por seção ----------
def add_kpis_estoque(story, df, colors_dict):
    if df is None or df.empty: return
    uniq = df['ID_Produto'].nunique() if 'ID_Produto' in df.columns else len(df)
    valor_custo = 0.0
    if {'Quantidade_Estoque','Preco_Custo'}.issubset(df.columns):
        q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce').fillna(0)
        c = pd.to_numeric(df['Preco_Custo'], errors='coerce').fillna(0.0)
        valor_custo = float((q*c).sum())
    baixo = 0
    if {'Quantidade_Estoque','Nivel_Minimo_Estoque'}.issubset(df.columns):
        baixo = int((pd.to_numeric(df['Quantidade_Estoque'], errors='coerce') <=
                     pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')).sum())
    _kpi_table(story, [
        {"title":"Produtos Únicos", "value": str(uniq)},
        {"title":"Valor do Estoque (Custo)", "value": _fmt_currency(valor_custo), "color":"#2E8B57"},
        {"title":"Itens com Estoque Baixo", "value": str(baixo)}
    ], colors_dict)

def add_kpis_financas(story, df, colors_dict):
    if df is None or df.empty: return
    if not {'Valor','Tipo'}.issubset(df.columns): return
    tipo = df['Tipo'].astype(str).str.lower()
    val  = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
    receita = float(val[tipo.str.startswith('entrada')].sum())
    despesa = float(val[tipo.str.startswith('saída')].sum())
    lucro = receita - despesa
    _kpi_table(story, [
        {"title":"Receita Total", "value": _fmt_currency(receita), "color":"#2E8B57"},
        {"title":"Despesas Totais", "value": _fmt_currency(despesa), "color":"#D62728"},
        {"title":"Lucro Líquido", "value": _fmt_currency(lucro), "color":"#FF8C00"},
    ], colors_dict)

def add_kpis_publico(story, df, colors_dict):
    if df is None or df.empty: return
    total = len(df)
    idade_media = None
    if 'Idade' in df.columns:
        idade_media = pd.to_numeric(df['Idade'], errors='coerce').mean()
    gasto_medio = None
    if 'Gasto_Medio' in df.columns:
        gasto_medio = pd.to_numeric(df['Gasto_Medio'], errors='coerce').mean()
    _kpi_table(story, [
        {"title":"Total de Clientes", "value": str(total)},
        {"title":"Idade Média", "value": f"{idade_media:.1f} anos" if isinstance(idade_media, float) and not math.isnan(idade_media) else "—"},
        {"title":"Gasto Médio por Cliente", "value": _fmt_currency(gasto_medio) if gasto_medio is not None else "—"},
    ], colors_dict)

def add_kpis_fornecedores(story, df, colors_dict):
    if df is None or df.empty: return
    total = len(df)
    aval = None
    if 'Avaliacao' in df.columns:
        aval = pd.to_numeric(df['Avaliacao'], errors='coerce').mean()
    _kpi_table(story, [
        {"title":"Total de Fornecedores", "value": str(total)},
        {"title":"Avaliação Média", "value": f"{aval:.1f} / 5 ★" if aval is not None and not math.isnan(aval) else "—"},
    ], colors_dict)

def add_kpis_rh(story, df, colors_dict):
    if df is None or df.empty: return
    total = len(df)
    custo_mensal = 0.0
    if 'Salario' in df.columns:
        custo_mensal = pd.to_numeric(df['Salario'], errors='coerce').fillna(0.0).sum()
    _kpi_table(story, [
        {"title":"Total de Funcionários", "value": str(total)},
        {"title":"Custo Mensal da Equipe", "value": _fmt_currency(custo_mensal)},
    ], colors_dict)