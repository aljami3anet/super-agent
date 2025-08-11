"""
AI Coder Agent - Autonomous AI coding system with multi-agent orchestration.

This package provides a comprehensive AI coding agent system with:
- Multi-agent architecture (Planner, Coder, Critic, Tester, Summarizer)
- Real-time collaboration via WebSocket
- Intelligent code generation with fallback models
- Comprehensive tooling for file operations, Git, testing
- OpenTelemetry integration for observability
- Modern FastAPI backend with PostgreSQL persistence
"""

__version__ = "0.1.0"
__author__ = "AI Coder Agent Team"
__email__ = "ai-coder-agent@example.com"

# Package metadata
__all__ = [
    "main",
    "config",
    "api",
    "agents",
    "tools",
    "services",
    "models",
    "db",
]

# Version info
VERSION_INFO = {
    "version": __version__,
    "author": __author__,
    "email": __email__,
    "description": "AI Coder Agent - Autonomous AI coding system",
    "url": "https://github.com/ai-coder-agent/ai-coder-agent",
}