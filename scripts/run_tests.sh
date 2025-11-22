#!/bin/bash
# Script para executar todos os testes

set -e

echo "🧪 Executando testes da aplicação Amazon Fruit..."
echo ""

# Verificar se o servidor está rodando
if ! curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "❌ Servidor não está rodando em http://localhost:8000"
    echo "Por favor, inicie o servidor primeiro:"
    echo "  cd backend && python -m uvicorn app.main:app --reload"
    exit 1
fi

echo "✅ Servidor está rodando"
echo ""

# Executar testes de integração
echo "📋 Executando testes de integração..."
if python -m pytest tests/test_integration.py -v; then
    echo "✅ Testes de integração passaram"
else
    echo "❌ Alguns testes de integração falharam"
fi

echo ""

# Executar testes de performance
echo "⚡ Executando testes de performance..."
if python tests/test_performance.py; then
    echo "✅ Testes de performance concluídos"
else
    echo "⚠️  Alguns testes de performance falharam"
fi

echo ""

# Executar testes de segurança
echo "🔒 Executando testes de segurança..."
if python tests/test_security.py; then
    echo "✅ Testes de segurança concluídos"
else
    echo "⚠️  Alguns testes de segurança falharam"
fi

echo ""
echo "✅ Todos os testes foram executados!"

