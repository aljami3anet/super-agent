"""
API module for AI Coder Agent.

This module provides the FastAPI router with all API endpoints including:
- Agent endpoints
- Tool endpoints
- Conversation endpoints
- Configuration endpoints
"""

from fastapi import APIRouter

from .agents import router as agents_router
from .tools import router as tools_router
from .conversations import router as conversations_router
from .config import router as config_router

# Create main API router
router = APIRouter()

# Include sub-routers
router.include_router(agents_router, prefix="/agents", tags=["agents"])
router.include_router(tools_router, prefix="/tools", tags=["tools"])
router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
router.include_router(config_router, prefix="/config", tags=["config"])

__all__ = ["router"]