"""
Agents API endpoints.

This module provides API endpoints for managing and interacting
with the AI agents in the system.
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..agents.base import AgentRequest, AgentResult
from ..agents.coder import CoderAgent
from ..agents.critic import CriticAgent
from ..agents.planner import PlannerAgent
from ..agents.summarizer import SummarizerAgent
from ..agents.tester import TesterAgent
from ..services.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Initialize agents
agents = {
    "planner": PlannerAgent(),
    "coder": CoderAgent(),
    "critic": CriticAgent(),
    "tester": TesterAgent(),
    "summarizer": SummarizerAgent(),
}


class AgentListResponse(BaseModel):
    """Response model for listing agents."""
    agents: List[Dict[str, Any]]


class AgentExecuteRequest(BaseModel):
    """Request model for executing an agent."""
    task: str
    context: Dict[str, Any] = {}
    parameters: Dict[str, Any] = {}
    conversation_id: str = None
    user_id: str = None


class AgentExecuteResponse(BaseModel):
    """Response model for agent execution."""
    result: AgentResult


@router.get("/", response_model=AgentListResponse)
async def list_agents():
    """List all available agents."""
    return {
        "agents": [
            {
                "id": agent_id,
                "name": agent.name,
                "description": agent.description,
                "type": agent.agent_type.value,
                "enabled": agent.enabled,
                "stats": agent.get_stats(),
            }
            for agent_id, agent in agents.items()
        ]
    }


@router.get("/{agent_id}", response_model=Dict[str, Any])
async def get_agent(agent_id: str):
    """Get information about a specific agent."""
    if agent_id not in agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found",
        )
    
    agent = agents[agent_id]
    return {
        "id": agent_id,
        "name": agent.name,
        "description": agent.description,
        "type": agent.agent_type.value,
        "enabled": agent.enabled,
        "stats": agent.get_stats(),
    }


@router.post("/{agent_id}/execute", response_model=AgentExecuteResponse)
async def execute_agent(agent_id: str, request: AgentExecuteRequest):
    """Execute an agent with the given task."""
    if agent_id not in agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found",
        )
    
    agent = agents[agent_id]
    
    if not agent.enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agent '{agent_id}' is disabled",
        )
    
    try:
        # Create agent request
        agent_request = AgentRequest(
            task=request.task,
            context=request.context,
            parameters=request.parameters,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )
        
        # Execute agent
        result = await agent.run(agent_request)
        
        return {"result": result}
        
    except Exception as e:
        logger.error(f"Error executing agent '{agent_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing agent: {str(e)}",
        )


@router.post("/{agent_id}/enable")
async def enable_agent(agent_id: str):
    """Enable an agent."""
    if agent_id not in agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found",
        )
    
    agents[agent_id].enable()
    return {"status": "enabled"}


@router.post("/{agent_id}/disable")
async def disable_agent(agent_id: str):
    """Disable an agent."""
    if agent_id not in agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found",
        )
    
    agents[agent_id].disable()
    return {"status": "disabled"}


@router.post("/{agent_id}/reset-stats")
async def reset_agent_stats(agent_id: str):
    """Reset statistics for an agent."""
    if agent_id not in agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found",
        )
    
    agents[agent_id].reset_stats()
    return {"status": "stats_reset"}