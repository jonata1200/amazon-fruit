#!/bin/bash
# Script de backup do banco de dados SQLite

set -e

# Configurações
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DB_PATH="${DB_PATH:-./data/amazon_fruit.db}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Verificar se o banco de dados existe
if [ ! -f "$DB_PATH" ]; then
    echo "ERRO: Banco de dados não encontrado em $DB_PATH"
    exit 1
fi

# Criar backup
BACKUP_FILE="$BACKUP_DIR/amazon_fruit_$DATE.db"
cp "$DB_PATH" "$BACKUP_FILE"

# Comprimir backup (opcional)
if command -v gzip &> /dev/null; then
    gzip "$BACKUP_FILE"
    BACKUP_FILE="${BACKUP_FILE}.gz"
    echo "Backup comprimido: $BACKUP_FILE"
else
    echo "Backup criado: $BACKUP_FILE"
fi

# Remover backups antigos
find "$BACKUP_DIR" -name "amazon_fruit_*.db*" -type f -mtime +$RETENTION_DAYS -delete

echo "Backup concluído com sucesso!"
echo "Arquivo: $BACKUP_FILE"
echo "Tamanho: $(du -h "$BACKUP_FILE" | cut -f1)"

