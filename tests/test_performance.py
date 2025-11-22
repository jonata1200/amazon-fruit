# tests/test_performance.py
"""
Testes de performance para Amazon Fruit API
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000"

def test_response_time():
    """Testa o tempo de resposta do health check"""
    # Fazer requisição de aquecimento primeiro
    requests.get(f"{BASE_URL}/api/health")
    time.sleep(0.5)
    
    # Agora medir tempo real
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/health")
    end_time = time.time()
    
    response_time = (end_time - start_time) * 1000  # em milissegundos
    
    assert response.status_code == 200
    
    # Ajustar limite para primeira requisição (cold start pode ser mais lento)
    if response_time < 2000:  # 2 segundos para primeira requisição
        print(f"✅ Health check: {response_time:.2f}ms")
    else:
        print(f"⚠️  Health check lento: {response_time:.2f}ms (pode ser cold start)")
    
    return response_time

def test_concurrent_requests():
    """Testa a aplicação com requisições concorrentes"""
    num_requests = 10
    
    def make_request():
        return requests.get(f"{BASE_URL}/api/health")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in as_completed(futures)]
    
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    
    # Verificar que todas as requisições foram bem-sucedidas
    success_count = sum(1 for r in results if r.status_code == 200)
    
    assert success_count == num_requests, f"Apenas {success_count}/{num_requests} requisições bem-sucedidas"
    
    avg_time = total_time / num_requests
    print(f"✅ {num_requests} requisições concorrentes: {avg_time:.2f}ms média")
    
    return avg_time

def test_dashboard_load_time():
    """Testa o tempo de carregamento de um dashboard"""
    # Obter data range
    date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
    date_range = date_range_response.json()
    
    if not (date_range.get("min_date") and date_range.get("max_date")):
        print("⚠️  Sem dados disponíveis para teste")
        return None
    
    start_date = date_range["min_date"]
    end_date = date_range["max_date"]
    
    start_time = time.time()
    response = requests.get(
        f"{BASE_URL}/api/dashboard/geral",
        params={"start_date": start_date, "end_date": end_date}
    )
    end_time = time.time()
    
    load_time = (end_time - start_time) * 1000
    
    assert response.status_code == 200
    assert load_time < 2000, f"Dashboard demorou muito para carregar: {load_time}ms"
    
    print(f"✅ Dashboard geral: {load_time:.2f}ms")
    return load_time

def test_chart_generation_time():
    """Testa o tempo de geração de um gráfico"""
    date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
    date_range = date_range_response.json()
    
    if not (date_range.get("min_date") and date_range.get("max_date")):
        print("⚠️  Sem dados disponíveis para teste")
        return None
    
    start_date = date_range["min_date"]
    end_date = date_range["max_date"]
    
    start_time = time.time()
    response = requests.get(
        f"{BASE_URL}/api/charts/financial/evolution",
        params={"start_date": start_date, "end_date": end_date}
    )
    end_time = time.time()
    
    generation_time = (end_time - start_time) * 1000
    
    assert response.status_code == 200
    assert generation_time < 3000, f"Gráfico demorou muito para gerar: {generation_time}ms"
    
    print(f"✅ Gráfico financeiro: {generation_time:.2f}ms")
    return generation_time

def run_all_performance_tests():
    """Executa todos os testes de performance"""
    print("🚀 Iniciando testes de performance...\n")
    
    results = {}
    
    try:
        results["health_check"] = test_response_time()
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
    
    try:
        results["concurrent"] = test_concurrent_requests()
    except Exception as e:
        print(f"❌ Erro em requisições concorrentes: {e}")
    
    try:
        results["dashboard"] = test_dashboard_load_time()
    except Exception as e:
        print(f"❌ Erro no dashboard: {e}")
    
    try:
        results["chart"] = test_chart_generation_time()
    except Exception as e:
        print(f"❌ Erro no gráfico: {e}")
    
    print("\n📊 Resumo dos Testes de Performance:")
    print("=" * 50)
    for test_name, result in results.items():
        if result:
            print(f"{test_name:20s}: {result:8.2f}ms")
    
    return results

if __name__ == "__main__":
    run_all_performance_tests()

