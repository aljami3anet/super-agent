from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# Rate Limiter: 100 requests per minute per IP (configurable)
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


def register_rate_limiting(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.middleware("http")
    async def add_rate_limit_headers(request: Request, call_next):
        response = await call_next(request)
        headers = limiter._storage.get_view_rate_limit_headers(request)
        for k, v in headers.items():
            response.headers[k] = v
        return response

# Graceful shutdown event

def register_graceful_shutdown(app: FastAPI):
    @app.on_event("shutdown")
    async def shutdown_event():
        logging.info("Graceful shutdown: closing resources...")
        # Add resource cleanup here (DB, cache, etc.)
        # Example: await db_engine.dispose()
        pass