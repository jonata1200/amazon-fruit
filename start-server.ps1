# Script PowerShell para iniciar o servidor Amazon Fruit
# Uso: .\start-server.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Amazon Fruit - Iniciando Servidor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend")) {
    Write-Host "❌ Erro: Diretório 'backend' não encontrado!" -ForegroundColor Red
    Write-Host "   Execute este script a partir da raiz do projeto." -ForegroundColor Yellow
    exit 1
}

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro: Python não encontrado!" -ForegroundColor Red
    Write-Host "   Instale Python 3.8+ e tente novamente." -ForegroundColor Yellow
    exit 1
}

# Verificar se as dependências estão instaladas
Write-Host ""
Write-Host "Verificando dependências..." -ForegroundColor Yellow
try {
    python -c "import fastapi" 2>&1 | Out-Null
    Write-Host "✅ FastAPI instalado" -ForegroundColor Green
} catch {
    Write-Host "⚠️  FastAPI não encontrado. Instalando dependências..." -ForegroundColor Yellow
    Set-Location backend
    pip install -r requirements.txt
    Set-Location ..
}

# Verificar se o servidor já está rodando
$portCheck = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($portCheck) {
    Write-Host ""
    Write-Host "⚠️  Porta 8000 já está em uso!" -ForegroundColor Yellow
    Write-Host "   Tentando encerrar processo existente..." -ForegroundColor Yellow
    $process = Get-Process -Id ($portCheck | Select-Object -First 1).OwningProcess -ErrorAction SilentlyContinue
    if ($process) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Write-Host "✅ Processo encerrado" -ForegroundColor Green
    }
}

# Iniciar servidor
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando servidor FastAPI..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Servidor será iniciado em: http://localhost:8000" -ForegroundColor Green
Write-Host "📚 Documentação API: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "🔍 Health Check: http://localhost:8000/api/health" -ForegroundColor Green
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Mudar para o diretório backend e iniciar
Set-Location backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

