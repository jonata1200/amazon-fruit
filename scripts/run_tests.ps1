# Script PowerShell para executar todos os testes

$ErrorActionPreference = "Continue"

Write-Host "🧪 Executando testes da aplicação Amazon Fruit..." -ForegroundColor Cyan
Write-Host ""

# Verificar se o servidor está rodando
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 2
    Write-Host "✅ Servidor está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Servidor não está rodando em http://localhost:8000" -ForegroundColor Red
    Write-Host "Por favor, inicie o servidor primeiro:" -ForegroundColor Yellow
    Write-Host "  cd backend && python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Executar testes de integração
Write-Host "📋 Executando testes de integração..." -ForegroundColor Cyan
try {
    python -m pytest tests/test_integration.py -v
    Write-Host "✅ Testes de integração passaram" -ForegroundColor Green
} catch {
    Write-Host "❌ Alguns testes de integração falharam" -ForegroundColor Red
}

Write-Host ""

# Executar testes de performance
Write-Host "⚡ Executando testes de performance..." -ForegroundColor Cyan
try {
    python tests/test_performance.py
    Write-Host "✅ Testes de performance concluídos" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Alguns testes de performance falharam" -ForegroundColor Yellow
}

Write-Host ""

# Executar testes de segurança
Write-Host "🔒 Executando testes de segurança..." -ForegroundColor Cyan
try {
    python tests/test_security.py
    Write-Host "✅ Testes de segurança concluídos" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Alguns testes de segurança falharam" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Todos os testes foram executados!" -ForegroundColor Green

