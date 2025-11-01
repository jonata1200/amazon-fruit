# modules/report/report_charts.py
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

BG = '#232323'      # fundo escuro do dashboard (estilo)
FG = '#F9F9F9'      # fundo claro p/ PDF; usamos no figure/axes para suavizar

# -------- util --------
def _image_fit(png_bytes, max_w_in=6.2, max_h_in=3.6):
    reader = ImageReader(io.BytesIO(png_bytes))
    iw, ih = reader.getSize()
    scale = min((max_w_in * inch) / iw, (max_h_in * inch) / ih)
    return Image(io.BytesIO(png_bytes), width=iw*scale, height=ih*scale)

def _save_plot(story, fig, max_w=6.2, max_h=3.2):
    buf = io.BytesIO()
    fig.savefig(buf, format='PNG', dpi=200, bbox_inches='tight')
    plt.close(fig)
    story.append(_image_fit(buf.getvalue(), max_w_in=max_w, max_h_in=max_h))
    story.append(Spacer(1, 8))

def _axes_style(fig, ax, title):
    fig.patch.set_facecolor('#F9F9F9')
    ax.set_facecolor('#F9F9F9')
    ax.set_title(title)
    ax.grid(axis='y', alpha=0.25)

# -------- FINANÇAS --------
def add_finance_charts(story, df):
    if df is None or df.empty:
        return
    _finance_rev_vs_exp(story, df)
    _finance_expense_pie(story, df)
    _finance_timeseries(story, df)

def _finance_rev_vs_exp(story, df):
    if not {'Valor','Tipo'}.issubset(df.columns): return
    t = df['Tipo'].astype(str).str.lower()
    v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
    receita = float(v[t.str.startswith('entrada')].sum())
    despesa = float(v[t.str.startswith('saída')].sum())

    fig, ax = plt.subplots(figsize=(6.2, 2.8), dpi=120)
    _axes_style(fig, ax, 'Receita vs. Despesas')
    ax.bar(['Receita','Despesas'], [receita, despesa], color=['#2E8B57', '#D62728'])
    _save_plot(story, fig)

def _finance_expense_pie(story, df):
    if not {'Categoria','Tipo','Valor'}.issubset(df.columns): return
    dd = df[df['Tipo'].astype(str).str.lower().str.startswith('saída')]
    if dd.empty: return
    s = dd.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5.2, 3.0), dpi=120)
    fig.patch.set_facecolor('#F9F9F9'); ax.set_facecolor('#F9F9F9')
    ax.pie(s.values, labels=s.index.astype(str), autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribuição de Despesas')
    _save_plot(story, fig, max_w=6.0, max_h=3.2)

def _finance_timeseries(story, df):
    if 'Data' not in df.columns or 'Valor' not in df.columns or 'Tipo' not in df.columns: return
    dfx = df.copy()
    dfx['Data'] = pd.to_datetime(dfx['Data'], errors='coerce'); dfx = dfx.dropna(subset=['Data'])
    dfx['signed'] = dfx.apply(lambda r: r['Valor'] if str(r.get('Tipo','')).lower().startswith('entrada')
                              else -abs(r['Valor']), axis=1)
    daily = dfx.groupby('Data')['signed'].sum().sort_index()
    if daily.empty: return
    fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=120)
    _axes_style(fig, ax, 'Fluxo Diário (Entradas - Saídas)')
    ax.plot(daily.index, daily.values, marker='o')
    fig.autofmt_xdate()
    _save_plot(story, fig)

# -------- ESTOQUE --------
def add_inventory_charts(story, df):
    if df is None or df.empty: return
    _inv_category_pie(story, df)
    _inv_low_stock_bar(story, df)

