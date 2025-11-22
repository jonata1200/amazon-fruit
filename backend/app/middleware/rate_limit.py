# backend/app/middleware/rate_limit.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from datetime import datetime, timedelta
from ..config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware de rate limiting simples baseado em memória.
    Para produção, considere usar Redis ou outro sistema distribuído.
    """
    
    def __init__(self, app, requests_per_minute: int = None):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute or settings.rate_limit_per_minute
        self.requests = defaultdict(list)
        self.cleanup_interval = timedelta(minutes=5)
        self.last_cleanup = datetime.now()
    
    async def dispatch(self, request: Request, call_next):
        # Pular rate limiting para health checks
        if request.url.path == "/api/health":
            return await call_next(request)
        
        if not settings.rate_limit_enabled:
            return await call_next(request)
        
        # Obter IP do cliente
        client_ip = request.client.host if request.client else "unknown"
        
        # Limpar requisições antigas periodicamente
        if datetime.now() - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_requests()
            self.last_cleanup = datetime.now()
        
        # Verificar rate limit
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Filtrar requisições do último minuto
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]
        
        # Verificar se excedeu o limite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute."
            )
        
        # Registrar requisição
        self.requests[client_ip].append(now)
        
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar headers de rate limit
        remaining = self.requests_per_minute - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int((now + timedelta(minutes=1)).timestamp()))
        
        return response
    
    def _cleanup_old_requests(self):
        """Remove requisições antigas da memória"""
        minute_ago = datetime.now() - timedelta(minutes=1)
        for ip in list(self.requests.keys()):
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if req_time > minute_ago
            ]
            if not self.requests[ip]:
                del self.requests[ip]

