"""
Logging configuration for the AI Coder Agent.

This module provides centralized logging configuration with support for
both JSON and human-readable log formats.
"""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Dict, Any

from pythonjsonlogger.json import JsonFormatter

from ..config import settings


def setup_logging():
    """Setup logging configuration with JSON and human-readable handlers."""
    
    # Create logs directory if it doesn't exist
    logs_path = Path(settings.LOGS_PATH)
    logs_path.mkdir(parents=True, exist_ok=True)
    
    # Define log formats
    json_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
    human_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter,
                "fmt": json_format,
            },
            "human": {
                "format": human_format,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "human" if settings.DEBUG else "json",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(settings.LOGS_PATH, "app.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "json",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(settings.LOGS_PATH, "error.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "json",
                "level": "ERROR",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file", "error_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
    
    # Apply configuration
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)