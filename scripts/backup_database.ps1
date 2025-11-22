# Script de backup do banco de dados SQLite (PowerShell)

param(
    [string]$BackupDir = "./backups",
    [string]$DbPath = "./data/amazon_fruit.db",
    [int]$RetentionDays = 30
)

# Criar diretório de backup se não existir
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

# Verificar se o banco de dados existe
if (-not (Test-Path $DbPath)) {
    Write-Host "ERRO: Banco de dados não encontrado em $DbPath" -ForegroundColor Red
    exit 1
}

# Criar nome do arquivo de backup com timestamp
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = Join-Path $BackupDir "amazon_fruit_$Date.db"

# Criar backup
Copy-Item $DbPath $BackupFile

# Comprimir backup (opcional)
if (Get-Command Compress-Archive -ErrorAction SilentlyContinue) {
    $CompressedFile = "$BackupFile.zip"
    Compress-Archive -Path $BackupFile -DestinationPath $CompressedFile -Force
    Remove-Item $BackupFile
    $BackupFile = $CompressedFile
    Write-Host "Backup comprimido: $BackupFile"
} else {
    Write-Host "Backup criado: $BackupFile"
}

# Remover backups antigos
$CutoffDate = (Get-Date).AddDays(-$RetentionDays)
Get-ChildItem -Path $BackupDir -Filter "amazon_fruit_*.db*" | 
    Where-Object { $_.LastWriteTime -lt $CutoffDate } | 
    Remove-Item -Force

Write-Host "Backup concluído com sucesso!" -ForegroundColor Green
Write-Host "Arquivo: $BackupFile"
$FileSize = (Get-Item $BackupFile).Length / 1MB
Write-Host "Tamanho: $([math]::Round($FileSize, 2)) MB"

