# backend/app/utils/warmup.py

"""
Módulo para pre-aquecer a aplicação no startup
"""

import logging
from pathlib import Path
from ..services.data_handler import DataHandler

logger = logging.getLogger(__name__)

def warmup_application():
    """
    Pre-aquece a aplicação inicializando componentes críticos.
    Isso reduz o tempo de resposta da primeira requisição (cold start).
    """
    try:
        logger.info("Iniciando warmup da aplicação...")
        
        # Inicializar DataHandler
        project_root = Path(__file__).resolve().parents[3]
        handler = DataHandler(base_dir=project_root)
        
        # Verificar conectividade com banco de dados
        if handler.db_path.exists():
            # Fazer uma query simples para aquecer a conexão
            try:
                min_date, max_date = handler.get_date_range()
                logger.info(f"Warmup: Banco de dados conectado. Range: {min_date} - {max_date}")
            except Exception as e:
                logger.warning(f"Warmup: Erro ao obter date range: {e}")
        else:
            logger.warning("Warmup: Banco de dados não encontrado")
        
        # Importar módulos críticos para pré-carregar
        try:
            from ..services.analysis import financial_analysis
            logger.info("Warmup: Módulos de análise carregados")
        except Exception as e:
            logger.warning(f"Warmup: Erro ao carregar módulos: {e}")
        
        logger.info("Warmup da aplicação concluído")
        
    except Exception as e:
        logger.error(f"Erro durante warmup: {e}")

