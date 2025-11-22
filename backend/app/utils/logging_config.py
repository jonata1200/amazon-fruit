# backend/app/utils/logging_config.py

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..config import settings

def setup_logging():
    """
    Configura o sistema de logging da aplicação.
    """
    # Criar diretório de logs se não existir
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar formato de log
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    
    # Remover handlers existentes
    root_logger.handlers.clear()
    
    # Handler para console (sempre ativo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Handler para arquivo (com rotação)
    if settings.environment == "production":
        file_handler = RotatingFileHandler(
            str(log_file_path),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(log_format)
        root_logger.addHandler(file_handler)
    
    # Configurar loggers específicos
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    
    return root_logger

# Inicializar logging ao importar o módulo
logger = setup_logging()

