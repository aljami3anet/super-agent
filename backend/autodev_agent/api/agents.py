"""
Agents API endpoints for AI Coder Agent.

This module provides API endpoints for:
- Agent orchestration
- Individual agent operations
- Agent status and health
- Agent configuration
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from ..agents.orchestrator import AgentOrchestrator
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response Models
class AgentRequest(BaseModel):
    """Request model for agent operations."""
    prompt: str = Field(..., description="The prompt for the agent")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    agent_type: Optional[str] = Field(default=None, description="Specific agent type to use")
    timeout: Optional[int] = Field(default=None, description="Request timeout in seconds")


class AgentResponse(BaseModel):
    """Response model for agent operations."""
    result: str = Field(..., description="Agent response")
    agent_type: str = Field(..., description="Type of agent used")
    model_used: str = Field(..., description="AI model used")
    cost: Optional[float] = Field(default=None, description="Cost of the request")
    duration: float = Field(..., description="Request duration in seconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentStatus(BaseModel):
    """Agent status model."""
    agent_type: str = Field(..., description="Type of agent")
    status: str = Field(..., description="Agent status")
    enabled: bool = Field(..., description="Whether agent is enabled")
    last_used: Optional[datetime] = Field(default=None, description="Last usage timestamp")
    total_requests: int = Field(default=0, description="Total requests processed")
    average_response_time: Optional[float] = Field(default=None, description="Average response time")


class OrchestrationRequest(BaseModel):
    """Request model for agent orchestration."""
    prompt: str = Field(..., description="The main prompt for orchestration")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    max_iterations: Optional[int] = Field(default=5, description="Maximum orchestration iterations")
    enable_critic: bool = Field(default=True, description="Enable critic agent")
    enable_tester: bool = Field(default=True, description="Enable tester agent")


class OrchestrationResponse(BaseModel):
    """Response model for agent orchestration."""
    final_result: str = Field(..., description="Final orchestrated result")
    iterations: List[Dict[str, Any]] = Field(..., description="Orchestration iterations")
    total_cost: float = Field(..., description="Total cost of orchestration")
    total_duration: float = Field(..., description="Total duration in seconds")
    agents_used: List[str] = Field(..., description="List of agents used")


# Global orchestrator instance
orchestrator = AgentOrchestrator()


@router.post("/process", response_model=AgentResponse)
async def process_with_agent(request: AgentRequest):
    """Process a request with a specific agent."""
    try:
        start_time = datetime.utcnow()
        
        # Determine agent type
        agent_type = request.agent_type or "coder"
        
        # Process with agent
        result = await orchestrator.process_with_agent(
            prompt=request.prompt,
            agent_type=agent_type,
            context=request.context,
            timeout=request.timeout or settings.AGENT_TIMEOUT
        )
        
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        return AgentResponse(
            result=result["response"],
            agent_type=agent_type,
            model_used=result.get("model_used", "unknown"),
            cost=result.get("cost"),
            duration=duration
        )
        
    except Exception as e:
        logger.error(f"Agent processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_agents(request: OrchestrationRequest):
    """Orchestrate multiple agents for complex tasks."""
    try:
        start_time = datetime.utcnow()
        
        # Run orchestration
        result = await orchestrator.orchestrate(
            prompt=request.prompt,
            context=request.context,
            max_iterations=request.max_iterations,
            enable_critic=request.enable_critic,
            enable_tester=request.enable_tester
        )
        
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        return OrchestrationResponse(
            final_result=result["final_result"],
            iterations=result["iterations"],
            total_cost=result.get("total_cost", 0.0),
            total_duration=duration,
            agents_used=result.get("agents_used", [])
        )
        
    except Exception as e:
        logger.error(f"Agent orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=List[AgentStatus])
async def get_agent_status():
    """Get status of all agents."""
    try:
        return await orchestrator.get_agent_status()
    except Exception as e:
        logger.error(f"Failed to get agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{agent_type}", response_model=AgentStatus)
async def get_agent_status_by_type(agent_type: str):
    """Get status of a specific agent."""
    try:
        status = await orchestrator.get_agent_status_by_type(agent_type)
        if not status:
            raise HTTPException(status_code=404, detail=f"Agent {agent_type} not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent status for {agent_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enable/{agent_type}")
async def enable_agent(agent_type: str):
    """Enable a specific agent."""
    try:
        success = await orchestrator.enable_agent(agent_type)
        if not success:
            raise HTTPException(status_code=404, detail=f"Agent {agent_type} not found")
        return {"message": f"Agent {agent_type} enabled"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to enable agent {agent_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disable/{agent_type}")
async def disable_agent(agent_type: str):
    """Disable a specific agent."""
    try:
        success = await orchestrator.disable_agent(agent_type)
        if not success:
            raise HTTPException(status_code=404, detail=f"Agent {agent_type} not found")
        return {"message": f"Agent {agent_type} disabled"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to disable agent {agent_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/available")
async def get_available_agents():
    """Get list of available agent types."""
    try:
        return {
            "available_agents": [
                "planner",
                "coder", 
                "critic",
                "tester",
                "summarizer"
            ],
            "enabled_agents": {
                "planner": settings.PLANNER_AGENT_ENABLED,
                "coder": settings.CODER_AGENT_ENABLED,
                "critic": settings.CRITIC_AGENT_ENABLED,
                "tester": settings.TESTER_AGENT_ENABLED,
                "summarizer": settings.SUMMARIZER_AGENT_ENABLED,
            }
        }
    except Exception as e:
        logger.error(f"Failed to get available agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_agents():
    """Reset all agents to initial state."""
    try:
        await orchestrator.reset()
        return {"message": "All agents reset successfully"}
    except Exception as e:
        logger.error(f"Failed to reset agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def agent_health():
    """Get health status of agent system."""
    try:
        health = await orchestrator.get_health()
        return health
    except Exception as e:
        logger.error(f"Failed to get agent health: {e}")
        raise HTTPException(status_code=500, detail=str(e))