"""
AI Coder Agent - Main FastAPI Application

This module provides the main FastAPI application with:
- Health check endpoints
- OpenTelemetry integration
- Rate limiting middleware
- Graceful shutdown
- CORS configuration
- API routing
"""

import asyncio
import logging
import os
import signal
import sys
from contextlib import asynccontextmanager
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from .config import settings
from .api import router as api_router
from .services.health import HealthService
from .services.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting AI Coder Agent application...")
    
    # Initialize OpenTelemetry
    if settings.OTEL_ENABLED:
        setup_opentelemetry()
    
    # Initialize health service
    health_service = HealthService()
    app.state.health_service = health_service
    
    logger.info("AI Coder Agent application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Coder Agent application...")
    
    # Cleanup
    if hasattr(app.state, 'health_service'):
        await app.state.health_service.cleanup()
    
    logger.info("AI Coder Agent application shutdown complete")


def setup_opentelemetry():
    """Setup OpenTelemetry tracing."""
    try:
        # Create tracer provider
        resource = Resource.create({
            "service.name": settings.OTEL_SERVICE_NAME,
            "service.version": settings.OTEL_SERVICE_VERSION,
            "service.environment": settings.OTEL_ENVIRONMENT,
        })
        
        tracer_provider = TracerProvider(resource=resource)
        
        # Create OTLP exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
        )
        
        # Add span processor
        tracer_provider.add_span_processor(
            BatchSpanProcessor(otlp_exporter)
        )
        
        # Set global tracer provider
        trace.set_tracer_provider(tracer_provider)
        
        logger.info("OpenTelemetry tracing initialized successfully")
        
    except Exception as e:
        logger.warning(f"Failed to initialize OpenTelemetry: {e}")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI Coder Agent - Autonomous AI coding system with multi-agent orchestration",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Add GZip middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = asyncio.get_event_loop().time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = asyncio.get_event_loop().time() - start_time
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s"
        )
        
        return response
    
    # Add error handling middleware
    @app.middleware("http")
    async def error_handling(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "detail": str(e)}
            )
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
    
    # Health check endpoints
    @app.get("/healthz")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}
    
    @app.get("/readyz")
    async def readiness_check():
        """Readiness check endpoint."""
        if hasattr(app.state, 'health_service'):
            is_ready = await app.state.health_service.is_ready()
            return {"status": "ready" if is_ready else "not ready"}
        return {"status": "ready"}
    
    # GDPR delete endpoint
    @app.delete("/gdpr/delete")
    @limiter.limit("10/minute")
    async def gdpr_delete(request: Request, user_id: str):
        """GDPR data deletion endpoint."""
        # TODO: Implement GDPR deletion logic
        logger.info(f"GDPR deletion request for user: {user_id}")
        return {"status": "deletion_requested", "user_id": user_id}
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "AI Coder Agent - Autonomous AI coding system",
            "docs": "/docs" if settings.DEBUG else None,
            "health": "/healthz",
            "ready": "/readyz",
        }
    
    return app


# Create app instance
app = create_app()

# Instrument FastAPI with OpenTelemetry
if settings.OTEL_ENABLED:
    FastAPIInstrumentor.instrument_app(app)


def main():
    """Main entry point for the application."""
    try:
        # Configure uvicorn
        uvicorn_config = {
            "app": "autodev_agent.main:app",
            "host": settings.HOST,
            "port": settings.PORT,
            "reload": settings.RELOAD,
            "workers": settings.WORKERS,
            "log_level": settings.LOG_LEVEL.lower(),
            "access_log": True,
        }
        
        # Start server
        uvicorn.run(**uvicorn_config)
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)



if __name__ == "__main__":
    main()
