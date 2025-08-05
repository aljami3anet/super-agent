"""
Tester Agent

Responsible for automated testing and validation of code and functionality.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class TesterAgent(BaseAgent):
    """Tester agent for automated testing and validation."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.TESTER,
            name="Tester",
            description="Performs automated testing and validation of code and functionality",
            enabled=True,
            max_retries=3,
            timeout=240,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a QA engineer and testing specialist. Your role is to:

1. Create comprehensive test suites for code and functionality
2. Design test cases that cover edge cases and error conditions
3. Implement automated tests using appropriate testing frameworks
4. Validate code functionality and performance
5. Identify potential bugs and issues through testing
6. Ensure code meets quality and reliability standards

When testing, always:
- Create tests for both happy path and edge cases
- Include unit tests, integration tests, and end-to-end tests
- Test error conditions and exception handling
- Validate input/output behavior
- Consider performance and load testing
- Ensure good test coverage

Generate comprehensive test suites that validate code quality and functionality."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the testing logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            code = context.get("code", "")
            
            # Build the prompt
            prompt = self._build_testing_prompt(task, code, context)
            
            # Generate the tests
            tests = await self._generate_tests(prompt)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=tests,
                metadata={
                    "test_count": self._count_tests(tests),
                    "test_types": self._analyze_test_types(tests),
                    "coverage_estimate": self._estimate_coverage(tests),
                },
                execution_time=execution_time,
                tokens_used=len(prompt.split()),  # Approximate
                cost=0.0,  # Would be calculated based on actual API usage
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResult(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time
            )
    
    def _build_testing_prompt(self, task: str, code: str, context: Dict[str, Any]) -> str:
        """Build the testing prompt."""
        prompt = f"{self.get_system_prompt()}\n\n"
        prompt += f"TASK: {task}\n\n"
        
        if context:
            prompt += "CONTEXT:\n"
            for key, value in context.items():
                if key != "code":
                    prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += f"CODE TO TEST:\n```\n{code}\n```\n\n"
        prompt += """Please create comprehensive tests for this code. Include:

1. Unit tests for individual functions and methods
2. Integration tests for component interactions
3. Edge case and error condition tests
4. Performance tests if applicable
5. Test data and fixtures
6. Test configuration and setup

Generate tests that provide good coverage and validate all functionality."""

        return prompt
    
    async def _generate_tests(self, prompt: str) -> str:
        """Generate the tests using the AI model."""
        # This would integrate with your model router
        # For now, return sample tests
        return '''"""
Comprehensive test suite for the API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json

# Import the app and models
from main import app, Item, ItemResponse

client = TestClient(app)

# Test data fixtures
@pytest.fixture
def sample_item():
    return {
        "name": "Test Item",
        "description": "A test item for testing",
        "price": 10.99,
        "category": "test"
    }

@pytest.fixture
def sample_items():
    return [
        {
            "name": "Item 1",
            "description": "First test item",
            "price": 15.50,
            "category": "electronics"
        },
        {
            "name": "Item 2", 
            "description": "Second test item",
            "price": 25.00,
            "category": "books"
        }
    ]

class TestRootEndpoint:
    """Test the root health check endpoint."""
    
    def test_root_endpoint(self):
        """Test that the root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "API is running"
        assert data["version"] == "1.0.0"

class TestCreateItem:
    """Test item creation functionality."""
    
    def test_create_item_success(self, sample_item):
        """Test successful item creation."""
        response = client.post("/items", json=sample_item)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == sample_item["name"]
        assert data["data"]["price"] == sample_item["price"]
        assert data["data"]["id"] is not None
    
    def test_create_item_missing_required_fields(self):
        """Test item creation with missing required fields."""
        incomplete_item = {"name": "Test"}
        response = client.post("/items", json=incomplete_item)
        assert response.status_code == 422  # Validation error
    
    def test_create_item_negative_price(self):
        """Test item creation with negative price."""
        invalid_item = {
            "name": "Test Item",
            "price": -10.99,
            "category": "test"
        }
        response = client.post("/items", json=invalid_item)
        assert response.status_code == 400
        assert "negative" in response.json()["detail"].lower()
    
    def test_create_item_empty_name(self):
        """Test item creation with empty name."""
        invalid_item = {
            "name": "",
            "price": 10.99,
            "category": "test"
        }
        response = client.post("/items", json=invalid_item)
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

class TestGetItems:
    """Test item retrieval functionality."""
    
    def test_get_items_empty(self):
        """Test getting items when none exist."""
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_items_with_data(self, sample_items):
        """Test getting items when data exists."""
        # Create items first
        for item in sample_items:
            client.post("/items", json=item)
        
        response = client.get("/items")
        assert response.status_code == 200
        items = response.json()
        assert len(items) >= len(sample_items)
    
    def test_get_items_by_category(self, sample_items):
        """Test filtering items by category."""
        # Create items first
        for item in sample_items:
            client.post("/items", json=item)
        
        response = client.get("/items?category=electronics")
        assert response.status_code == 200
        items = response.json()
        assert all(item["category"] == "electronics" for item in items)

class TestGetItem:
    """Test individual item retrieval."""
    
    def test_get_item_success(self, sample_item):
        """Test successful item retrieval."""
        # Create item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == item_id
    
    def test_get_item_not_found(self):
        """Test retrieving non-existent item."""
        response = client.get("/items/999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()

class TestUpdateItem:
    """Test item update functionality."""
    
    def test_update_item_success(self, sample_item):
        """Test successful item update."""
        # Create item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        # Update item
        update_data = {
            "name": "Updated Item",
            "price": 20.99,
            "category": "updated"
        }
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Updated Item"
        assert data["data"]["price"] == 20.99
    
    def test_update_item_not_found(self):
        """Test updating non-existent item."""
        update_data = {
            "name": "Updated Item",
            "price": 20.99,
            "category": "updated"
        }
        response = client.put("/items/999", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()
    
    def test_update_item_invalid_data(self):
        """Test updating item with invalid data."""
        # Create item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        # Try to update with negative price
        invalid_update = {
            "name": "Updated Item",
            "price": -5.00,
            "category": "updated"
        }
        response = client.put(f"/items/{item_id}", json=invalid_update)
        assert response.status_code == 400

class TestDeleteItem:
    """Test item deletion functionality."""
    
    def test_delete_item_success(self, sample_item):
        """Test successful item deletion."""
        # Create item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == item_id
    
    def test_delete_item_not_found(self):
        """Test deleting non-existent item."""
        response = client.delete("/items/999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()

class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON in request body."""
        response = client.post("/items", data="invalid json")
        assert response.status_code == 422
    
    def test_malformed_request_data(self):
        """Test handling of malformed request data."""
        malformed_data = {"name": None, "price": "not a number"}
        response = client.post("/items", json=malformed_data)
        assert response.status_code == 422
    
    @patch('main.logger')
    def test_logging_on_errors(self, mock_logger):
        """Test that errors are properly logged."""
        # Trigger an error
        client.post("/items", json={"name": "", "price": -1, "category": "test"})
        
        # Verify logging was called
        assert mock_logger.error.called or mock_logger.warning.called

class TestPerformance:
    """Test performance characteristics."""
    
    def test_response_time(self):
        """Test that response times are reasonable."""
        import time
        
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get("/")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(errors) == 0
        assert all(status == 200 for status in results)

# Integration tests
class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_full_crud_workflow(self, sample_item):
        """Test complete CRUD workflow."""
        # Create
        create_response = client.post("/items", json=sample_item)
        assert create_response.status_code == 200
        item_id = create_response.json()["data"]["id"]
        
        # Read
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 200
        assert get_response.json()["data"]["id"] == item_id
        
        # Update
        update_data = {"name": "Updated", "price": 30.00, "category": "updated"}
        update_response = client.put(f"/items/{item_id}", json=update_data)
        assert update_response.status_code == 200
        
        # Verify update
        verify_response = client.get(f"/items/{item_id}")
        assert verify_response.json()["data"]["name"] == "Updated"
        
        # Delete
        delete_response = client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200
        
        # Verify deletion
        final_response = client.get(f"/items/{item_id}")
        assert final_response.json()["success"] is False

# Test configuration
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test."""
    # Setup: Clear the database
    global items_db, item_id_counter
    items_db.clear()
    item_id_counter = 1
    
    yield
    
    # Teardown: Clear the database
    items_db.clear()
    item_id_counter = 1

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])'''
    
    def _count_tests(self, tests: str) -> int:
        """Count the number of test functions."""
        return tests.count("def test_")
    
    def _analyze_test_types(self, tests: str) -> Dict[str, int]:
        """Analyze the types of tests present."""
        return {
            "unit_tests": tests.count("class Test") - tests.count("class TestIntegration"),
            "integration_tests": tests.count("class TestIntegration"),
            "performance_tests": tests.count("class TestPerformance"),
            "error_tests": tests.count("class TestErrorHandling"),
        }
    
    def _estimate_coverage(self, tests: str) -> float:
        """Estimate test coverage based on test content."""
        # Simple heuristic based on test count and complexity
        test_count = self._count_tests(tests)
        if test_count > 20:
            return 90.0
        elif test_count > 10:
            return 75.0
        elif test_count > 5:
            return 60.0
        else:
            return 40.0