#!/bin/bash
# Script Bash para iniciar o servidor Amazon Fruit
# Uso: ./start-server.sh

echo "========================================"
echo "  Amazon Fruit - Iniciando Servidor"
echo "========================================"
echo ""

# Verificar se estamos no diretório correto
if [ ! -d "backend" ]; then
    echo "❌ Erro: Diretório 'backend' não encontrado!"
    echo "   Execute este script a partir da raiz do projeto."
    exit 1
fi

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Erro: Python não encontrado!"
    echo "   Instale Python 3.8+ e tente novamente."
    exit 1
fi

# Usar python3 se disponível, senão python
PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
echo "✅ Python encontrado: $($PYTHON_CMD --version)"

# Verificar se as dependências estão instaladas
echo ""
echo "Verificando dependências..."
if ! $PYTHON_CMD -c "import fastapi" 2>/dev/null; then
    echo "⚠️  FastAPI não encontrado. Instalando dependências..."
    cd backend
    pip install -r requirements.txt
    cd ..
fi

# Verificar se a porta 8000 está em uso
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an 2>/dev/null | grep -q ":8000.*LISTEN"; then
    echo ""
    echo "⚠️  Porta 8000 já está em uso!"
    echo "   Tentando encerrar processo existente..."
    pkill -f "uvicorn app.main:app" 2>/dev/null || true
    sleep 2
    echo "✅ Processo encerrado"
fi

# Iniciar servidor
echo ""
echo "========================================"
echo "  Iniciando servidor FastAPI..."
echo "========================================"
echo ""
echo "🌐 Servidor será iniciado em: http://localhost:8000"
echo "📚 Documentação API: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/api/health"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Mudar para o diretório backend e iniciar
cd backend
$PYTHON_CMD -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

