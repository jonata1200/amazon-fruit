# Script PowerShell para testar o build Docker

$ErrorActionPreference = "Stop"

Write-Host "🐳 Testando build Docker..." -ForegroundColor Cyan

# Verificar se Docker está instalado
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não está instalado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker encontrado" -ForegroundColor Green

# Verificar se docker-compose está disponível
$dockerCompose = "docker-compose"
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        $dockerCompose = "docker compose"
        Write-Host "⚠️  Usando 'docker compose' (sem hífen)" -ForegroundColor Yellow
    } else {
        Write-Host "❌ docker-compose não encontrado" -ForegroundColor Red
        exit 1
    }
}

# Limpar builds anteriores
Write-Host "🧹 Limpando builds anteriores..." -ForegroundColor Yellow
& docker-compose down 2>$null
docker rmi amazon-fruit-app 2>$null

# Build da imagem
Write-Host "🔨 Construindo imagem Docker..." -ForegroundColor Cyan
try {
    docker build -t amazon-fruit-app .
    Write-Host "✅ Build da imagem concluído com sucesso" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro no build da imagem: $_" -ForegroundColor Red
    exit 1
}

# Verificar tamanho da imagem
$imageSize = docker images amazon-fruit-app --format "{{.Size}}"
Write-Host "📦 Tamanho da imagem: $imageSize" -ForegroundColor Green

# Testar execução do container
Write-Host "🚀 Testando execução do container..." -ForegroundColor Cyan
$containerId = docker run -d -p 8000:8000 --name amazon-fruit-test amazon-fruit-app

# Aguardar container iniciar
Write-Host "⏳ Aguardando container iniciar..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar se container está rodando
$running = docker ps --filter "name=amazon-fruit-test" --format "{{.Names}}"
if ($running -eq "amazon-fruit-test") {
    Write-Host "✅ Container está rodando" -ForegroundColor Green
} else {
    Write-Host "❌ Container não está rodando" -ForegroundColor Red
    docker logs amazon-fruit-test
    docker rm -f amazon-fruit-test
    exit 1
}

# Testar health check
Write-Host "🏥 Testando health check..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Health check passou" -ForegroundColor Green
    } else {
        throw "Status code: $($response.StatusCode)"
    }
} catch {
    Write-Host "❌ Health check falhou: $_" -ForegroundColor Red
    docker logs amazon-fruit-test
    docker rm -f amazon-fruit-test
    exit 1
}

# Verificar logs
Write-Host "📋 Últimas linhas dos logs:" -ForegroundColor Cyan
docker logs --tail 10 amazon-fruit-test

# Limpar
Write-Host "🧹 Limpando container de teste..." -ForegroundColor Yellow
docker rm -f amazon-fruit-test

Write-Host "✅ Todos os testes Docker passaram!" -ForegroundColor Green

