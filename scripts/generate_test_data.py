#!/usr/bin/env python3
"""
Script para gerar dados de teste mínimos para a aplicação Amazon Fruit.
Cria um banco de dados SQLite com dados básicos para testes.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import random

def create_test_database(db_path: Path):
    """Cria um banco de dados SQLite com dados de teste"""
    
    # Criar diretório se não existir
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Conectar ao banco (cria se não existir)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    print(f"📦 Criando banco de dados de teste em: {db_path}")
    
    # Criar tabelas
    print("📋 Criando tabelas...")
    
    # Tabela Financas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Financas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Data DATE,
            Categoria TEXT,
            Tipo TEXT,
            Valor REAL,
            Descricao TEXT
        )
    """)
    
    # Tabela Estoque
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Data DATE,
            Produto TEXT,
            Quantidade INTEGER,
            Valor_Unitario REAL,
            Categoria TEXT
        )
    """)
    
    # Tabela Publico_Alvo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Publico_Alvo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Data DATE,
            Cliente TEXT,
            Genero TEXT,
            Idade INTEGER,
            Cidade TEXT,
            Canal_Venda TEXT
        )
    """)
    
    # Tabela Fornecedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Fornecedor TEXT,
            Estado TEXT,
            Categoria TEXT,
            Avaliacao REAL,
            Contato TEXT
        )
    """)
    
    # Tabela Recursos_Humanos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recursos_Humanos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT,
            Departamento TEXT,
            Cargo TEXT,
            Salario REAL,
            Data_Admissao DATE
        )
    """)
    
    conn.commit()
    print("✅ Tabelas criadas")
    
    # Gerar dados de teste
    print("📊 Gerando dados de teste...")
    
    # Dados de Financas (últimos 12 meses)
    financas_data = []
    categorias = ["Vendas", "Marketing", "Operacional", "Administrativo"]
    tipos = ["Receita", "Despesa"]
    
    base_date = datetime.now() - timedelta(days=365)
    for i in range(100):
        date = base_date + timedelta(days=random.randint(0, 365))
        financas_data.append({
            "Data": date.strftime("%Y-%m-%d"),
            "Categoria": random.choice(categorias),
            "Tipo": random.choice(tipos),
            "Valor": round(random.uniform(100, 10000), 2),
            "Descricao": f"Transação {i+1}"
        })
    
    df_financas = pd.DataFrame(financas_data)
    df_financas.to_sql("Financas", conn, if_exists="append", index=False)
    print(f"  ✅ {len(financas_data)} registros em Financas")
    
    # Dados de Estoque
    produtos = ["Maçã", "Banana", "Laranja", "Uva", "Manga", "Abacaxi", "Melancia", "Morango"]
    estoque_data = []
    
    for i in range(50):
        date = base_date + timedelta(days=random.randint(0, 365))
        produto = random.choice(produtos)
        estoque_data.append({
            "Data": date.strftime("%Y-%m-%d"),
            "Produto": produto,
            "Quantidade": random.randint(10, 500),
            "Valor_Unitario": round(random.uniform(2, 15), 2),
            "Categoria": "Frutas"
        })
    
    df_estoque = pd.DataFrame(estoque_data)
    df_estoque.to_sql("Estoque", conn, if_exists="append", index=False)
    print(f"  ✅ {len(estoque_data)} registros em Estoque")
    
    # Dados de Publico_Alvo
    generos = ["Masculino", "Feminino", "Outro"]
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre"]
    canais = ["Online", "Loja Física", "Telefone", "App"]
    publico_data = []
    
    for i in range(80):
        date = base_date + timedelta(days=random.randint(0, 365))
        publico_data.append({
            "Data": date.strftime("%Y-%m-%d"),
            "Cliente": f"Cliente {i+1}",
            "Genero": random.choice(generos),
            "Idade": random.randint(18, 70),
            "Cidade": random.choice(cidades),
            "Canal_Venda": random.choice(canais)
        })
    
    df_publico = pd.DataFrame(publico_data)
    df_publico.to_sql("Publico_Alvo", conn, if_exists="append", index=False)
    print(f"  ✅ {len(publico_data)} registros em Publico_Alvo")
    
    # Dados de Fornecedores
    estados = ["SP", "RJ", "MG", "PR", "RS", "SC"]
    categorias_forn = ["Frutas", "Verduras", "Embalagens", "Transporte"]
    fornecedores_data = []
    
    for i in range(15):
        fornecedores_data.append({
            "Nome_Fornecedor": f"Fornecedor {i+1}",
            "Estado": random.choice(estados),
            "Categoria": random.choice(categorias_forn),
            "Avaliacao": round(random.uniform(3.0, 5.0), 1),
            "Contato": f"contato{i+1}@fornecedor.com"
        })
    
    df_fornecedores = pd.DataFrame(fornecedores_data)
    df_fornecedores.to_sql("Fornecedores", conn, if_exists="append", index=False)
    print(f"  ✅ {len(fornecedores_data)} registros em Fornecedores")
    
    # Dados de Recursos_Humanos
    departamentos = ["Vendas", "Marketing", "Operações", "RH", "Financeiro"]
    cargos = ["Analista", "Coordenador", "Gerente", "Diretor", "Assistente"]
    rh_data = []
    
    for i in range(30):
        date = base_date + timedelta(days=random.randint(0, 1000))
        rh_data.append({
            "Nome": f"Funcionário {i+1}",
            "Departamento": random.choice(departamentos),
            "Cargo": random.choice(cargos),
            "Salario": round(random.uniform(3000, 15000), 2),
            "Data_Admissao": date.strftime("%Y-%m-%d")
        })
    
    df_rh = pd.DataFrame(rh_data)
    df_rh.to_sql("Recursos_Humanos", conn, if_exists="append", index=False)
    print(f"  ✅ {len(rh_data)} registros em Recursos_Humanos")
    
    conn.close()
    print(f"\n✅ Banco de dados de teste criado com sucesso!")
    print(f"   Localização: {db_path}")
    print(f"   Total de registros: {len(financas_data) + len(estoque_data) + len(publico_data) + len(fornecedores_data) + len(rh_data)}")

if __name__ == "__main__":
    import sys
    
    # Determinar caminho do banco
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
    else:
        # Caminho padrão: data/amazon_fruit_test.db
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent
        db_path = project_root / "data" / "amazon_fruit_test.db"
    
    print("🚀 Gerador de Dados de Teste - Amazon Fruit\n")
    
    # Perguntar se deve sobrescrever banco existente
    if db_path.exists():
        resposta = input(f"⚠️  Banco de dados já existe em {db_path}\nDeseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada")
            sys.exit(0)
        db_path.unlink()
    
    try:
        create_test_database(db_path)
        print("\n✅ Dados de teste gerados com sucesso!")
        print("\n💡 Para usar este banco de dados:")
        print(f"   1. Copie para: data/amazon_fruit.db")
        print(f"   2. Ou configure DB_PATH={db_path} no .env")
    except Exception as e:
        print(f"\n❌ Erro ao gerar dados de teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

