"""
Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json

from autodev_agent.main import app


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_healthz(self, client):
        """Test /healthz endpoint."""
        response = client.get("/healthz")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_readyz(self, client):
        """Test /readyz endpoint."""
        response = client.get("/readyz")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "timestamp" in data
        assert "services" in data
    
    def test_gdpr_delete(self, client):
        """Test GDPR delete endpoint."""
        response = client.delete("/gdpr/delete", json={"user_id": "test-user"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "deleted"
        assert data["user_id"] == "test-user"


class TestAgentEndpoints:
    """Test agent-related endpoints."""
    
    def test_get_agents(self, client, mock_orchestrator):
        """Test GET /api/v1/agents endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.get("/api/v1/agents")
            
            assert response.status_code == 200
            data = response.json()
            assert "agents" in data
            assert len(data["agents"]) == 5
    
    def test_get_agent_status(self, client, mock_orchestrator):
        """Test GET /api/v1/agents/{agent_type} endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.get("/api/v1/agents/planner")
            
            assert response.status_code == 200
            data = response.json()
            assert data["agent_type"] == "planner"
            assert "status" in data
            assert "stats" in data
    
    def test_execute_agent(self, client, mock_orchestrator, test_data):
        """Test POST /api/v1/agents/{agent_type}/execute endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.post(
                "/api/v1/agents/planner/execute",
                json=test_data["agent_request"]
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            assert "execution_time" in data
    
    def test_disable_agent(self, client, mock_orchestrator):
        """Test POST /api/v1/agents/{agent_type}/disable endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.post("/api/v1/agents/planner/disable")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "disabled"
    
    def test_enable_agent(self, client, mock_orchestrator):
        """Test POST /api/v1/agents/{agent_type}/enable endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.post("/api/v1/agents/planner/enable")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "enabled"


class TestWorkflowEndpoints:
    """Test workflow-related endpoints."""
    
    def test_execute_workflow(self, client, mock_orchestrator, test_data):
        """Test POST /api/v1/workflows/execute endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.post(
                "/api/v1/workflows/execute",
                json=test_data["workflow_request"]
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "workflow_id" in data
            assert "status" in data
            assert "steps" in data
    
    def test_get_workflow_status(self, client, mock_orchestrator):
        """Test GET /api/v1/workflows/{workflow_id} endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.get("/api/v1/workflows/test-workflow-id")
            
            assert response.status_code == 200
            data = response.json()
            assert "workflow_id" in data
            assert "status" in data
    
    def test_get_workflow_history(self, client, mock_orchestrator):
        """Test GET /api/v1/workflows endpoint."""
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.get("/api/v1/workflows")
            
            assert response.status_code == 200
            data = response.json()
            assert "workflows" in data
            assert isinstance(data["workflows"], list)


class TestToolEndpoints:
    """Test tool-related endpoints."""
    
    def test_get_tools(self, client):
        """Test GET /api/v1/tools endpoint."""
        response = client.get("/api/v1/tools")
        
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) > 0
    
    def test_execute_tool(self, client, temp_dir):
        """Test POST /api/v1/tools/{tool_name}/execute endpoint."""
        # Test file read tool
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, World!")
        
        response = client.post(
            "/api/v1/tools/read_file/execute",
            json={"path": str(test_file)}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"] == "Hello, World!"
    
    def test_execute_shell_command(self, client):
        """Test shell command execution."""
        response = client.post(
            "/api/v1/tools/execute_shell/execute",
            json={"command": "echo 'test'"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "test" in data["result"]


class TestConversationEndpoints:
    """Test conversation-related endpoints."""
    
    def test_get_conversations(self, client):
        """Test GET /api/v1/conversations endpoint."""
        response = client.get("/api/v1/conversations")
        
        assert response.status_code == 200
        data = response.json()
        assert "conversations" in data
        assert isinstance(data["conversations"], list)
    
    def test_get_conversation(self, client):
        """Test GET /api/v1/conversations/{conversation_id} endpoint."""
        response = client.get("/api/v1/conversations/test-conv-123")
        
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "messages" in data
    
    def test_create_conversation(self, client):
        """Test POST /api/v1/conversations endpoint."""
        response = client.post(
            "/api/v1/conversations",
            json={"title": "Test Conversation"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "conversation_id" in data
        assert data["title"] == "Test Conversation"
    
    def test_add_message(self, client):
        """Test POST /api/v1/conversations/{conversation_id}/messages endpoint."""
        response = client.post(
            "/api/v1/conversations/test-conv-123/messages",
            json={
                "role": "user",
                "content": "Hello, AI!"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "message_id" in data
        assert data["role"] == "user"
        assert data["content"] == "Hello, AI!"


class TestConfigEndpoints:
    """Test configuration endpoints."""
    
    def test_get_config(self, client):
        """Test GET /api/v1/config endpoint."""
        response = client.get("/api/v1/config")
        
        assert response.status_code == 200
        data = response.json()
        assert "app_name" in data
        assert "app_version" in data
        assert "app_env" in data
    
    def test_update_config(self, client):
        """Test PUT /api/v1/config endpoint."""
        config_update = {
            "log_level": "DEBUG",
            "max_tokens": 2048
        }
        
        response = client.put("/api/v1/config", json=config_update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "updated"
    
    def test_get_models(self, client):
        """Test GET /api/v1/config/models endpoint."""
        response = client.get("/api/v1/config/models")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_models" in data
        assert "primary_model" in data
        assert "fallback_model" in data


class TestLogsEndpoints:
    """Test logs endpoints."""
    
    def test_get_logs(self, client):
        """Test GET /api/v1/logs endpoint."""
        response = client.get("/api/v1/logs")
        
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert isinstance(data["logs"], list)
    
    def test_get_logs_with_filters(self, client):
        """Test GET /api/v1/logs with query parameters."""
        response = client.get("/api/v1/logs?level=ERROR&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
    
    def test_clear_logs(self, client):
        """Test DELETE /api/v1/logs endpoint."""
        response = client.delete("/api/v1/logs")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cleared"


class TestErrorHandling:
    """Test API error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "detail" in data
    
    def test_422_validation_error(self, client):
        """Test validation error handling."""
        response = client.post(
            "/api/v1/agents/planner/execute",
            json={"invalid": "data"}
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_500_internal_error(self, client, mock_orchestrator):
        """Test internal server error handling."""
        # Mock orchestrator to raise an exception
        mock_orchestrator.execute_workflow.side_effect = Exception("Test error")
        
        with patch("autodev_agent.main.orchestrator", mock_orchestrator):
            response = client.post(
                "/api/v1/workflows/execute",
                json={"task": "test"}
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "error" in data


class TestRateLimiting:
    """Test rate limiting functionality."""
    
    def test_rate_limiting(self, client):
        """Test that rate limiting is enforced."""
        # Make multiple rapid requests
        responses = []
        for _ in range(105):  # More than the default limit
            response = client.get("/healthz")
            responses.append(response)
        
        # Check that some requests were rate limited
        status_codes = [r.status_code for r in responses]
        assert 429 in status_codes  # Too Many Requests


class TestCORS:
    """Test CORS functionality."""
    
    def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        response = client.options("/healthz")
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers


class TestWebSocket:
    """Test WebSocket functionality."""
    
    def test_websocket_connection(self, client):
        """Test WebSocket connection."""
        with client.websocket_connect("/ws/logs") as websocket:
            # Send a message
            websocket.send_text("subscribe")
            
            # Receive response
            data = websocket.receive_text()
            assert data is not None
    
    def test_websocket_logs_stream(self, client):
        """Test WebSocket logs streaming."""
        with client.websocket_connect("/ws/logs") as websocket:
            # Subscribe to logs
            websocket.send_text(json.dumps({"action": "subscribe", "level": "INFO"}))
            
            # Should receive subscription confirmation
            data = websocket.receive_json()
            assert data["type"] == "subscription"
            assert data["status"] == "subscribed"


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_login(self, client):
        """Test login endpoint."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "test", "password": "test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
    
    def test_register(self, client):
        """Test registration endpoint."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "user_id" in data
        assert data["username"] == "newuser"
    
    def test_protected_endpoint_without_auth(self, client):
        """Test that protected endpoints require authentication."""
        response = client.get("/api/v1/protected")
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_auth(self, client):
        """Test protected endpoint with valid authentication."""
        # First login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "test", "password": "test"}
        )
        token = login_response.json()["access_token"]
        
        # Use token for protected endpoint
        response = client.get(
            "/api/v1/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200