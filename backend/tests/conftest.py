"""
Pytest configuration and fixtures for backend testing.
"""

import asyncio
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import tempfile
import os
from typing import Generator, Dict, Any

from autodev_agent.main import app
from autodev_agent.config import settings
from autodev_agent.agents.orchestrator import AgentOrchestrator


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch("autodev_agent.config.settings") as mock:
        mock.OPENROUTER_API_KEY = "test-api-key"
        mock.OPENROUTER_MODELS = ["gpt-4", "gpt-3.5-turbo"]
        mock.PRIMARY_MODEL = "gpt-4"
        mock.FALLBACK_MODEL = "gpt-3.5-turbo"
        mock.DATABASE_URL = "sqlite:///./test.db"
        mock.LOG_LEVEL = "INFO"
        mock.APP_ENV = "test"
        yield mock


@pytest.fixture
def mock_orchestrator():
    """Mock agent orchestrator for testing."""
    orchestrator = Mock(spec=AgentOrchestrator)
    
    # Mock successful workflow execution
    async def mock_execute_workflow(*args, **kwargs):
        return {
            "workflow_id": "test-workflow-id",
            "status": "completed",
            "steps": [
                {
                    "agent": "planner",
                    "status": "completed",
                    "result": {"success": True, "output": "Test plan"},
                },
                {
                    "agent": "coder",
                    "status": "completed",
                    "result": {"success": True, "output": "Test code"},
                },
            ],
            "summary": "Test workflow completed successfully",
            "duration": 10.5,
        }
    
    orchestrator.execute_workflow = mock_execute_workflow
    orchestrator.get_agent_status.return_value = {
        "planner": {"status": "idle", "enabled": True},
        "coder": {"status": "idle", "enabled": True},
        "critic": {"status": "idle", "enabled": True},
        "tester": {"status": "idle", "enabled": True},
        "summarizer": {"status": "idle", "enabled": True},
    }
    orchestrator.get_statistics.return_value = {
        "total_workflows": 10,
        "successful_workflows": 8,
        "failed_workflows": 2,
        "success_rate": 0.8,
        "active_workflows": 0,
    }
    
    return orchestrator


@pytest.fixture
def test_data() -> Dict[str, Any]:
    """Test data for various tests."""
    return {
        "task": "Create a simple REST API endpoint",
        "context": {
            "language": "python",
            "framework": "fastapi",
            "requirements": ["authentication", "validation"],
        },
        "agent_request": {
            "task": "Generate a user authentication endpoint",
            "context": {"method": "POST", "path": "/auth/login"},
            "conversation_id": "test-conversation-123",
        },
        "workflow_request": {
            "task": "Build a complete user management system",
            "context": {
                "features": ["registration", "login", "profile"],
                "database": "postgresql",
            },
        },
    }


@pytest.fixture
def temp_dir():
    """Create a temporary directory for file operations testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    files = {
        "test.py": "def hello(): return 'Hello, World!'",
        "test.json": '{"name": "test", "value": 42}',
        "test.txt": "This is a test file",
        "requirements.txt": "fastapi==0.104.1\nuvicorn==0.24.0",
    }
    
    for filename, content in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
    
    return temp_dir, files


@pytest.fixture
def mock_ai_response():
    """Mock AI model response for testing."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a mock AI response for testing purposes.",
                    "role": "assistant",
                }
            }
        ],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
        },
    }


@pytest.fixture
def mock_http_response():
    """Mock HTTP response for testing."""
    return {
        "status_code": 200,
        "headers": {"content-type": "application/json"},
        "json": lambda: {"success": True, "data": "test data"},
        "text": '{"success": true, "data": "test data"}',
    }


# Coverage configuration
def pytest_configure(config):
    """Configure pytest for coverage reporting."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Test markers
pytestmark = [
    pytest.mark.unit,
]