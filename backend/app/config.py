# backend/app/config.py

import os
from pathlib import Path
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    def __init__(self):
        # Ambiente
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.debug: bool = os.getenv("DEBUG", "True").lower() == "true"
        
        # Caminho do banco de dados (relativo ao diretório raiz)
        db_path_str = os.getenv("DB_PATH", "data/amazon_fruit.db")
        project_root = Path(__file__).resolve().parents[2]
        self.db_path: Path = project_root / db_path_str
        
        # Configurações da API
        self.api_title: str = "Amazon Fruit API"
        self.api_version: str = "1.0.0"
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # CORS
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
        self.cors_origins: List[str] = [origin.strip() for origin in cors_origins_str.split(",")]

# Instância global de configurações
settings = Settings()