def _inv_category_pie(story, df):
    if 'Categoria' not in df.columns: return
    s = df['Categoria'].astype(str).value_counts()
    if s.empty: return
    fig, ax = plt.subplots(figsize=(5.0, 3.0), dpi=120)
    fig.patch.set_facecolor('#F9F9F9'); ax.set_facecolor('#F9F9F9')
    ax.pie(s.values, labels=s.index.astype(str), autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribuição por Categoria')
    _save_plot(story, fig, max_w=6.0, max_h=3.0)

def _inv_low_stock_bar(story, df):
    req = {'Nome_Produto','Quantidade_Estoque','Nivel_Minimo_Estoque'}
    if not req.issubset(df.columns): return
    dfx = df.copy()
    dfx['gap'] = pd.to_numeric(dfx['Nivel_Minimo_Estoque'], errors='coerce') - \
                 pd.to_numeric(dfx['Quantidade_Estoque'], errors='coerce')
    low = dfx[dfx['gap'] > 0].sort_values('gap', ascending=False).head(10)
    if low.empty: return
    fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=120)
    _axes_style(fig, ax, 'Itens com Estoque Baixo (gap)')
    ax.barh(low['Nome_Produto'].astype(str), low['gap'])
    ax.invert_yaxis()
    _save_plot(story, fig)

# -------- PÚBLICO-ALVO --------
def add_public_charts(story, df):
    if df is None or df.empty: return
    _public_location_bar(story, df)
    _public_gender_pie(story, df)

def _public_location_bar(story, df):
    if 'Localizacao' not in df.columns: return
    s = df['Localizacao'].astype(str).value_counts()
    if s.empty: return
    fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=120)
    _axes_style(fig, ax, 'Distribuição de Clientes por Localização')
    ax.bar(s.index.astype(str), s.values, color='#4B0082')
    ax.tick_params(axis='x', rotation=15)
    _save_plot(story, fig)

def _public_gender_pie(story, df):
    if 'Genero' not in df.columns: return
    s = df['Genero'].astype(str).value_counts()
    if s.empty: return
    fig, ax = plt.subplots(figsize=(5.0, 3.0), dpi=120)
    fig.patch.set_facecolor('#F9F9F9'); ax.set_facecolor('#F9F9F9')
    ax.pie(s.values, labels=s.index.astype(str), autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribuição por Gênero')
    _save_plot(story, fig, max_w=6.0, max_h=3.0)

# -------- FORNECEDORES --------
def add_suppliers_charts(story, df):
    if df is None or df.empty: return
    _suppliers_rating_hbar(story, df)
    _suppliers_types_pie(story, df)

def _suppliers_rating_hbar(story, df):
    if {'Nome_Fornecedor','Avaliacao'}.issubset(df.columns):
        dfx = df.copy()
        dfx['Avaliacao'] = pd.to_numeric(dfx['Avaliacao'], errors='coerce')
        dfx = dfx.dropna(subset=['Avaliacao'])
        if dfx.empty: return
        fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=120)
        _axes_style(fig, ax, 'Avaliação dos Fornecedores')
        ax.barh(dfx['Nome_Fornecedor'].astype(str), dfx['Avaliacao'], color='#2E8B57')
        ax.set_xlim(0, 5)
        ax.invert_yaxis()
        _save_plot(story, fig)

def _suppliers_types_pie(story, df):
    if 'Produtos_Fornecidos' not in df.columns: return
    # separa por vírgula e conta tipos
    all_types = []
    for x in df['Produtos_Fornecidos'].dropna().astype(str):
        all_types += [t.strip() for t in x.split(',')]
    if not all_types: return
    s = pd.Series(all_types).value_counts()
    fig, ax = plt.subplots(figsize=(5.4, 3.0), dpi=120)
    fig.patch.set_facecolor('#F9F9F9'); ax.set_facecolor('#F9F9F9')
    ax.pie(s.values, labels=s.index.astype(str), autopct='%1.1f%%', startangle=90)
    ax.set_title('Tipos de Produtos Fornecidos')
    _save_plot(story, fig, max_w=6.0, max_h=3.2)

# -------- RH --------
def add_hr_charts(story, df):
    if df is None or df.empty: return
    _hr_salary_by_employee(story, df)

def _hr_salary_by_employee(story, df):
    if {'Nome_Funcionario','Salario'}.issubset(df.columns):
        dfx = df.copy()
        dfx['Salario'] = pd.to_numeric(dfx['Salario'], errors='coerce')
        dfx = dfx.dropna(subset=['Salario'])
        if dfx.empty: return
        fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=120)
        _axes_style(fig, ax, 'Salários por Funcionário')
        ax.bar(dfx['Nome_Funcionario'].astype(str), dfx['Salario'], color='#4B0082')
        ax.tick_params(axis='x', rotation=25)
        _save_plot(story, fig)