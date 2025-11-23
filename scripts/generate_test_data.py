#!/usr/bin/env python3
"""
Script para gerar dados de teste robustos para a aplicação Amazon Fruit.
Cria um banco de dados SQLite com dados apenas de 2024 e 2025.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import random

def create_test_database(db_path: Path):
    """Cria um banco de dados SQLite com dados de teste robustos"""
    
    # Criar diretório se não existir
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Conectar ao banco (cria se não existir)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    print(f"📦 Criando banco de dados de teste em: {db_path}")
    
    # Criar tabelas
    print("📋 Criando tabelas...")
    
    # Limpar tabelas existentes
    cursor.execute("DROP TABLE IF EXISTS Financas")
    cursor.execute("DROP TABLE IF EXISTS Estoque")
    cursor.execute("DROP TABLE IF EXISTS Publico_Alvo")
    cursor.execute("DROP TABLE IF EXISTS Fornecedores")
    cursor.execute("DROP TABLE IF EXISTS Recursos_Humanos")
    
    # Tabela Financas
    cursor.execute("""
        CREATE TABLE Financas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Data DATE,
            Categoria TEXT,
            Tipo TEXT,
            Valor REAL,
            Descricao TEXT
        )
    """)
    
    # Tabela Estoque (estrutura completa)
    cursor.execute("""
        CREATE TABLE Estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Produto INTEGER,
            Produto TEXT,
            Nome_Produto TEXT,
            Quantidade_Estoque INTEGER,
            Nivel_Minimo_Estoque INTEGER,
            Preco_Custo REAL,
            Preco_Venda REAL,
            Quantidade_Vendida INTEGER,
            Data_Snapshot DATE,
            Data_Validade DATE,
            Categoria TEXT,
            Ano INTEGER,
            Mes INTEGER
        )
    """)
    
    # Tabela Publico_Alvo
    cursor.execute("""
        CREATE TABLE Publico_Alvo (
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
        CREATE TABLE Fornecedores (
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
        CREATE TABLE Recursos_Humanos (
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
    print("📊 Gerando dados de teste (2024-2025)...")
    
    # ============================================================================
    # DADOS DE FINANÇAS (2024-2025)
    # ============================================================================
    financas_data = []
    categorias = ["Vendas", "Marketing", "Operacional", "Administrativo"]
    tipos = ["Receita", "Despesa"]
    
    # Gerar dados para cada mês de 2024 e 2025
    for ano in [2024, 2025]:
        for mes in range(1, 13):
            # Último dia do mês
            if mes == 12:
                ultimo_dia = 31
            elif mes in [4, 6, 9, 11]:
                ultimo_dia = 30
            elif mes == 2:
                ultimo_dia = 29 if ano == 2024 else 28
            else:
                ultimo_dia = 31
            
            # Gerar 15-25 transações por mês
            num_transacoes = random.randint(15, 25)
            for i in range(num_transacoes):
                dia = random.randint(1, ultimo_dia)
                date = datetime(ano, mes, dia)
                
                # Distribuição: 60% Receita, 40% Despesa
                tipo = random.choices(tipos, weights=[60, 40])[0]
                
                # Valores diferentes para receita e despesa
                if tipo == "Receita":
                    valor = round(random.uniform(500, 15000), 2)
                else:
                    valor = round(random.uniform(200, 8000), 2)
                
                financas_data.append({
                    "Data": date.strftime("%Y-%m-%d"),
                    "Categoria": random.choice(categorias),
                    "Tipo": tipo,
                    "Valor": valor,
                    "Descricao": f"Transação {tipo} - {categorias[0]} - {date.strftime('%m/%Y')}"
                })
    
    df_financas = pd.DataFrame(financas_data)
    df_financas.to_sql("Financas", conn, if_exists="append", index=False)
    print(f"  ✅ {len(financas_data)} registros em Financas")
    
    # ============================================================================
    # DADOS DE ESTOQUE (2024-2025) - Estrutura completa
    # ============================================================================
    produtos_info = [
        {"ID": 1, "Nome": "Maçã Gala", "Categoria": "Frutas", "Preco_Custo": 3.50, "Preco_Venda": 5.90, "Nivel_Minimo": 100},
        {"ID": 2, "Nome": "Banana Prata", "Categoria": "Frutas", "Preco_Custo": 2.80, "Preco_Venda": 4.50, "Nivel_Minimo": 150},
        {"ID": 3, "Nome": "Laranja Lima", "Categoria": "Frutas", "Preco_Custo": 2.20, "Preco_Venda": 3.80, "Nivel_Minimo": 120},
        {"ID": 4, "Nome": "Uva Itália", "Categoria": "Frutas", "Preco_Custo": 8.50, "Preco_Venda": 12.90, "Nivel_Minimo": 80},
        {"ID": 5, "Nome": "Manga Palmer", "Categoria": "Frutas", "Preco_Custo": 4.20, "Preco_Venda": 6.50, "Nivel_Minimo": 90},
        {"ID": 6, "Nome": "Abacaxi Pérola", "Categoria": "Frutas", "Preco_Custo": 3.80, "Preco_Venda": 5.90, "Nivel_Minimo": 70},
        {"ID": 7, "Nome": "Melancia", "Categoria": "Frutas", "Preco_Custo": 1.80, "Preco_Venda": 2.90, "Nivel_Minimo": 60},
        {"ID": 8, "Nome": "Morango", "Categoria": "Frutas", "Preco_Custo": 12.00, "Preco_Venda": 18.90, "Nivel_Minimo": 50},
        {"ID": 9, "Nome": "Limão Taiti", "Categoria": "Frutas", "Preco_Custo": 2.50, "Preco_Venda": 4.20, "Nivel_Minimo": 100},
        {"ID": 10, "Nome": "Pera Williams", "Categoria": "Frutas", "Preco_Custo": 5.50, "Preco_Venda": 8.90, "Nivel_Minimo": 75},
        {"ID": 11, "Nome": "Kiwi", "Categoria": "Frutas", "Preco_Custo": 6.80, "Preco_Venda": 10.50, "Nivel_Minimo": 40},
        {"ID": 12, "Nome": "Mamão Papaya", "Categoria": "Frutas", "Preco_Custo": 2.20, "Preco_Venda": 3.50, "Nivel_Minimo": 85},
    ]
    
    estoque_data = []
    
    # Gerar snapshot mensal para cada produto em 2024 e 2025
    for ano in [2024, 2025]:
        for mes in range(1, 13):
            # Último dia do mês
            if mes == 12:
                ultimo_dia = 31
            elif mes in [4, 6, 9, 11]:
                ultimo_dia = 30
            elif mes == 2:
                ultimo_dia = 29 if ano == 2024 else 28
            else:
                ultimo_dia = 31
            
            data_snapshot = datetime(ano, mes, ultimo_dia)
            
            for produto in produtos_info:
                # Quantidade em estoque varia ao longo do tempo
                base_quantidade = produto["Nivel_Minimo"] * random.uniform(1.5, 3.0)
                quantidade_estoque = max(int(base_quantidade), produto["Nivel_Minimo"] - random.randint(0, 30))
                
                # Quantidade vendida varia por produto e mês
                quantidade_vendida = random.randint(
                    int(produto["Nivel_Minimo"] * 0.3),
                    int(produto["Nivel_Minimo"] * 1.5)
                )
                
                # Data de validade (30-60 dias após snapshot)
                dias_validade = random.randint(30, 60)
                data_validade = data_snapshot + timedelta(days=dias_validade)
                
                estoque_data.append({
                    "ID_Produto": produto["ID"],
                    "Produto": produto["Nome"],
                    "Nome_Produto": produto["Nome"],
                    "Quantidade_Estoque": quantidade_estoque,
                    "Nivel_Minimo_Estoque": produto["Nivel_Minimo"],
                    "Preco_Custo": produto["Preco_Custo"],
                    "Preco_Venda": produto["Preco_Venda"],
                    "Quantidade_Vendida": quantidade_vendida,
                    "Data_Snapshot": data_snapshot.strftime("%Y-%m-%d"),
                    "Data_Validade": data_validade.strftime("%Y-%m-%d"),
                    "Categoria": produto["Categoria"],
                    "Ano": ano,
                    "Mes": mes
                })
    
    df_estoque = pd.DataFrame(estoque_data)
    df_estoque.to_sql("Estoque", conn, if_exists="append", index=False)
    print(f"  ✅ {len(estoque_data)} registros em Estoque")
    
    # ============================================================================
    # DADOS DE PÚBLICO-ALVO (2024-2025)
    # ============================================================================
    generos = ["Masculino", "Feminino", "Outro"]
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre", 
               "Brasília", "Salvador", "Fortaleza", "Recife", "Manaus"]
    canais = ["Online", "Loja Física", "Telefone", "App"]
    publico_data = []
    
    # Gerar dados para cada mês de 2024 e 2025
    for ano in [2024, 2025]:
        for mes in range(1, 13):
            # Último dia do mês
            if mes == 12:
                ultimo_dia = 31
            elif mes in [4, 6, 9, 11]:
                ultimo_dia = 30
            elif mes == 2:
                ultimo_dia = 29 if ano == 2024 else 28
            else:
                ultimo_dia = 31
            
            # 20-30 clientes por mês
            num_clientes = random.randint(20, 30)
            for i in range(num_clientes):
                dia = random.randint(1, ultimo_dia)
                date = datetime(ano, mes, dia)
                
                publico_data.append({
                    "Data": date.strftime("%Y-%m-%d"),
                    "Cliente": f"Cliente {random.randint(1000, 9999)}",
                    "Genero": random.choice(generos),
                    "Idade": random.randint(18, 70),
                    "Cidade": random.choice(cidades),
                    "Canal_Venda": random.choice(canais)
                })
    
    df_publico = pd.DataFrame(publico_data)
    df_publico.to_sql("Publico_Alvo", conn, if_exists="append", index=False)
    print(f"  ✅ {len(publico_data)} registros em Publico_Alvo")
    
    # ============================================================================
    # DADOS DE FORNECEDORES (sem data)
    # ============================================================================
    estados = ["SP", "RJ", "MG", "PR", "RS", "SC", "BA", "GO", "PE", "CE"]
    categorias_forn = ["Frutas", "Verduras", "Embalagens", "Transporte", "Equipamentos"]
    nomes_fornecedores = [
        "Agro Frutas Sul", "Distribuidora Norte", "Hortifruti Central", "Frutas Premium",
        "Distribuidora Oeste", "Agro Verde", "Frutas do Vale", "Hortifruti Express",
        "Distribuidora Leste", "Agro Brasil", "Frutas Frescas", "Hortifruti Plus",
        "Distribuidora Sul", "Agro Premium", "Frutas Naturais"
    ]
    
    fornecedores_data = []
    for i, nome in enumerate(nomes_fornecedores[:15]):
        fornecedores_data.append({
            "Nome_Fornecedor": nome,
            "Estado": random.choice(estados),
            "Categoria": random.choice(categorias_forn),
            "Avaliacao": round(random.uniform(3.5, 5.0), 1),
            "Contato": f"contato{nome.lower().replace(' ', '')}@fornecedor.com"
        })
    
    df_fornecedores = pd.DataFrame(fornecedores_data)
    df_fornecedores.to_sql("Fornecedores", conn, if_exists="append", index=False)
    print(f"  ✅ {len(fornecedores_data)} registros em Fornecedores")
    
    # ============================================================================
    # DADOS DE RECURSOS HUMANOS (2024-2025)
    # ============================================================================
    departamentos = ["Vendas", "Marketing", "Operações", "RH", "Financeiro", "TI", "Logística"]
    cargos = ["Analista", "Coordenador", "Gerente", "Diretor", "Assistente", "Supervisor"]
    nomes_funcionarios = [
        "Ana Silva", "Carlos Santos", "Maria Oliveira", "João Pereira", "Fernanda Costa",
        "Ricardo Alves", "Juliana Lima", "Paulo Souza", "Patricia Rocha", "Marcos Ferreira",
        "Luciana Martins", "Roberto Dias", "Camila Araujo", "Felipe Ribeiro", "Amanda Correia",
        "Bruno Gomes", "Larissa Barbosa", "Thiago Cardoso", "Vanessa Nunes", "Gabriel Moreira",
        "Isabela Teixeira", "Rafael Monteiro", "Beatriz Carvalho", "Diego Ramos", "Mariana Lopes",
        "Gustavo Azevedo", "Renata Cunha", "André Freitas", "Tatiana Mendes", "Leandro Duarte"
    ]
    
    rh_data = []
    for i, nome in enumerate(nomes_funcionarios):
        # Admissões distribuídas entre 2020-2024
        ano_admissao = random.randint(2020, 2024)
        mes_admissao = random.randint(1, 12)
        dia_admissao = random.randint(1, 28)
        date = datetime(ano_admissao, mes_admissao, dia_admissao)
        
        rh_data.append({
            "Nome": nome,
            "Departamento": random.choice(departamentos),
            "Cargo": random.choice(cargos),
            "Salario": round(random.uniform(3500, 18000), 2),
            "Data_Admissao": date.strftime("%Y-%m-%d")
        })
    
    df_rh = pd.DataFrame(rh_data)
    df_rh.to_sql("Recursos_Humanos", conn, if_exists="append", index=False)
    print(f"  ✅ {len(rh_data)} registros em Recursos_Humanos")
    
    conn.close()
    
    total_registros = len(financas_data) + len(estoque_data) + len(publico_data) + len(fornecedores_data) + len(rh_data)
    print(f"\n✅ Banco de dados de teste criado com sucesso!")
    print(f"   Localização: {db_path}")
    print(f"   Total de registros: {total_registros}")
    print(f"   Período: 2024-2025")

if __name__ == "__main__":
    import sys
    
    # Determinar caminho do banco
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
    else:
        # Caminho padrão: data/amazon_fruit.db
        script_dir = Path(__file__).resolve().parent
        project_root = script_dir.parent
        db_path = project_root / "data" / "amazon_fruit.db"
    
    print("🚀 Gerador de Dados de Teste - Amazon Fruit")
    print("   Período: 2024-2025\n")
    
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
        print("\n💡 O banco de dados está pronto para uso!")
    except Exception as e:
        print(f"\n❌ Erro ao gerar dados de teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
