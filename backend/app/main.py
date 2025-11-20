# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .config import settings
from .api.routes.data import router as data_router
from .api.routes.analysis import router as analysis_router
from .api.routes.dashboard import router as dashboard_router
from .api.routes.charts import router as charts_router

app = FastAPI(
    title=settings.api_title,
    description="API para sistema de análise de dados Amazon Fruit",
    version=settings.api_version
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "message": "API está funcionando corretamente"
    }

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

