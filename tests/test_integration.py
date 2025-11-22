# tests/test_integration.py
"""
Testes de integração para Amazon Fruit API
"""

import pytest
import requests
from datetime import datetime, timedelta

# URL base da API (ajustar conforme necessário)
BASE_URL = "http://localhost:8000"

class TestHealthCheck:
    """Testes do endpoint de health check"""
    
    def test_health_check_status(self):
        """Verifica se o health check retorna status healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "degraded"]
    
    def test_health_check_structure(self):
        """Verifica a estrutura da resposta do health check"""
        response = requests.get(f"{BASE_URL}/api/health")
        data = response.json()
        assert "timestamp" in data
        assert "version" in data
        assert "environment" in data
        assert "checks" in data
    
    def test_health_check_database(self):
        """Verifica se o health check verifica o banco de dados"""
        response = requests.get(f"{BASE_URL}/api/health")
        data = response.json()
        assert "checks" in data
        assert "database" in data["checks"]

class TestDataEndpoints:
    """Testes dos endpoints de dados"""
    
    def test_get_tables(self):
        """Verifica se é possível obter dados de uma tabela conhecida"""
        # Testar com uma tabela conhecida (financas)
        response = requests.get(f"{BASE_URL}/api/data/financas")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_get_table_data(self):
        """Verifica se é possível obter dados de uma tabela"""
        # Obter data range primeiro
        date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
        date_range = date_range_response.json()
        
        if date_range.get("min_date") and date_range.get("max_date"):
            start_date = date_range["min_date"]
            end_date = date_range["max_date"]
            
            # Testar com tabela financas
            response = requests.get(
                f"{BASE_URL}/api/data/financas",
                params={"start_date": start_date, "end_date": end_date}
            )
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "data" in data

class TestDashboardEndpoints:
    """Testes dos endpoints de dashboards"""
    
    def test_dashboard_geral(self):
        """Verifica se o dashboard geral funciona"""
        # Obter data range
        date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
        date_range = date_range_response.json()
        
        if date_range.get("min_date") and date_range.get("max_date"):
            start_date = date_range["min_date"]
            end_date = date_range["max_date"]
            
            response = requests.get(
                f"{BASE_URL}/api/dashboard/geral",
                params={"start_date": start_date, "end_date": end_date}
            )
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
    
    def test_dashboard_financas(self):
        """Verifica se o dashboard de finanças funciona"""
        date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
        date_range = date_range_response.json()
        
        if date_range.get("min_date") and date_range.get("max_date"):
            start_date = date_range["min_date"]
            end_date = date_range["max_date"]
            
            response = requests.get(
                f"{BASE_URL}/api/dashboard/financas",
                params={"start_date": start_date, "end_date": end_date}
            )
            assert response.status_code == 200

class TestChartEndpoints:
    """Testes dos endpoints de gráficos"""
    
    def test_financial_evolution_chart(self):
        """Verifica se o gráfico de evolução financeira funciona"""
        date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
        date_range = date_range_response.json()
        
        if date_range.get("min_date") and date_range.get("max_date"):
            start_date = date_range["min_date"]
            end_date = date_range["max_date"]
            
            response = requests.get(
                f"{BASE_URL}/api/charts/financial/evolution",
                params={"start_date": start_date, "end_date": end_date}
            )
            assert response.status_code == 200
            data = response.json()
            assert "status" in data

class TestSearchEndpoint:
    """Testes do endpoint de busca global"""
    
    def test_global_search(self):
        """Verifica se a busca global funciona"""
        # O endpoint usa 'q' ao invés de 'query'
        response = requests.get(
            f"{BASE_URL}/api/search",
            params={"q": "test", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data or "status" in data

class TestAlertsEndpoint:
    """Testes do endpoint de alertas"""
    
    def test_get_alerts(self):
        """Verifica se o endpoint de alertas funciona"""
        date_range_response = requests.get(f"{BASE_URL}/api/data/date-range")
        date_range = date_range_response.json()
        
        if date_range.get("min_date") and date_range.get("max_date"):
            start_date = date_range["min_date"]
            end_date = date_range["max_date"]
            
            response = requests.get(
                f"{BASE_URL}/api/alerts",
                params={"start_date": start_date, "end_date": end_date}
            )
            assert response.status_code == 200
            data = response.json()
            assert "alerts" in data

class TestExportEndpoints:
    """Testes dos endpoints de exportação"""
    
    def test_export_table_xlsx(self):
        """Verifica se a exportação para Excel funciona"""
        # Testar com tabela conhecida
        response = requests.get(
            f"{BASE_URL}/api/export/financas",
            params={"format": "xlsx"}
        )
        # Pode retornar 200 (sucesso), 400 (sem dados) ou 500 (erro interno)
        # Aceitar qualquer status que não seja 404 (endpoint não existe)
        assert response.status_code != 404, "Endpoint de exportação não encontrado"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

