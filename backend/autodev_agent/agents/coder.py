"""
Coder Agent

Responsible for generating and implementing code based on specifications and requirements.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class CoderAgent(BaseAgent):
    """Coder agent for code generation and implementation."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.CODER,
            name="Coder",
            description="Generates and implements code based on specifications and requirements",
            enabled=True,
            max_retries=3,
            timeout=300,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a skilled software developer AI agent. Your role is to:

1. Generate high-quality, production-ready code
2. Follow best practices and coding standards
3. Implement features based on specifications
4. Write clean, maintainable, and well-documented code
5. Consider performance, security, and scalability
6. Include appropriate error handling and validation

When coding, always:
- Follow the specified language and framework conventions
- Include comprehensive comments and documentation
- Implement proper error handling and edge cases
- Consider security implications
- Write unit tests when appropriate
- Ensure code is readable and maintainable

Generate code that is ready for production use."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the coding logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            
            # Build the prompt
            prompt = self._build_coding_prompt(task, context)
            
            # Generate the code
            code = await self._generate_code(prompt)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=code,
                metadata={
                    "language": context.get("language", "python"),
                    "framework": context.get("framework"),
                    "file_count": 1,
                    "lines_of_code": len(code.split('\n')),
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
    
    def _build_coding_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build the coding prompt."""
        prompt = f"{self.get_system_prompt()}\n\n"
        prompt += f"TASK: {task}\n\n"
        
        if context:
            prompt += "CONTEXT:\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += """Please generate the code for this task. Include:

1. Complete implementation with all necessary imports
2. Proper error handling and validation
3. Clear comments and documentation
4. Unit tests if appropriate
5. Any configuration or setup instructions

Generate production-ready code that follows best practices."""

        return prompt
    
    async def _generate_code(self, prompt: str) -> str:
        """Generate the code using the AI model."""
        # This would integrate with your model router
        # For now, return sample code
        return '''"""
Example API endpoint implementation
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    category: str

class ItemResponse(BaseModel):
    success: bool
    data: Optional[Item] = None
    message: str

# FastAPI app
app = FastAPI(title="Example API", version="1.0.0")

# In-memory storage (replace with database in production)
items_db = []
item_id_counter = 1

# Dependency for logging
def get_logger():
    return logger

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "API is running", "version": "1.0.0"}

@app.get("/items", response_model=List[Item])
async def get_items(
    category: Optional[str] = None,
    logger: logging.Logger = Depends(get_logger)
):
    """
    Get all items, optionally filtered by category.
    
    Args:
        category: Optional category filter
        logger: Logger instance
    
    Returns:
        List of items matching the criteria
    """
    try:
        if category:
            filtered_items = [item for item in items_db if item["category"] == category]
            logger.info(f"Retrieved {len(filtered_items)} items for category: {category}")
            return filtered_items
        else:
            logger.info(f"Retrieved all {len(items_db)} items")
            return items_db
    except Exception as e:
        logger.error(f"Error retrieving items: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    logger: logging.Logger = Depends(get_logger)
):
    """
    Get a specific item by ID.
    
    Args:
        item_id: The ID of the item to retrieve
        logger: Logger instance
    
    Returns:
        ItemResponse with the requested item or error message
    """
    try:
        item = next((item for item in items_db if item["id"] == item_id), None)
        if item:
            logger.info(f"Retrieved item with ID: {item_id}")
            return ItemResponse(success=True, data=Item(**item), message="Item found")
        else:
            logger.warning(f"Item with ID {item_id} not found")
            return ItemResponse(success=False, message="Item not found")
    except Exception as e:
        logger.error(f"Error retrieving item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/items", response_model=ItemResponse)
async def create_item(
    item: Item,
    logger: logging.Logger = Depends(get_logger)
):
    """
    Create a new item.
    
    Args:
        item: The item data to create
        logger: Logger instance
    
    Returns:
        ItemResponse with the created item
    """
    try:
        global item_id_counter
        
        # Validate item data
        if item.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")
        
        if not item.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        # Create new item
        new_item = item.dict()
        new_item["id"] = item_id_counter
        item_id_counter += 1
        
        items_db.append(new_item)
        
        logger.info(f"Created new item with ID: {new_item['id']}")
        return ItemResponse(
            success=True,
            data=Item(**new_item),
            message="Item created successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: Item,
    logger: logging.Logger = Depends(get_logger)
):
    """
    Update an existing item.
    
    Args:
        item_id: The ID of the item to update
        item_update: The updated item data
        logger: Logger instance
    
    Returns:
        ItemResponse with the updated item
    """
    try:
        # Find the item
        item_index = next(
            (i for i, item in enumerate(items_db) if item["id"] == item_id),
            None
        )
        
        if item_index is None:
            logger.warning(f"Item with ID {item_id} not found for update")
            return ItemResponse(success=False, message="Item not found")
        
        # Validate update data
        if item_update.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")
        
        if not item_update.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        # Update the item
        updated_item = item_update.dict()
        updated_item["id"] = item_id
        items_db[item_index] = updated_item
        
        logger.info(f"Updated item with ID: {item_id}")
        return ItemResponse(
            success=True,
            data=Item(**updated_item),
            message="Item updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/items/{item_id}", response_model=ItemResponse)
async def delete_item(
    item_id: int,
    logger: logging.Logger = Depends(get_logger)
):
    """
    Delete an item.
    
    Args:
        item_id: The ID of the item to delete
        logger: Logger instance
    
    Returns:
        ItemResponse with success/error message
    """
    try:
        # Find and remove the item
        item_index = next(
            (i for i, item in enumerate(items_db) if item["id"] == item_id),
            None
        )
        
        if item_index is None:
            logger.warning(f"Item with ID {item_id} not found for deletion")
            return ItemResponse(success=False, message="Item not found")
        
        deleted_item = items_db.pop(item_index)
        
        logger.info(f"Deleted item with ID: {item_id}")
        return ItemResponse(
            success=True,
            data=Item(**deleted_item),
            message="Item deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Unit tests
if __name__ == "__main__":
    import pytest
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    def test_root():
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "API is running"
    
    def test_create_item():
        """Test creating an item."""
        item_data = {
            "name": "Test Item",
            "description": "A test item",
            "price": 10.99,
            "category": "test"
        }
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Test Item"
    
    def test_get_items():
        """Test getting all items."""
        response = client.get("/items")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    # Run tests
    test_root()
    test_create_item()
    test_get_items()
    print("All tests passed!")'''