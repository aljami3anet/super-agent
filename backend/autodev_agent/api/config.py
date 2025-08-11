"""
Configuration API endpoints.

This module provides API endpoints for managing application
configuration and settings.
"""

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..config import settings
from ..services.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class ConfigResponse(BaseModel):
    """Response model for configuration."""
    config: Dict[str, Any]


class ConfigUpdateRequest(BaseModel):
    """Request model for updating configuration."""
    updates: Dict[str, Any]


@router.get("/", response_model=ConfigResponse)
async def get_config():
    """Get the current application configuration."""
    # Return a subset of configuration settings that are safe to expose
    safe_config = {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "cors_origins": settings.CORS_ORIGINS,
        "otel_enabled": settings.OTEL_ENABLED,
        "otel_service_name": settings.OTEL_SERVICE_NAME,
        "otel_environment": settings.OTEL_ENVIRONMENT,
        "primary_model": settings.PRIMARY_MODEL,
        "fallback_model": settings.FALLBACK_MODEL,
        "max_tokens": settings.MAX_TOKENS,
        "temperature": settings.TEMPERATURE,
        "rate_limit_requests": settings.RATE_LIMIT_REQUESTS,
        "rate_limit_window": settings.RATE_LIMIT_WINDOW,
    }
    
    return {"config": safe_config}


@router.post("/update", response_model=ConfigResponse)
async def update_config(request: ConfigUpdateRequest):
    """Update application configuration."""
    # In a real implementation, this would update the configuration
    # and potentially reload the application or services
    
    # For now, just return the current configuration
    safe_config = {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "cors_origins": settings.CORS_ORIGINS,
        "otel_enabled": settings.OTEL_ENABLED,
        "otel_service_name": settings.OTEL_SERVICE_NAME,
        "otel_environment": settings.OTEL_ENVIRONMENT,
        "primary_model": settings.PRIMARY_MODEL,
        "fallback_model": settings.FALLBACK_MODEL,
        "max_tokens": settings.MAX_TOKENS,
        "temperature": settings.TEMPERATURE,
        "rate_limit_requests": settings.RATE_LIMIT_REQUESTS,
        "rate_limit_window": settings.RATE_LIMIT_WINDOW,
    }
    
    logger.info(f"Configuration update requested: {request.updates}")
    
    return {"config": safe_config}


@router.get("/models")
async def get_available_models():
    """Get available AI models."""
    # In a real implementation, this would fetch available models from OpenRouter
    models = [
        {
            "id": "anthropic/claude-2",
            "name": "Claude 2",
            "provider": "Anthropic",
            "description": "Powerful AI assistant for complex reasoning and creativity",
        },
        {
            "id": "openai/gpt-4",
            "name": "GPT-4",
            "provider": "OpenAI",
            "description": "Advanced language model with broad knowledge and reasoning capabilities",
        },
        {
            "id": "openai/gpt-3.5-turbo",
            "name": "GPT-3.5 Turbo",
            "provider": "OpenAI",
            "description": "Fast and capable language model for most tasks",
        },
    ]
    
    return {"models": models}