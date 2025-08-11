"""
Tools API endpoints.

This module provides API endpoints for managing and executing
tools that can be used by the AI agents.
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..services.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class Tool(BaseModel):
    """Tool model."""
    id: str
    name: str
    description: str
    parameters: Dict[str, Any]
    enabled: bool = True


class ToolListResponse(BaseModel):
    """Response model for listing tools."""
    tools: List[Tool]


class ToolExecuteRequest(BaseModel):
    """Request model for executing a tool."""
    tool_id: str
    parameters: Dict[str, Any]


class ToolExecuteResponse(BaseModel):
    """Response model for tool execution."""
    result: Any
    execution_time: float


# In-memory storage for tools (in a real app, this would be a database)
tools_db = {
    "read_file": Tool(
        id="read_file",
        name="Read File",
        description="Read the contents of a file",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to read",
                }
            },
            "required": ["path"],
        },
    ),
    "write_file": Tool(
        id="write_file",
        name="Write File",
        description="Write content to a file",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to write",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["path", "content"],
        },
    ),
    "list_dir": Tool(
        id="list_dir",
        name="List Directory",
        description="List the contents of a directory",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the directory to list",
                }
            },
            "required": ["path"],
        },
    ),
    "execute_shell": Tool(
        id="execute_shell",
        name="Execute Shell Command",
        description="Execute a shell command",
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute",
                }
            },
            "required": ["command"],
        },
    ),
}


@router.get("/", response_model=ToolListResponse)
async def list_tools():
    """List all available tools."""
    return {"tools": list(tools_db.values())}


@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: str):
    """Get information about a specific tool."""
    if tool_id not in tools_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_id}' not found",
        )
    
    return tools_db[tool_id]


@router.post("/{tool_id}/execute", response_model=ToolExecuteResponse)
async def execute_tool(tool_id: str, request: ToolExecuteRequest):
    """Execute a tool with the given parameters."""
    if tool_id not in tools_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_id}' not found",
        )
    
    tool = tools_db[tool_id]
    
    if not tool.enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tool '{tool_id}' is disabled",
        )
    
    try:
        # Execute the tool
        import time
        start_time = time.time()
        
        # In a real implementation, this would call the actual tool function
        result = f"Executed {tool_id} with parameters: {request.parameters}"
        
        execution_time = time.time() - start_time
        
        logger.info(f"Executed tool '{tool_id}' with parameters: {request.parameters}")
        
        return {
            "result": result,
            "execution_time": execution_time,
        }
        
    except Exception as e:
        logger.error(f"Error executing tool '{tool_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing tool: {str(e)}",
        )


@router.post("/{tool_id}/enable")
async def enable_tool(tool_id: str):
    """Enable a tool."""
    if tool_id not in tools_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_id}' not found",
        )
    
    tools_db[tool_id].enabled = True
    return {"status": "enabled"}


@router.post("/{tool_id}/disable")
async def disable_tool(tool_id: str):
    """Disable a tool."""
    if tool_id not in tools_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_id}' not found",
        )
    
    tools_db[tool_id].enabled = False
    return {"status": "disabled"}