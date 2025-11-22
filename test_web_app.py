#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste Automatizado - Amazon Fruit Web App
Testa todos os componentes da aplicação web
"""

import requests
import json
import sys
from datetime import datetime
from pathlib import Path

# Configurações
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

# Cores para output (Windows compatible)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}[ERRO] {text}{Colors.RESET}")

def print_warning(text):
    """Imprime mensagem de aviso"""
    print(f"{Colors.YELLOW}[AVISO] {text}{Colors.RESET}")

def print_info(text):
    """Imprime informação"""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

def test_server_connection():
    """Testa se o servidor está rodando"""
    print_header("TESTE 1: Conexão com o Servidor")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Servidor está rodando e respondendo")
            print_info(f"Status: {data.get('status', 'N/A')}")
            print_info(f"Mensagem: {data.get('message', 'N/A')}")
            return True
        else:
            print_error(f"Servidor retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar ao servidor")
        print_warning("Certifique-se de que o servidor está rodando:")
        print_warning("  cd backend")
        print_warning("  uvicorn app.main:app --reload --host localhost --port 8000")
        return False
    except Exception as e:
        print_error(f"Erro ao conectar: {str(e)}")
        return False

def test_root_endpoint():
    """Testa o endpoint raiz"""
    print_header("TESTE 2: Endpoint Raiz (/)")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            content = response.text
            if "base.html" in content or "Amazon Fruit" in content:
                print_success("Endpoint raiz retornando HTML corretamente")
                print_info(f"Tamanho da resposta: {len(content)} bytes")
                return True
            else:
                print_warning("Endpoint raiz retornou HTML, mas conteúdo pode estar incompleto")
                return True
        else:
            print_error(f"Endpoint raiz retornou status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro ao testar endpoint raiz: {str(e)}")
        return False

def test_static_files():
    """Testa se os arquivos estáticos estão sendo servidos"""
    print_header("TESTE 3: Arquivos Estáticos")
    
    static_files = [
        "/static/css/main.css",
        "/static/js/app.js"
    ]
    
    all_ok = True
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}", timeout=TIMEOUT)
            if response.status_code == 200:
                print_success(f"Arquivo estático encontrado: {file_path}")
            else:
                print_error(f"Arquivo estático não encontrado: {file_path} (Status: {response.status_code})")
                all_ok = False
        except Exception as e:
            print_error(f"Erro ao testar {file_path}: {str(e)}")
            all_ok = False
    
    return all_ok

def test_templates():
    """Testa se os templates HTML estão sendo servidos"""
    print_header("TESTE 4: Templates HTML")
    
    templates = [
        "geral",
        "financas",
        "estoque",
        "publico_alvo",
        "fornecedores",
        "recursos_humanos"
    ]
    
    all_ok = True
    for template in templates:
        try:
            response = requests.get(f"{BASE_URL}/templates/dashboards/{template}.html", timeout=TIMEOUT)
            if response.status_code == 200:
                content = response.text
                if len(content) > 100:  # Verifica se tem conteúdo significativo
                    print_success(f"Template encontrado: {template}.html ({len(content)} bytes)")
                else:
                    print_warning(f"Template {template}.html muito pequeno ({len(content)} bytes)")
            else:
                print_error(f"Template não encontrado: {template}.html (Status: {response.status_code})")
                all_ok = False
        except Exception as e:
            print_error(f"Erro ao testar template {template}.html: {str(e)}")
            all_ok = False
    
    return all_ok

def test_data_endpoints():
    """Testa os endpoints de dados"""
    print_header("TESTE 5: Endpoints de Dados")
    
    endpoints = [
        "/api/data/date-range",
        "/api/test/data-handler"
    ]
    
    all_ok = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print_success(f"Endpoint funcionando: {endpoint}")
                if endpoint == "/api/data/date-range":
                    if data.get("status") == "success":
                        print_info(f"  Data mínima: {data.get('min_date', 'N/A')}")
                        print_info(f"  Data máxima: {data.get('max_date', 'N/A')}")
                    elif data.get("status") == "warning":
                        print_warning(f"  {data.get('message', 'N/A')}")
            else:
                print_error(f"Endpoint retornou erro: {endpoint} (Status: {response.status_code})")
                all_ok = False
        except Exception as e:
            print_error(f"Erro ao testar {endpoint}: {str(e)}")
            all_ok = False
    
    return all_ok

def test_dashboard_endpoints():
    """Testa os endpoints de dashboard"""
    print_header("TESTE 6: Endpoints de Dashboard")
    
    dashboards = [
        "geral",
        "financas",
        "estoque",
        "publico_alvo",
        "fornecedores",
        "recursos_humanos"
    ]
    
    # Obter range de datas primeiro
    try:
        date_response = requests.get(f"{BASE_URL}/api/data/date-range", timeout=TIMEOUT)
        if date_response.status_code == 200:
            date_data = date_response.json()
            start_date = date_data.get("min_date", "2024-01-01")
            end_date = date_data.get("max_date", "2025-12-31")
        else:
            start_date = "2024-01-01"
            end_date = "2025-12-31"
    except:
        start_date = "2024-01-01"
        end_date = "2025-12-31"
    
    all_ok = True
    for dashboard in dashboards:
        try:
            # Alguns dashboards precisam de parâmetros de data
            if dashboard in ["geral", "financas", "estoque", "publico_alvo"]:
                url = f"{BASE_URL}/api/dashboard/{dashboard}?start_date={start_date}&end_date={end_date}"
            else:
                url = f"{BASE_URL}/api/dashboard/{dashboard}"
            
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    print_success(f"Dashboard funcionando: {dashboard}")
                    # Verificar se tem dados
                    if "data" in data or "kpis" in data:
                        print_info(f"  Dashboard retornou dados")
                else:
                    print_warning(f"Dashboard {dashboard} retornou status: {data.get('status', 'N/A')}")
            else:
                print_error(f"Dashboard retornou erro: {dashboard} (Status: {response.status_code})")
                all_ok = False
        except Exception as e:
            print_error(f"Erro ao testar dashboard {dashboard}: {str(e)}")
            all_ok = False
    
    return all_ok

def test_analysis_endpoints():
    """Testa alguns endpoints de análise"""
    print_header("TESTE 7: Endpoints de Análise (Amostra)")
    
    # Testar apenas alguns endpoints principais
    endpoints = [
        "/api/analysis/financial/summary",
        "/api/analysis/inventory/summary",
        "/api/analysis/suppliers/summary"
    ]
    
    all_ok = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            if response.status_code == 200:
                print_success(f"Endpoint de análise funcionando: {endpoint}")
            elif response.status_code == 422:
                print_warning(f"Endpoint {endpoint} precisa de parâmetros (Status 422)")
            else:
                print_error(f"Endpoint retornou erro: {endpoint} (Status: {response.status_code})")
                all_ok = False
        except Exception as e:
            print_error(f"Erro ao testar {endpoint}: {str(e)}")
            all_ok = False
    
    return all_ok

def test_chart_endpoints():
    """Testa alguns endpoints de gráficos"""
    print_header("TESTE 8: Endpoints de Gráficos (Amostra)")
    
    # Obter range de datas primeiro
    try:
        date_response = requests.get(f"{BASE_URL}/api/data/date-range", timeout=TIMEOUT)
        if date_response.status_code == 200:
            date_data = date_response.json()
            start_date = date_data.get("min_date", "2024-01-01")
            end_date = date_data.get("max_date", "2025-12-31")
        else:
            start_date = "2024-01-01"
            end_date = "2025-12-31"
    except:
        start_date = "2024-01-01"
        end_date = "2025-12-31"
    
    # Testar alguns gráficos principais
    charts = [
        f"/api/charts/financial/revenue-trend?start_date={start_date}&end_date={end_date}",
        f"/api/charts/inventory/stock-level?start_date={start_date}&end_date={end_date}",
    ]
    
    all_ok = True
    for chart_url in charts:
        try:
            response = requests.get(f"{BASE_URL}{chart_url}", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                if "data" in data or "figure" in data:
                    print_success(f"Gráfico funcionando: {chart_url.split('?')[0]}")
                else:
                    print_warning(f"Gráfico retornou sem dados: {chart_url.split('?')[0]}")
            else:
                print_error(f"Gráfico retornou erro (Status: {response.status_code})")
                all_ok = False
        except Exception as e:
            print_error(f"Erro ao testar gráfico: {str(e)}")
            all_ok = False
    
    return all_ok

def check_file_structure():
    """Verifica se a estrutura de arquivos está correta"""
    print_header("TESTE 9: Estrutura de Arquivos")
    
    project_root = Path(__file__).parent
    required_paths = [
        "backend/app/main.py",
        "frontend/templates/base.html",
        "frontend/static/css/main.css",
        "frontend/static/js/app.js",
        "frontend/templates/dashboards/geral.html",
        "frontend/templates/dashboards/financas.html",
    ]
    
    all_ok = True
    for path_str in required_paths:
        path = project_root / path_str
        if path.exists():
            print_success(f"Arquivo encontrado: {path_str}")
        else:
            print_error(f"Arquivo não encontrado: {path_str}")
            all_ok = False
    
    return all_ok

def generate_report(results):
    """Gera relatório final dos testes"""
    print_header("RELATÓRIO FINAL")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    failed_tests = total_tests - passed_tests
    
    print(f"\n{Colors.BOLD}Resumo dos Testes:{Colors.RESET}")
    print(f"  Total de testes: {total_tests}")
    print(f"  {Colors.GREEN}[OK] Passou: {passed_tests}{Colors.RESET}")
    print(f"  {Colors.RED}[ERRO] Falhou: {failed_tests}{Colors.RESET}")
    print(f"  Taxa de sucesso: {(passed_tests/total_tests*100):.1f}%")
    
    print(f"\n{Colors.BOLD}Detalhes:{Colors.RESET}")
    for test_name, result in results.items():
        status = f"{Colors.GREEN}[PASSOU]{Colors.RESET}" if result else f"{Colors.RED}[FALHOU]{Colors.RESET}"
        print(f"  {test_name}: {status}")
    
    if failed_tests == 0:
        print(f"\n{Colors.BOLD}{Colors.GREEN}[SUCESSO] Todos os testes passaram!{Colors.RESET}")
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}[AVISO] Alguns testes falharam. Verifique os detalhes acima.{Colors.RESET}")
    
    return failed_tests == 0

def main():
    """Função principal"""
    print_header("TESTE AUTOMATIZADO - AMAZON FRUIT WEB APP")
    print_info(f"URL Base: {BASE_URL}")
    print_info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Executar todos os testes
    results["1. Conexão com Servidor"] = test_server_connection()
    
    if not results["1. Conexão com Servidor"]:
        print_error("\nServidor não está rodando. Execute:")
        print_error("  cd backend")
        print_error("  uvicorn app.main:app --reload --host localhost --port 8000")
        sys.exit(1)
    
    results["2. Estrutura de Arquivos"] = check_file_structure()
    results["3. Endpoint Raiz"] = test_root_endpoint()
    results["4. Arquivos Estáticos"] = test_static_files()
    results["5. Templates HTML"] = test_templates()
    results["6. Endpoints de Dados"] = test_data_endpoints()
    results["7. Endpoints de Dashboard"] = test_dashboard_endpoints()
    results["8. Endpoints de Análise"] = test_analysis_endpoints()
    results["9. Endpoints de Gráficos"] = test_chart_endpoints()
    
    # Gerar relatório
    success = generate_report(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTeste interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nErro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

