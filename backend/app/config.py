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
        self.api_title: str = os.getenv("API_TITLE", "Amazon Fruit API")
        self.api_version: str = os.getenv("API_VERSION", "1.0.0")
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # CORS
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
        self.cors_origins: List[str] = [origin.strip() for origin in cors_origins_str.split(",")]
        
        # Segurança
        self.secret_key: str = os.getenv("SECRET_KEY", "change-this-in-production")
        allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
        self.allowed_hosts: List[str] = [host.strip() for host in allowed_hosts_str.split(",")]
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        log_file_str = os.getenv("LOG_FILE", "logs/app.log")
        self.log_file: Path = project_root / log_file_str
        
        # Performance
        self.workers: int = int(os.getenv("WORKERS", "4"))
        self.max_requests: int = int(os.getenv("MAX_REQUESTS", "1000"))
        self.max_requests_jitter: int = int(os.getenv("MAX_REQUESTS_JITTER", "50"))
        
        # Rate Limiting
        self.rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
        self.rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# Instância global de configurações
settings = Settings()

