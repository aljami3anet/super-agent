"""
Configuration settings for the AI Coder Agent.

This module provides configuration management with environment variable support,
validation, and sensible defaults.
"""

import os
from typing import List, Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    APP_NAME: str = Field(default="AI Coder Agent", env="APP_NAME")
    APP_VERSION: str = Field(default="0.1.0", env="APP_VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    RELOAD: bool = Field(default=False, env="RELOAD")
    WORKERS: int = Field(default=1, env="WORKERS")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database settings
    DATABASE_URL: str = Field(env="DATABASE_URL")
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:5173"], env="CORS_ORIGINS")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"], env="CORS_ALLOW_METHODS")
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")
    
    # OpenTelemetry settings
    OTEL_ENABLED: bool = Field(default=True, env="OTEL_ENABLED")
    OTEL_SERVICE_NAME: str = Field(default="ai-coder-agent", env="OTEL_SERVICE_NAME")
    OTEL_SERVICE_VERSION: str = Field(default="0.1.0", env="OTEL_SERVICE_VERSION")
    OTEL_ENVIRONMENT: str = Field(default="development", env="OTEL_ENVIRONMENT")
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(default="http://localhost:4317", env="OTEL_EXPORTER_OTLP_ENDPOINT")
    
    # AI model settings
    OPENROUTER_API_KEY: str = Field(env="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", env="OPENROUTER_BASE_URL")
    PRIMARY_MODEL: str = Field(default="anthropic/claude-2", env="PRIMARY_MODEL")
    FALLBACK_MODEL: str = Field(default="openai/gpt-4", env="FALLBACK_MODEL")
    MAX_TOKENS: int = Field(default=4000, env="MAX_TOKENS")
    TEMPERATURE: float = Field(default=0.7, env="TEMPERATURE")
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Security
    SECRET_KEY: str = Field(env="SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION: int = Field(default=3600, env="JWT_EXPIRATION")  # seconds
    
    # Storage paths
    LOGS_PATH: str = Field(default="./logs", env="LOGS_PATH")
    MEMORY_PATH: str = Field(default="./memory", env="MEMORY_PATH")
    SUMMARIES_PATH: str = Field(default="./summaries", env="SUMMARIES_PATH")
    ARTIFACTS_PATH: str = Field(default="./artifacts", env="ARTIFACTS_PATH")
    
    # Redis settings
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()
