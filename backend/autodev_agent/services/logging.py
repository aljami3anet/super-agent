"""
Logging service for AI Coder Agent.

This module provides comprehensive logging configuration with:
- JSON and human-readable formats
- File and console handlers
- Log rotation
- Structured logging
- Performance monitoring
"""

import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..config import settings

# Custom JSON formatter
class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


# Custom human-readable formatter
class HumanFormatter(logging.Formatter):
    """Human-readable formatter for development."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record for human reading."""
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        level = record.levelname.ljust(8)
        logger_name = record.name.ljust(20)
        message = record.getMessage()
        
        formatted = f"{timestamp} | {level} | {logger_name} | {message}"
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """Setup logging configuration."""
    
    # Use settings if not provided
    log_level = log_level or settings.LOG_LEVEL
    log_format = log_format or settings.LOG_FORMAT
    log_file = log_file or settings.LOG_FILE_PATH
    
    # Convert log level string to logging level
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    if log_format.lower() == "json":
        formatter = JSONFormatter()
    else:
        formatter = HumanFormatter()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Parse log size
            max_bytes = _parse_size(settings.LOG_MAX_SIZE)
            
            # Create rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=max_bytes,
                backupCount=settings.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            # Fallback to console only if file logging fails
            logging.warning(f"Failed to setup file logging: {e}")
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    
    # Log startup message
    logging.info(f"Logging configured - Level: {log_level}, Format: {log_format}")


def _parse_size(size_str: str) -> int:
    """Parse size string to bytes."""
    size_str = size_str.upper()
    
    if size_str.endswith('KB'):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith('MB'):
        return int(float(size_str[:-2]) * 1024 * 1024)
    elif size_str.endswith('GB'):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
    else:
        return int(size_str)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)


def log_extra_fields(logger: logging.Logger, **kwargs) -> None:
    """Log with extra fields for structured logging."""
    record = logger.makeRecord(
        logger.name,
        logging.INFO,
        "",
        0,
        "",
        (),
        None
    )
    record.extra_fields = kwargs
    logger.handle(record)


class PerformanceLogger:
    """Performance logging utility."""
    
    def __init__(self, logger: logging.Logger, operation: str):
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        self.logger.info(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.utcnow() - self.start_time).total_seconds()
            status = "completed" if exc_type is None else "failed"
            
            self.logger.info(
                f"{self.operation} {status}",
                extra={
                    "operation": self.operation,
                    "duration_seconds": duration,
                    "status": status
                }
            )
            
            if exc_type is not None:
                self.logger.error(f"{self.operation} failed: {exc_val}")


def log_function_call(func):
    """Decorator to log function calls with performance metrics."""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        with PerformanceLogger(logger, f"function {func.__name__}"):
            return func(*args, **kwargs)
    
    return wrapper


def log_async_function_call(func):
    """Decorator to log async function calls with performance metrics."""
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        with PerformanceLogger(logger, f"async function {func.__name__}"):
            return await func(*args, **kwargs)
    
    return wrapper