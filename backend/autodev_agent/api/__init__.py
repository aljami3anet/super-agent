"""
API module for the AI Coder Agent.

This module provides the API router and endpoint definitions
for the AI Coder Agent application.
"""

from fastapi import APIRouter

from . import agents, config, conversations, tools

# Create API router
router = APIRouter()

# Include sub-routers
router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(config.router, prefix="/config", tags=["config"])
router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
router.include_router(tools.router, prefix="/tools", tags=["tools"])