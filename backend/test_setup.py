# backend/test_setup.py
"""
Script simples para testar se a estrutura básica está funcionando
"""

import sys
from pathlib import Path

def test_imports():
    """Testa se os imports básicos funcionam"""
    print("Testando imports...")
    try:
        from app.main import app
        from app.config import settings
        print("[OK] Imports funcionando corretamente!")
        return True
    except Exception as e:
        print(f"[ERRO] Erro nos imports: {e}")
        return False

def test_structure():
    """Testa se a estrutura de pastas está correta"""
    print("\nTestando estrutura de pastas...")
    base_path = Path(__file__).parent
    
    required_paths = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/api/__init__.py",
        "app/api/routes/__init__.py",
        "app/services/__init__.py",
        "requirements.txt"
    ]
    
    all_ok = True
    for path_str in required_paths:
        path = base_path / path_str
        if path.exists():
            print(f"[OK] {path_str}")
        else:
            print(f"[ERRO] {path_str} nao encontrado")
            all_ok = False
    
    return all_ok

def test_config():
    """Testa se as configurações estão funcionando"""
    print("\nTestando configurações...")
    try:
        from app.config import settings
        print(f"[OK] Ambiente: {settings.environment}")
        print(f"[OK] Debug: {settings.debug}")
        print(f"[OK] DB Path: {settings.db_path}")
        print(f"[OK] API Host: {settings.api_host}")
        print(f"[OK] API Port: {settings.api_port}")
        return True
    except Exception as e:
        print(f"[ERRO] Erro nas configuracoes: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TESTE DE CONFIGURAÇÃO - FASE 1")
    print("=" * 50)
    
    results = []
    results.append(("Estrutura", test_structure()))
    results.append(("Configurações", test_config()))
    results.append(("Imports", test_imports()))
    
    print("\n" + "=" * 50)
    print("RESUMO:")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "[OK] PASSOU" if result else "[ERRO] FALHOU"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("[OK] Todos os testes passaram! Pronto para proxima etapa.")
        sys.exit(0)
    else:
        print("[ERRO] Alguns testes falharam. Revise os erros acima.")
        sys.exit(1)

