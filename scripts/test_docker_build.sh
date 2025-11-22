#!/bin/bash
# Script para testar o build Docker

set -e

echo "🐳 Testando build Docker..."

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker encontrado${NC}"

# Verificar se docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  docker-compose não encontrado, usando 'docker compose'${NC}"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Limpar builds anteriores
echo "🧹 Limpando builds anteriores..."
docker-compose down 2>/dev/null || true
docker rmi amazon-fruit-app 2>/dev/null || true

# Build da imagem
echo "🔨 Construindo imagem Docker..."
if docker build -t amazon-fruit-app .; then
    echo -e "${GREEN}✅ Build da imagem concluído com sucesso${NC}"
else
    echo -e "${RED}❌ Erro no build da imagem${NC}"
    exit 1
fi

# Verificar tamanho da imagem
IMAGE_SIZE=$(docker images amazon-fruit-app --format "{{.Size}}")
echo -e "${GREEN}📦 Tamanho da imagem: $IMAGE_SIZE${NC}"

# Testar execução do container
echo "🚀 Testando execução do container..."
CONTAINER_ID=$(docker run -d -p 8000:8000 --name amazon-fruit-test amazon-fruit-app)

# Aguardar container iniciar
echo "⏳ Aguardando container iniciar..."
sleep 5

# Verificar se container está rodando
if docker ps | grep -q amazon-fruit-test; then
    echo -e "${GREEN}✅ Container está rodando${NC}"
else
    echo -e "${RED}❌ Container não está rodando${NC}"
    docker logs amazon-fruit-test
    docker rm -f amazon-fruit-test
    exit 1
fi

# Testar health check
echo "🏥 Testando health check..."
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check passou${NC}"
else
    echo -e "${RED}❌ Health check falhou${NC}"
    docker logs amazon-fruit-test
    docker rm -f amazon-fruit-test
    exit 1
fi

# Verificar logs
echo "📋 Últimas linhas dos logs:"
docker logs --tail 10 amazon-fruit-test

# Limpar
echo "🧹 Limpando container de teste..."
docker rm -f amazon-fruit-test

echo -e "${GREEN}✅ Todos os testes Docker passaram!${NC}"

