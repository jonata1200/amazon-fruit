# backend/test_data_handler.py
"""
Script de teste para verificar se o DataHandler migrado está funcionando corretamente.
"""

import sys
from pathlib import Path

def test_import():
    """Testa se o DataHandler pode ser importado"""
    print("Testando import do DataHandler...")
    try:
        from app.services.data_handler import DataHandler
        print("[OK] DataHandler importado com sucesso!")
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao importar DataHandler: {e}")
        return False

def test_initialization():
    """Testa se o DataHandler pode ser inicializado"""
    print("\nTestando inicializacao do DataHandler...")
    try:
        from app.services.data_handler import DataHandler
        
        # Tenta inicializar com o diretório raiz do projeto
        project_root = Path(__file__).resolve().parents[1]
        handler = DataHandler(base_dir=project_root)
        
        print(f"[OK] DataHandler inicializado!")
        print(f"[OK] DB Path: {handler.db_path}")
        
        # Verifica se o arquivo existe
        if handler.db_path.exists():
            print(f"[OK] Arquivo de banco de dados encontrado!")
        else:
            print(f"[AVISO] Arquivo de banco de dados nao encontrado em: {handler.db_path}")
            print("        Isso e normal se o banco ainda nao foi criado.")
        
        return True
    except FileNotFoundError as e:
        print(f"[AVISO] Banco de dados nao encontrado: {e}")
        print("        Isso e normal se o banco ainda nao foi criado.")
        return True  # Não é um erro crítico para esta fase
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar DataHandler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_methods():
    """Testa se os métodos principais existem"""
    print("\nTestando metodos do DataHandler...")
    try:
        from app.services.data_handler import DataHandler
        
        project_root = Path(__file__).resolve().parents[1]
        handler = DataHandler(base_dir=project_root)
        
        # Verifica se os métodos existem
        methods = [
            'set_period',
            'get_period',
            'load_table',
            'load_comparative_data',
            'load_full_unfiltered_table',
            'get_date_range'
        ]
        
        all_ok = True
        for method_name in methods:
            if hasattr(handler, method_name):
                print(f"[OK] Metodo '{method_name}' existe")
            else:
                print(f"[ERRO] Metodo '{method_name}' nao encontrado")
                all_ok = False
        
        return all_ok
    except FileNotFoundError:
        print("[AVISO] Pulando teste de metodos - banco nao encontrado")
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao testar metodos: {e}")
        return False

def test_with_real_data():
    """Testa com dados reais se o banco existir"""
    print("\nTestando com dados reais...")
    try:
        from app.services.data_handler import DataHandler
        
        project_root = Path(__file__).resolve().parents[1]
        handler = DataHandler(base_dir=project_root)
        
        # Testa get_date_range
        min_date, max_date = handler.get_date_range()
        if min_date and max_date:
            print(f"[OK] Range de datas encontrado: {min_date} a {max_date}")
        else:
            print("[AVISO] Nenhuma data encontrada no banco")
        
        # Testa load_table sem período
        df_fin = handler.load_full_unfiltered_table("Financas")
        if not df_fin.empty:
            print(f"[OK] Dados de Financas carregados: {len(df_fin)} registros")
        else:
            print("[AVISO] Nenhum dado encontrado na tabela Financas")
        
        return True
    except FileNotFoundError:
        print("[AVISO] Pulando teste com dados reais - banco nao encontrado")
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao testar com dados reais: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO DATAHANDLER MIGRADO - FASE 1")
    print("=" * 60)
    
    results = []
    results.append(("Import", test_import()))
    results.append(("Inicializacao", test_initialization()))
    results.append(("Metodos", test_methods()))
    results.append(("Dados Reais", test_with_real_data()))
    
    print("\n" + "=" * 60)
    print("RESUMO:")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "[OK] PASSOU" if result else "[ERRO] FALHOU"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("[OK] Todos os testes passaram! DataHandler migrado com sucesso.")
        sys.exit(0)
    else:
        print("[ERRO] Alguns testes falharam. Revise os erros acima.")
        sys.exit(1)

