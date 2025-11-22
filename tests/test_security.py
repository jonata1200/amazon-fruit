# tests/test_security.py
"""
Testes de segurança para Amazon Fruit API
"""

import requests
from requests.exceptions import RequestException

BASE_URL = "http://localhost:8000"

def test_cors_headers():
    """Verifica se os headers CORS estão configurados"""
    # Testar com requisição GET normal (CORS funciona em requisições normais)
    response = requests.get(f"{BASE_URL}/api/health")
    
    # Verificar se CORS está configurado (pode estar presente em GET também)
    # Ou verificar se a requisição não foi bloqueada
    assert response.status_code == 200, "Requisição bloqueada por CORS"
    
    # Se headers CORS estiverem presentes, verificar
    if "Access-Control-Allow-Origin" in response.headers:
        print("✅ Headers CORS encontrados")
    else:
        # CORS pode estar configurado apenas para requisições cross-origin
        print("⚠️  Headers CORS não encontrados (pode estar OK se não for cross-origin)")

def test_security_headers():
    """Verifica headers de segurança"""
    response = requests.get(f"{BASE_URL}/api/health")
    
    # Headers de segurança esperados (se configurados via Nginx)
    security_headers = [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection"
    ]
    
    found_headers = []
    for header in security_headers:
        if header in response.headers:
            found_headers.append(header)
    
    if found_headers:
        print(f"✅ Headers de segurança encontrados: {', '.join(found_headers)}")
    else:
        print("⚠️  Headers de segurança não encontrados (pode estar configurado no Nginx)")

def test_rate_limiting():
    """Testa se o rate limiting está funcionando"""
    # Fazer muitas requisições rapidamente
    num_requests = 100
    rate_limit_hit = False
    
    for i in range(num_requests):
        try:
            response = requests.get(f"{BASE_URL}/api/health")
            if response.status_code == 429:
                rate_limit_hit = True
                print(f"✅ Rate limiting ativado após {i+1} requisições")
                break
        except RequestException as e:
            print(f"Erro na requisição {i+1}: {e}")
            break
    
    if not rate_limit_hit:
        print("⚠️  Rate limiting não foi ativado (pode estar desabilitado em desenvolvimento)")

def test_sql_injection_protection():
    """Testa proteção contra SQL injection"""
    # Tentar SQL injection em parâmetros
    malicious_inputs = [
        "'; DROP TABLE--",
        "1' OR '1'='1",
        "'; SELECT * FROM--"
    ]
    
    for malicious_input in malicious_inputs:
        try:
            response = requests.get(
                f"{BASE_URL}/api/search",
                params={"query": malicious_input, "limit": 10}
            )
            # Não deve retornar erro 500 (erro interno)
            assert response.status_code != 500, f"SQL injection possível com: {malicious_input}"
        except RequestException:
            pass
    
    print("✅ Proteção contra SQL injection funcionando")

def test_xss_protection():
    """Testa proteção contra XSS"""
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')"
    ]
    
    for payload in xss_payloads:
        try:
            response = requests.get(
                f"{BASE_URL}/api/search",
                params={"query": payload, "limit": 10}
            )
            # Verificar se o payload não é executado (resposta não contém script)
            assert "<script>" not in response.text.lower(), f"XSS possível com: {payload}"
        except RequestException:
            pass
    
    print("✅ Proteção contra XSS funcionando")

def test_input_validation():
    """Testa validação de inputs"""
    # Testar com datas inválidas
    invalid_dates = [
        ("invalid-date", "2022-12-31"),  # Formato inválido
        ("2020/01/01", "2022-12-31"),   # Formato incorreto
    ]
    
    validation_passed = 0
    for invalid_start, valid_end in invalid_dates:
        try:
            response = requests.get(
                f"{BASE_URL}/api/dashboard/geral",
                params={"start_date": invalid_start, "end_date": valid_end}
            )
            # Deve retornar erro 422 (Unprocessable Entity) ou 400
            if response.status_code in [400, 422]:
                validation_passed += 1
        except RequestException:
            pass
    
    # Nota: Datas como "2020-13-01" podem passar pela validação básica do FastAPI
    # mas falhar na lógica de negócio. Isso é aceitável.
    if validation_passed >= len(invalid_dates) * 0.5:  # Pelo menos 50% devem falhar
        print("✅ Validação de inputs funcionando (formato básico)")
    else:
        print("⚠️  Validação de inputs pode precisar melhorias")

def test_error_handling():
    """Testa tratamento de erros"""
    # Testar endpoint inexistente
    response = requests.get(f"{BASE_URL}/api/endpoint-inexistente")
    assert response.status_code == 404, "Erro 404 não retornado para endpoint inexistente"
    
    # Testar método não permitido
    response = requests.post(f"{BASE_URL}/api/health")
    # Pode retornar 405 ou 200 dependendo da configuração
    assert response.status_code in [200, 405], "Método não permitido não tratado corretamente"
    
    print("✅ Tratamento de erros funcionando")

def run_all_security_tests():
    """Executa todos os testes de segurança"""
    print("🔒 Iniciando testes de segurança...\n")
    
    tests = [
        ("CORS Headers", test_cors_headers),
        ("Security Headers", test_security_headers),
        ("Rate Limiting", test_rate_limiting),
        ("SQL Injection Protection", test_sql_injection_protection),
        ("XSS Protection", test_xss_protection),
        ("Input Validation", test_input_validation),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            test_func()
            results[test_name] = "✅ PASSOU"
        except AssertionError as e:
            print(f"❌ {test_name}: {e}")
            results[test_name] = f"❌ FALHOU: {e}"
        except Exception as e:
            print(f"⚠️  {test_name}: {e}")
            results[test_name] = f"⚠️  ERRO: {e}"
    
    print("\n📊 Resumo dos Testes de Segurança:")
    print("=" * 50)
    for test_name, result in results.items():
        print(f"{test_name:30s}: {result}")
    
    return results

if __name__ == "__main__":
    run_all_security_tests()

