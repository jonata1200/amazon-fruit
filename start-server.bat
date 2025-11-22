@echo off
REM Script Batch para iniciar o servidor Amazon Fruit
REM Uso: start-server.bat

echo ========================================
echo   Amazon Fruit - Iniciando Servidor
echo ========================================
echo.

REM Verificar se estamos no diretório correto
if not exist "backend" (
    echo [ERRO] Diretório 'backend' não encontrado!
    echo        Execute este script a partir da raiz do projeto.
    pause
    exit /b 1
)

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo        Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM Verificar se FastAPI está instalado
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [AVISO] FastAPI não encontrado. Instalando dependências...
    cd backend
    pip install -r requirements.txt
    cd ..
)

echo ========================================
echo   Iniciando servidor FastAPI...
echo ========================================
echo.
echo [INFO] Servidor será iniciado em: http://localhost:8000
echo [INFO] Documentação API: http://localhost:8000/docs
echo [INFO] Health Check: http://localhost:8000/api/health
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Mudar para o diretório backend e iniciar
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

