# Script rápido para iniciar o servidor (sem verificações detalhadas)
# Uso: .\start-server-quick.ps1

Write-Host "🚀 Iniciando servidor Amazon Fruit..." -ForegroundColor Green
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

