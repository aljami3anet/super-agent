"""
Settings configuration for AI Coder Agent.

This module provides comprehensive configuration management with:
- Environment variable loading with precedence (.env > config.yaml > config.json)
- Configuration validation
- Type hints and default values
- OpenRouter model configuration
"""

import os
from pathlib import Path
from typing import List, Optional, Union
from pydantic import BaseSettings, Field, validator
from pydantic.types import SecretStr


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application Settings
    APP_NAME: str = Field(default="AI Coder Agent", env="APP_NAME")
    APP_VERSION: str = Field(default="0.1.0", env="APP_VERSION")
    APP_ENV: str = Field(default="development", env="APP_ENV")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    RELOAD: bool = Field(default=True, env="RELOAD")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://ai_coder_user:ai_coder_password@localhost:5432/ai_coder_db",
        env="DATABASE_URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    DATABASE_POOL_RECYCLE: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    
    # AI Model Configuration
    OPENROUTER_API_KEY: SecretStr = Field(env="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        env="OPENROUTER_BASE_URL"
    )
    OPENROUTER_MODELS: List[str] = Field(
        default=[
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4-turbo",
            "meta-llama/llama-3.1-8b-instruct"
        ],
        env="OPENROUTER_MODELS"
    )
    OPENROUTER_FALLBACK_MODELS: List[str] = Field(
        default=[
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-haiku"
        ],
        env="OPENROUTER_FALLBACK_MODELS"
    )
    
    # Model Parameters
    MAX_TOKENS: int = Field(default=4096, env="MAX_TOKENS")
    TEMPERATURE: float = Field(default=0.7, env="TEMPERATURE")
    TOP_P: float = Field(default=0.9, env="TOP_P")
    FREQUENCY_PENALTY: float = Field(default=0.0, env="FREQUENCY_PENALTY")
    PRESENCE_PENALTY: float = Field(default=0.0, env="PRESENCE_PENALTY")
    
    # Cost Management
    MAX_COST_PER_REQUEST: float = Field(default=0.10, env="MAX_COST_PER_REQUEST")
    MAX_COST_PER_DAY: float = Field(default=10.00, env="MAX_COST_PER_DAY")
    COST_TRACKING_ENABLED: bool = Field(default=True, env="COST_TRACKING_ENABLED")
    
    # Agent Configuration
    AGENT_TIMEOUT: int = Field(default=300, env="AGENT_TIMEOUT")
    AGENT_MAX_RETRIES: int = Field(default=3, env="AGENT_MAX_RETRIES")
    AGENT_RETRY_DELAY: int = Field(default=5, env="AGENT_RETRY_DELAY")
    
    # Agent Orchestration
    PLANNER_AGENT_ENABLED: bool = Field(default=True, env="PLANNER_AGENT_ENABLED")
    CODER_AGENT_ENABLED: bool = Field(default=True, env="CODER_AGENT_ENABLED")
    CRITIC_AGENT_ENABLED: bool = Field(default=True, env="CRITIC_AGENT_ENABLED")
    TESTER_AGENT_ENABLED: bool = Field(default=True, env="TESTER_AGENT_ENABLED")
    SUMMARIZER_AGENT_ENABLED: bool = Field(default=True, env="SUMMARIZER_AGENT_ENABLED")
    
    # Conversation Management
    MAX_CONVERSATION_LENGTH: int = Field(default=50, env="MAX_CONVERSATION_LENGTH")
    SUMMARY_COMPRESSION_RATIO: float = Field(default=0.8, env="SUMMARY_COMPRESSION_RATIO")
    SUMMARY_MAX_SIZE: int = Field(default=8192, env="SUMMARY_MAX_SIZE")
    
    # Security Configuration
    SECRET_KEY: SecretStr = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="CORS_ALLOW_METHODS"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"],
        env="CORS_ALLOW_HEADERS"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_REQUESTS_PER_MINUTE")
    RATE_LIMIT_BURST_SIZE: int = Field(default=10, env="RATE_LIMIT_BURST_SIZE")
    
    # OpenTelemetry Configuration
    OTEL_ENABLED: bool = Field(default=True, env="OTEL_ENABLED")
    OTEL_SERVICE_NAME: str = Field(default="ai-coder-agent", env="OTEL_SERVICE_NAME")
    OTEL_SERVICE_VERSION: str = Field(default="0.1.0", env="OTEL_SERVICE_VERSION")
    OTEL_ENVIRONMENT: str = Field(default="development", env="OTEL_ENVIRONMENT")
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(
        default="http://localhost:4317",
        env="OTEL_EXPORTER_OTLP_ENDPOINT"
    )
    OTEL_EXPORTER_OTLP_PROTOCOL: str = Field(
        default="http/protobuf",
        env="OTEL_EXPORTER_OTLP_PROTOCOL"
    )
    OTEL_TRACES_SAMPLER: str = Field(default="always_on", env="OTEL_TRACES_SAMPLER")
    OTEL_METRICS_EXPORTER: str = Field(default="otlp", env="OTEL_METRICS_EXPORTER")
    OTEL_LOGS_EXPORTER: str = Field(default="otlp", env="OTEL_LOGS_EXPORTER")
    
    # Logging Configuration
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE_PATH: str = Field(default="logs/ai_coder_agent.log", env="LOG_FILE_PATH")
    LOG_MAX_SIZE: str = Field(default="100MB", env="LOG_MAX_SIZE")
    LOG_BACKUP_COUNT: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    # File System Configuration
    WORKSPACE_ROOT: str = Field(default="/workspace", env="WORKSPACE_ROOT")
    LOGS_DIR: str = Field(default="logs", env="LOGS_DIR")
    MEMORY_DIR: str = Field(default="memory", env="MEMORY_DIR")
    SUMMARIES_DIR: str = Field(default="summaries", env="SUMMARIES_DIR")
    ARTIFACTS_DIR: str = Field(default="artifacts", env="ARTIFACTS_DIR")
    TEMP_DIR: str = Field(default="temp", env="TEMP_DIR")
    
    # File Size Limits
    MAX_FILE_SIZE: str = Field(default="10MB", env="MAX_FILE_SIZE")
    MAX_PROJECT_SIZE: str = Field(default="100MB", env="MAX_PROJECT_SIZE")
    MAX_LOG_SIZE: str = Field(default="50MB", env="MAX_LOG_SIZE")
    
    # Git Configuration
    GIT_AUTHOR_NAME: str = Field(default="AI Coder Agent", env="GIT_AUTHOR_NAME")
    GIT_AUTHOR_EMAIL: str = Field(default="ai-coder-agent@example.com", env="GIT_AUTHOR_EMAIL")
    GIT_COMMIT_MESSAGE_PREFIX: str = Field(default="[AI] ", env="GIT_COMMIT_MESSAGE_PREFIX")
    GIT_AUTO_COMMIT: bool = Field(default=True, env="GIT_AUTO_COMMIT")
    GIT_AUTO_PUSH: bool = Field(default=False, env="GIT_AUTO_PUSH")
    
    # Testing Configuration
    TEST_COVERAGE_THRESHOLD: int = Field(default=95, env="TEST_COVERAGE_THRESHOLD")
    TEST_TIMEOUT: int = Field(default=300, env="TEST_TIMEOUT")
    TEST_PARALLEL: bool = Field(default=True, env="TEST_PARALLEL")
    TEST_VERBOSE: bool = Field(default=True, env="TEST_VERBOSE")
    
    # Development Configuration
    AUTO_RELOAD: bool = Field(default=True, env="AUTO_RELOAD")
    HOT_RELOAD: bool = Field(default=True, env="HOT_RELOAD")
    DEBUG_TOOLBAR_ENABLED: bool = Field(default=True, env="DEBUG_TOOLBAR_ENABLED")
    PROFILING_ENABLED: bool = Field(default=False, env="PROFILING_ENABLED")
    
    # Code Quality Tools
    RUFF_ENABLED: bool = Field(default=True, env="RUFF_ENABLED")
    MYPY_ENABLED: bool = Field(default=True, env="MYPY_ENABLED")
    BLACK_ENABLED: bool = Field(default=True, env="BLACK_ENABLED")
    ISORT_ENABLED: bool = Field(default=True, env="ISORT_ENABLED")
    
    # Frontend Configuration
    ESLINT_ENABLED: bool = Field(default=True, env="ESLINT_ENABLED")
    PRETTIER_ENABLED: bool = Field(default=True, env="PRETTIER_ENABLED")
    TYPESCRIPT_STRICT: bool = Field(default=True, env="TYPESCRIPT_STRICT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("OPENROUTER_MODELS", "OPENROUTER_FALLBACK_MODELS", pre=True)
    def parse_model_lists(cls, v):
        """Parse comma-separated model lists."""
        if isinstance(v, str):
            return [model.strip() for model in v.split(",")]
        return v
    
    @validator("CORS_ORIGINS", "CORS_ALLOW_METHODS", "CORS_ALLOW_HEADERS", pre=True)
    def parse_cors_lists(cls, v):
        """Parse comma-separated CORS lists."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator("APP_ENV")
    def validate_app_env(cls, v):
        """Validate application environment."""
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"App environment must be one of: {valid_envs}")
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.APP_ENV == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.APP_ENV == "production"
    
    @property
    def is_staging(self) -> bool:
        """Check if running in staging mode."""
        return self.APP_ENV == "staging"
    
    @property
    def workspace_path(self) -> Path:
        """Get workspace path."""
        return Path(self.WORKSPACE_ROOT)
    
    @property
    def logs_path(self) -> Path:
        """Get logs directory path."""
        return self.workspace_path / self.LOGS_DIR
    
    @property
    def memory_path(self) -> Path:
        """Get memory directory path."""
        return self.workspace_path / self.MEMORY_DIR
    
    @property
    def summaries_path(self) -> Path:
        """Get summaries directory path."""
        return self.workspace_path / self.SUMMARIES_DIR
    
    @property
    def artifacts_path(self) -> Path:
        """Get artifacts directory path."""
        return self.workspace_path / self.ARTIFACTS_DIR
    
    @property
    def temp_path(self) -> Path:
        """Get temp directory path."""
        return self.workspace_path / self.TEMP_DIR


# Create settings instance
settings = Settings()

# Ensure required directories exist
def ensure_directories():
    """Ensure required directories exist."""
    directories = [
        settings.logs_path,
        settings.memory_path,
        settings.summaries_path,
        settings.artifacts_path,
        settings.temp_path,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories
ensure_directories()