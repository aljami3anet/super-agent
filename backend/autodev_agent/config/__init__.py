"""
Configuration module for AI Coder Agent.

This module provides configuration management with:
- Environment variable loading
- Configuration validation
- Default values
- Type hints
"""

from .settings import Settings, settings

__all__ = ["Settings", "settings"]