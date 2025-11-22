# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .config import settings
from .api.routes.data import router as data_router
from .api.routes.analysis import router as analysis_router
from .api.routes.dashboard import router as dashboard_router
from .api.routes.charts import router as charts_router
from .api.routes.export import router as export_router
from .api.routes.alerts import router as alerts_router
from .api.routes.search import router as search_router

# Configurar logging
from .utils.logging_config import logger
logger.info(f"Iniciando aplicação em modo {settings.environment}")

app = FastAPI(
    title=settings.api_title,
    description="API para sistema de análise de dados Amazon Fruit",
    version=settings.api_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Pre-aquecer aplicação no startup
@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação"""
    from .utils.warmup import warmup_application
    # Executar warmup em thread separada para não bloquear startup
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, warmup_application)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar compressão GZip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configurar rate limiting (apenas em produção)
if settings.rate_limit_enabled and settings.environment == "production":
    from .middleware.rate_limit import RateLimitMiddleware
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.rate_limit_per_minute
    )
    logger.info(f"Rate limiting habilitado: {settings.rate_limit_per_minute} req/min")

# Caminho para o frontend (relativo ao diretório raiz do projeto)
project_root = Path(__file__).resolve().parents[2]
frontend_path = project_root / "frontend"

# Servir arquivos estáticos
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")
    # Servir templates HTML também
    app.mount("/templates", StaticFiles(directory=str(frontend_path / "templates")), name="templates")

# Registrar rotas da API
app.include_router(data_router)
app.include_router(analysis_router)
app.include_router(dashboard_router)
app.include_router(charts_router)
app.include_router(export_router)
app.include_router(alerts_router)
app.include_router(search_router)

@app.get("/")
async def read_root():
    """Endpoint raiz - retorna a página inicial"""
    base_path = frontend_path / "templates" / "base.html"
    if base_path.exists():
        return FileResponse(str(base_path))
    index_path = frontend_path / "templates" / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Amazon Fruit API", "status": "running", "frontend": "not configured"}

@app.get("/base.html")
async def read_base():
    """Endpoint para servir base.html"""
    base_path = frontend_path / "templates" / "base.html"
    if base_path.exists():
        return FileResponse(str(base_path))
    return {"error": "base.html not found"}

@app.get("/api/health")
async def health_check():
    """
    Endpoint de health check para monitoramento.
    Verifica status da aplicação e conectividade com banco de dados.
    """
    from datetime import datetime
    import sqlite3
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.api_version,
        "environment": settings.environment,
        "checks": {}
    }
    
    # Verificar banco de dados
    try:
        db_path = settings.db_path
        if db_path.exists():
            # Tentar conectar ao banco
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            health_status["checks"]["database"] = {
                "status": "healthy",
                "path": str(db_path),
                "exists": True
            }
        else:
            health_status["checks"]["database"] = {
                "status": "warning",
                "path": str(db_path),
                "exists": False,
                "message": "Banco de dados não encontrado"
            }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Determinar status geral
    if health_status["status"] == "degraded":
        health_status["status"] = "degraded"
    elif any(check.get("status") == "warning" for check in health_status["checks"].values()):
        health_status["status"] = "healthy"
    
    return health_status

@app.get("/api/test/data-handler")
async def test_data_handler():
    """Endpoint de teste para verificar se o DataHandler está funcionando"""
    try:
        from .services.data_handler import DataHandler
        from pathlib import Path
        
        project_root = Path(__file__).resolve().parents[2]
        handler = DataHandler(base_dir=project_root)
        
        # Testa get_date_range
        min_date, max_date = handler.get_date_range()
        
        return {
            "status": "success",
            "message": "DataHandler está funcionando corretamente",
            "db_path": str(handler.db_path),
            "db_exists": handler.db_path.exists(),
            "date_range": {
                "min": str(min_date) if min_date else None,
                "max": str(max_date) if max_date else None
            }
        }
    except FileNotFoundError as e:
        return {
            "status": "warning",
            "message": "DataHandler inicializado, mas banco de dados não encontrado",
            "error": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Erro ao testar DataHandler",
            "error": str(e)
        }

