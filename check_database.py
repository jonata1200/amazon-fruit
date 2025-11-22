#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar dados no banco de dados"""

import sqlite3
from pathlib import Path

db_path = Path("data/amazon_fruit.db")

if not db_path.exists():
    print(f"[ERRO] Banco de dados nao encontrado em: {db_path}")
    exit(1)

print(f"[OK] Banco de dados encontrado: {db_path}\n")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Listar tabelas
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

if not tables:
    print("[AVISO] Nenhuma tabela encontrada no banco de dados!")
    conn.close()
    exit(0)

print("Tabelas encontradas:")
for table in tables:
    table_name = table[0]
    count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    status = "[OK]" if count > 0 else "[VAZIO]"
    print(f"  {status} {table_name}: {count} registros")

# Verificar range de datas
print("\nRange de datas disponivel:")
date_ranges = {
    'lancamentos_financeiros': 'Data',
    'estoque_historico': 'Data_Snapshot',
    'clientes': None,  # Não tem coluna de data
    'fornecedores': None,  # Não tem coluna de data
    'funcionarios': 'Data_Contratacao'
}

for table_name, date_col in date_ranges.items():
    if date_col:
        try:
            result = cursor.execute(f"SELECT MIN({date_col}), MAX({date_col}) FROM {table_name}").fetchone()
            if result and result[0]:
                print(f"  {table_name}: {result[0]} até {result[1]}")
        except:
            pass

conn.close()

print("\n[INFO] Se os dados estao zerados, execute o script de migracao:")
print("   python scripts/migrate_excel_to_sqlite.py")

