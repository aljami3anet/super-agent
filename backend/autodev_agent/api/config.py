"""
Configuration API endpoints for AI Coder Agent.

This module provides API endpoints for:
- Configuration management
- Settings updates
- Environment information
- Feature flags
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import settings
from ..services.config import ConfigService

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize config service
config_service = ConfigService()


# Request/Response Models
class ConfigUpdateRequest(BaseModel):
    """Request model for configuration updates."""
    key: str = Field(..., description="Configuration key")
    value: Any = Field(..., description="Configuration value")
    description: Optional[str] = Field(default=None, description="Configuration description")


class ConfigResponse(BaseModel):
    """Response model for configuration operations."""
    key: str = Field(..., description="Configuration key")
    value: Any = Field(..., description="Configuration value")
    description: Optional[str] = Field(default=None, description="Configuration description")
    updated_at: datetime = Field(..., description="Last update timestamp")
    source: str = Field(..., description="Configuration source")


class EnvironmentInfo(BaseModel):
    """Environment information model."""
    app_name: str = Field(..., description="Application name")
    app_version: str = Field(..., description="Application version")
    app_env: str = Field(..., description="Application environment")
    debug: bool = Field(..., description="Debug mode")
    log_level: str = Field(..., description="Log level")
    host: str = Field(..., description="Server host")
    port: int = Field(..., description="Server port")
    database_url: str = Field(..., description="Database URL (masked)")
    openrouter_models: List[str] = Field(..., description="Available OpenRouter models")


class FeatureFlag(BaseModel):
    """Feature flag model."""
    name: str = Field(..., description="Feature flag name")
    enabled: bool = Field(..., description="Whether feature is enabled")
    description: str = Field(..., description="Feature description")
    last_updated: datetime = Field(..., description="Last update timestamp")


# Configuration Management Endpoints
@router.get("/all", response_model=Dict[str, Any])
async def get_all_config():
    """Get all configuration settings."""
    try:
        return await config_service.get_all_config()
    except Exception as e:
        logger.error(f"Failed to get all config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{key}", response_model=ConfigResponse)
async def get_config(key: str):
    """Get a specific configuration setting."""
    try:
        config = await config_service.get_config(key)
        
        if not config:
            raise HTTPException(status_code=404, detail=f"Configuration key '{key}' not found")
        
        return ConfigResponse(
            key=config["key"],
            value=config["value"],
            description=config.get("description"),
            updated_at=config["updated_at"],
            source=config["source"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get config for key '{key}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{key}", response_model=ConfigResponse)
async def update_config(key: str, request: ConfigUpdateRequest):
    """Update a configuration setting."""
    try:
        config = await config_service.update_config(
            key=key,
            value=request.value,
            description=request.description
        )
        
        return ConfigResponse(
            key=config["key"],
            value=config["value"],
            description=config.get("description"),
            updated_at=config["updated_at"],
            source=config["source"]
        )
        
    except Exception as e:
        logger.error(f"Failed to update config for key '{key}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{key}")
async def delete_config(key: str):
    """Delete a configuration setting."""
    try:
        success = await config_service.delete_config(key)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Configuration key '{key}' not found")
        
        return {"message": f"Configuration key '{key}' deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete config for key '{key}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reload")
async def reload_config():
    """Reload configuration from sources."""
    try:
        result = await config_service.reload_config()
        return {
            "message": "Configuration reloaded successfully",
            "reloaded_keys": result.get("reloaded_keys", []),
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Failed to reload config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Environment Information Endpoints
@router.get("/environment/info", response_model=EnvironmentInfo)
async def get_environment_info():
    """Get environment information."""
    try:
        # Mask sensitive information
        masked_db_url = settings.DATABASE_URL
        if "@" in masked_db_url:
            # Mask password in database URL
            parts = masked_db_url.split("@")
            if len(parts) == 2:
                user_pass = parts[0].split("://")
                if len(user_pass) == 2:
                    protocol = user_pass[0]
                    user_pass_parts = user_pass[1].split(":")
                    if len(user_pass_parts) >= 2:
                        user = user_pass_parts[0]
                        masked_db_url = f"{protocol}://{user}:***@{parts[1]}"
        
        return EnvironmentInfo(
            app_name=settings.APP_NAME,
            app_version=settings.APP_VERSION,
            app_env=settings.APP_ENV,
            debug=settings.DEBUG,
            log_level=settings.LOG_LEVEL,
            host=settings.HOST,
            port=settings.PORT,
            database_url=masked_db_url,
            openrouter_models=settings.OPENROUTER_MODELS
        )
        
    except Exception as e:
        logger.error(f"Failed to get environment info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/environment/health")
async def get_environment_health():
    """Get environment health status."""
    try:
        health = await config_service.get_environment_health()
        return health
    except Exception as e:
        logger.error(f"Failed to get environment health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Feature Flags Endpoints
@router.get("/features/flags", response_model=List[FeatureFlag])
async def get_feature_flags():
    """Get all feature flags."""
    try:
        flags = await config_service.get_feature_flags()
        return [
            FeatureFlag(
                name=flag["name"],
                enabled=flag["enabled"],
                description=flag["description"],
                last_updated=flag["last_updated"]
            )
            for flag in flags
        ]
    except Exception as e:
        logger.error(f"Failed to get feature flags: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/features/flags/{flag_name}", response_model=FeatureFlag)
async def get_feature_flag(flag_name: str):
    """Get a specific feature flag."""
    try:
        flag = await config_service.get_feature_flag(flag_name)
        
        if not flag:
            raise HTTPException(status_code=404, detail=f"Feature flag '{flag_name}' not found")
        
        return FeatureFlag(
            name=flag["name"],
            enabled=flag["enabled"],
            description=flag["description"],
            last_updated=flag["last_updated"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get feature flag '{flag_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/features/flags/{flag_name}")
async def update_feature_flag(flag_name: str, enabled: bool):
    """Update a feature flag."""
    try:
        success = await config_service.update_feature_flag(flag_name, enabled)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Feature flag '{flag_name}' not found")
        
        return {
            "message": f"Feature flag '{flag_name}' updated successfully",
            "enabled": enabled,
            "timestamp": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update feature flag '{flag_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Agent Configuration Endpoints
@router.get("/agents/settings")
async def get_agent_settings():
    """Get agent-specific settings."""
    try:
        return {
            "agent_timeout": settings.AGENT_TIMEOUT,
            "agent_max_retries": settings.AGENT_MAX_RETRIES,
            "agent_retry_delay": settings.AGENT_RETRY_DELAY,
            "planner_agent_enabled": settings.PLANNER_AGENT_ENABLED,
            "coder_agent_enabled": settings.CODER_AGENT_ENABLED,
            "critic_agent_enabled": settings.CRITIC_AGENT_ENABLED,
            "tester_agent_enabled": settings.TESTER_AGENT_ENABLED,
            "summarizer_agent_enabled": settings.SUMMARIZER_AGENT_ENABLED,
            "max_conversation_length": settings.MAX_CONVERSATION_LENGTH,
            "summary_compression_ratio": settings.SUMMARY_COMPRESSION_RATIO,
            "summary_max_size": settings.SUMMARY_MAX_SIZE
        }
    except Exception as e:
        logger.error(f"Failed to get agent settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai/models")
async def get_ai_models():
    """Get AI model configuration."""
    try:
        return {
            "primary_models": settings.OPENROUTER_MODELS,
            "fallback_models": settings.OPENROUTER_FALLBACK_MODELS,
            "max_tokens": settings.MAX_TOKENS,
            "temperature": settings.TEMPERATURE,
            "top_p": settings.TOP_P,
            "frequency_penalty": settings.FREQUENCY_PENALTY,
            "presence_penalty": settings.PRESENCE_PENALTY,
            "max_cost_per_request": settings.MAX_COST_PER_REQUEST,
            "max_cost_per_day": settings.MAX_COST_PER_DAY,
            "cost_tracking_enabled": settings.COST_TRACKING_ENABLED
        }
    except Exception as e:
        logger.error(f"Failed to get AI models config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Security Configuration Endpoints
@router.get("/security/settings")
async def get_security_settings():
    """Get security-related settings."""
    try:
        return {
            "algorithm": settings.ALGORITHM,
            "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_expire_days": settings.REFRESH_TOKEN_EXPIRE_DAYS,
            "cors_origins": settings.CORS_ORIGINS,
            "cors_allow_credentials": settings.CORS_ALLOW_CREDENTIALS,
            "cors_allow_methods": settings.CORS_ALLOW_METHODS,
            "cors_allow_headers": settings.CORS_ALLOW_HEADERS,
            "rate_limit_requests_per_minute": settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
            "rate_limit_burst_size": settings.RATE_LIMIT_BURST_SIZE
        }
    except Exception as e:
        logger.error(f"Failed to get security settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Observability Configuration Endpoints
@router.get("/observability/settings")
async def get_observability_settings():
    """Get observability-related settings."""
    try:
        return {
            "otel_enabled": settings.OTEL_ENABLED,
            "otel_service_name": settings.OTEL_SERVICE_NAME,
            "otel_service_version": settings.OTEL_SERVICE_VERSION,
            "otel_environment": settings.OTEL_ENVIRONMENT,
            "otel_exporter_otlp_endpoint": settings.OTEL_EXPORTER_OTLP_ENDPOINT,
            "otel_exporter_otlp_protocol": settings.OTEL_EXPORTER_OTLP_PROTOCOL,
            "otel_traces_sampler": settings.OTEL_TRACES_SAMPLER,
            "otel_metrics_exporter": settings.OTEL_METRICS_EXPORTER,
            "otel_logs_exporter": settings.OTEL_LOGS_EXPORTER,
            "log_format": settings.LOG_FORMAT,
            "log_file_path": settings.LOG_FILE_PATH,
            "log_max_size": settings.LOG_MAX_SIZE,
            "log_backup_count": settings.LOG_BACKUP_COUNT
        }
    except Exception as e:
        logger.error(f"Failed to get observability settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))