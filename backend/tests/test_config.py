"""
Tests for configuration management.
"""

import pytest
import os
from unittest.mock import patch
from autodev_agent.config import Settings


class TestSettings:
    """Test the Settings class."""
    
    def test_default_settings(self):
        """Test that default settings are loaded correctly."""
        settings = Settings()
        
        assert settings.APP_NAME == "AI Coder Agent"
        assert settings.APP_VERSION == "0.1.0"
        assert settings.APP_ENV == "development"
        assert settings.LOG_LEVEL == "INFO"
    
    def test_environment_variables(self):
        """Test that environment variables override defaults."""
        with patch.dict(os.environ, {
            "OPENROUTER_API_KEY": "test-key",
            "LOG_LEVEL": "DEBUG",
            "APP_ENV": "production",
        }):
            settings = Settings()
            
            assert settings.OPENROUTER_API_KEY == "test-key"
            assert settings.LOG_LEVEL == "DEBUG"
            assert settings.APP_ENV == "production"
    
    def test_openrouter_models_parsing(self):
        """Test that OPENROUTER_MODELS is parsed correctly."""
        with patch.dict(os.environ, {
            "OPENROUTER_MODELS": "gpt-4,gpt-3.5-turbo,claude-3"
        }):
            settings = Settings()
            
            assert "gpt-4" in settings.OPENROUTER_MODELS
            assert "gpt-3.5-turbo" in settings.OPENROUTER_MODELS
            assert "claude-3" in settings.OPENROUTER_MODELS
            assert len(settings.OPENROUTER_MODELS) == 3
    
    def test_cors_origins_parsing(self):
        """Test that CORS_ORIGINS is parsed correctly."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": "http://localhost:3000,https://example.com"
        }):
            settings = Settings()
            
            assert "http://localhost:3000" in settings.CORS_ORIGINS
            assert "https://example.com" in settings.CORS_ORIGINS
            assert len(settings.CORS_ORIGINS) == 2
    
    def test_database_url_default(self):
        """Test default database URL."""
        settings = Settings()
        assert "sqlite" in settings.DATABASE_URL
    
    def test_database_url_override(self):
        """Test database URL override."""
        with patch.dict(os.environ, {
            "DATABASE_URL": "postgresql://user:pass@localhost/db"
        }):
            settings = Settings()
            assert settings.DATABASE_URL == "postgresql://user:pass@localhost/db"
    
    def test_secret_key_generation(self):
        """Test that secret key is generated if not provided."""
        settings = Settings()
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) >= 32
    
    def test_secret_key_override(self):
        """Test secret key override."""
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-secret-key-123"
        }):
            settings = Settings()
            assert settings.SECRET_KEY == "test-secret-key-123"
    
    def test_file_paths(self):
        """Test that file paths are generated correctly."""
        settings = Settings()
        
        assert settings.LOGS_DIR.endswith("logs")
        assert settings.MEMORY_DIR.endswith("memory")
        assert settings.SUMMARIES_DIR.endswith("summaries")
        assert settings.ARTIFACTS_DIR.endswith("artifacts")
    
    def test_model_configuration(self):
        """Test model configuration."""
        with patch.dict(os.environ, {
            "PRIMARY_MODEL": "gpt-4",
            "FALLBACK_MODEL": "gpt-3.5-turbo",
            "MAX_TOKENS": "4096",
            "TEMPERATURE": "0.7"
        }):
            settings = Settings()
            
            assert settings.PRIMARY_MODEL == "gpt-4"
            assert settings.FALLBACK_MODEL == "gpt-3.5-turbo"
            assert settings.MAX_TOKENS == 4096
            assert settings.TEMPERATURE == 0.7
    
    def test_agent_configuration(self):
        """Test agent configuration."""
        with patch.dict(os.environ, {
            "AGENT_TIMEOUT": "300",
            "AGENT_MAX_RETRIES": "5"
        }):
            settings = Settings()
            
            assert settings.AGENT_TIMEOUT == 300
            assert settings.AGENT_MAX_RETRIES == 5
    
    def test_security_configuration(self):
        """Test security configuration."""
        with patch.dict(os.environ, {
            "RATE_LIMIT_PER_MINUTE": "100",
            "CORS_ORIGINS": "https://trusted-site.com"
        }):
            settings = Settings()
            
            assert settings.RATE_LIMIT_PER_MINUTE == 100
            assert "https://trusted-site.com" in settings.CORS_ORIGINS
    
    def test_observability_configuration(self):
        """Test observability configuration."""
        with patch.dict(os.environ, {
            "OTEL_ENDPOINT": "http://localhost:4317",
            "PROMETHEUS_PORT": "9090"
        }):
            settings = Settings()
            
            assert settings.OTEL_ENDPOINT == "http://localhost:4317"
            assert settings.PROMETHEUS_PORT == 9090
    
    def test_validation_errors(self):
        """Test that validation errors are raised for invalid values."""
        with patch.dict(os.environ, {
            "MAX_TOKENS": "invalid",
            "TEMPERATURE": "2.5",  # Should be <= 2.0
        }):
            with pytest.raises(ValueError):
                Settings()
    
    def test_optional_settings(self):
        """Test that optional settings work correctly."""
        settings = Settings()
        
        # These should have defaults even if not in environment
        assert settings.APP_NAME is not None
        assert settings.APP_VERSION is not None
        assert settings.LOG_LEVEL is not None
        assert settings.APP_ENV is not None


class TestSettingsValidation:
    """Test settings validation."""
    
    def test_valid_log_levels(self):
        """Test that valid log levels are accepted."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in valid_levels:
            with patch.dict(os.environ, {"LOG_LEVEL": level}):
                settings = Settings()
                assert settings.LOG_LEVEL == level
    
    def test_invalid_log_level(self):
        """Test that invalid log levels raise an error."""
        with patch.dict(os.environ, {"LOG_LEVEL": "INVALID"}):
            with pytest.raises(ValueError):
                Settings()
    
    def test_valid_app_env(self):
        """Test that valid app environments are accepted."""
        valid_envs = ["development", "testing", "staging", "production"]
        
        for env in valid_envs:
            with patch.dict(os.environ, {"APP_ENV": env}):
                settings = Settings()
                assert settings.APP_ENV == env
    
    def test_invalid_app_env(self):
        """Test that invalid app environments raise an error."""
        with patch.dict(os.environ, {"APP_ENV": "invalid"}):
            with pytest.raises(ValueError):
                Settings()
    
    def test_temperature_range(self):
        """Test that temperature is within valid range."""
        # Test valid range
        with patch.dict(os.environ, {"TEMPERATURE": "0.5"}):
            settings = Settings()
            assert settings.TEMPERATURE == 0.5
        
        # Test invalid range
        with patch.dict(os.environ, {"TEMPERATURE": "2.5"}):
            with pytest.raises(ValueError):
                Settings()
    
    def test_max_tokens_positive(self):
        """Test that max tokens is positive."""
        with patch.dict(os.environ, {"MAX_TOKENS": "1000"}):
            settings = Settings()
            assert settings.MAX_TOKENS == 1000
        
        with patch.dict(os.environ, {"MAX_TOKENS": "-100"}):
            with pytest.raises(ValueError):
                Settings()
    
    def test_rate_limit_positive(self):
        """Test that rate limit is positive."""
        with patch.dict(os.environ, {"RATE_LIMIT_PER_MINUTE": "100"}):
            settings = Settings()
            assert settings.RATE_LIMIT_PER_MINUTE == 100
        
        with patch.dict(os.environ, {"RATE_LIMIT_PER_MINUTE": "0"}):
            with pytest.raises(ValueError):
                Settings()


class TestSettingsProperties:
    """Test settings properties."""
    
    def test_is_development(self):
        """Test is_development property."""
        with patch.dict(os.environ, {"APP_ENV": "development"}):
            settings = Settings()
            assert settings.is_development is True
        
        with patch.dict(os.environ, {"APP_ENV": "production"}):
            settings = Settings()
            assert settings.is_development is False
    
    def test_is_production(self):
        """Test is_production property."""
        with patch.dict(os.environ, {"APP_ENV": "production"}):
            settings = Settings()
            assert settings.is_production is True
        
        with patch.dict(os.environ, {"APP_ENV": "development"}):
            settings = Settings()
            assert settings.is_production is False
    
    def test_is_testing(self):
        """Test is_testing property."""
        with patch.dict(os.environ, {"APP_ENV": "testing"}):
            settings = Settings()
            assert settings.is_testing is True
        
        with patch.dict(os.environ, {"APP_ENV": "development"}):
            settings = Settings()
            assert settings.is_testing is False