# modules/report/report_formatter.py

import pandas as pd
from ..utils.formatters import fmt_currency

def format_df_for_report(df_original: pd.DataFrame, table_name: str):
    """Prepara e formata um DataFrame para exibição no relatório PDF."""
    if df_original is None or df_original.empty:
        return pd.DataFrame()
    
    df = df_original.copy()
    
    format_map = {
        "Estoque": format_estoque,
        "Financas": format_financas,
        "Publico_Alvo": format_publico,
        "Fornecedores": format_fornecedores,
        "Recursos_Humanos": format_rh
    }
    
    formatter = format_map.get(table_name)
    if formatter:
        return formatter(df)
    return df

def format_estoque(df):
    for col in ["Data_Validade", "Data_Venda"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime("%d/%m/%Y")
    for col in ["Preco_Custo", "Preco_Venda"]:
        if col in df.columns:
            df[col] = df[col].map(fmt_currency)
    
    rename_map = {
        "Produto": "Produto", "Categoria": "Cat.", "Quantidade_Estoque": "Qtd. Estoque",
        "Preco_Custo": "Custo", "Preco_Venda": "Venda", "Nivel_Minimo_Estoque": "Mín.",
        "Quantidade_Vendida": "Qtd. Vendida", "Data_Venda": "Data Venda"
    }
    df = df.rename(columns=rename_map)
    
    cols_to_show = ["Produto", "Cat.", "Qtd. Estoque", "Custo", "Venda", "Mín.", "Qtd. Vendida", "Data Venda"]
    return df[[col for col in cols_to_show if col in df.columns]]

def format_financas(df):
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors='coerce').dt.strftime("%d/%m/%Y")
    if "Valor" in df.columns:
        df["Valor"] = df["Valor"].map(fmt_currency)
    
    rename_map = {"Descricao": "Descrição", "Metodo_Pagamento": "Pagamento"}
    df = df.rename(columns=rename_map)
    
    cols_to_show = ["Data", "Tipo", "Categoria", "Descrição", "Valor", "Pagamento"]
    return df[[col for col in cols_to_show if col in df.columns]]

def format_publico(df):
    rename_map = {"Genero": "Gênero", "Canal_de_venda": "Canal de Venda", "Estado": "UF"}
    df = df.rename(columns=rename_map)
    
    cols_to_show = ["Nome", "Gênero", "Idade", "Cidade", "UF", "Canal de Venda"]
    return df[[col for col in cols_to_show if col in df.columns]]

def format_fornecedores(df):
    rename_map = {"Nome_Fornecedor": "Fornecedor", "Avaliacao": "Nota", "Produtos_Fornecidos": "Produtos"}
    df = df.rename(columns=rename_map)
    
    cols_to_show = ["Fornecedor", "Nota", "Cidade", "Estado", "Produtos"]
    return df[[col for col in cols_to_show if col in df.columns]]

def format_rh(df):
    if "Data_Contratacao" in df.columns:
        df["Data_Contratacao"] = pd.to_datetime(df["Data_Contratacao"], errors='coerce').dt.strftime("%d/%m/%Y")
    if "Salario" in df.columns:
        df["Salario"] = df["Salario"].map(fmt_currency)
        
    rename_map = {"Data_Contratacao": "Contratação", "Departamento": "Depto."}
    df = df.rename(columns=rename_map)
    
    cols_to_show = ["Nome", "Cargo", "Depto.", "Contratação", "Salario"]
    return df[[col for col in cols_to_show if col in df.columns]]