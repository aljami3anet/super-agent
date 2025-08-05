"""
Base Agent Class

Provides the foundation for all AI agents in the system.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel

from ..config import settings
from ..services.logging import get_logger

logger = get_logger(__name__)


class AgentStatus(str, Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    DISABLED = "disabled"


class AgentType(str, Enum):
    """Agent type enumeration."""
    PLANNER = "planner"
    CODER = "coder"
    CRITIC = "critic"
    TESTER = "tester"
    SUMMARIZER = "summarizer"


@dataclass
class AgentResult:
    """Result from agent execution."""
    success: bool
    output: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    execution_time: float = 0.0
    tokens_used: int = 0
    cost: float = 0.0


class AgentRequest(BaseModel):
    """Request model for agent execution."""
    task: str
    context: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(
        self,
        agent_type: AgentType,
        name: str,
        description: str,
        enabled: bool = True,
        max_retries: int = 3,
        timeout: int = 300,
    ):
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.enabled = enabled
        self.max_retries = max_retries
        self.timeout = timeout
        
        self.status = AgentStatus.IDLE
        self.current_task: Optional[str] = None
        self.last_execution: Optional[datetime] = None
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_time = 0.0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        
        self.logger = get_logger(f"agent.{agent_type.value}")
    
    @abstractmethod
    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the agent's main logic."""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    async def run(self, request: AgentRequest) -> AgentResult:
        """Run the agent with retry logic and error handling."""
        if not self.enabled:
            return AgentResult(
                success=False,
                output="",
                error="Agent is disabled",
                execution_time=0.0
            )
        
        self.status = AgentStatus.RUNNING
        self.current_task = request.task
        start_time = datetime.now()
        
        try:
            for attempt in range(self.max_retries):
                try:
                    result = await asyncio.wait_for(
                        self.execute(request),
                        timeout=self.timeout
                    )
                    
                    # Update statistics
                    self.execution_count += 1
                    if result.success:
                        self.success_count += 1
                    else:
                        self.failure_count += 1
                    
                    self.total_execution_time += result.execution_time
                    self.total_tokens_used += result.tokens_used
                    self.total_cost += result.cost
                    
                    self.status = AgentStatus.SUCCESS if result.success else AgentStatus.FAILED
                    self.last_execution = datetime.now()
                    
                    return result
                    
                except asyncio.TimeoutError:
                    self.logger.warning(f"Agent {self.name} timed out on attempt {attempt + 1}")
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(1)  # Brief delay before retry
                    
                except Exception as e:
                    self.logger.error(f"Agent {self.name} failed on attempt {attempt + 1}: {e}")
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(1)  # Brief delay before retry
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            self.failure_count += 1
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.error(f"Agent {self.name} failed after {self.max_retries} attempts: {e}")
            
            return AgentResult(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time
            )
        
        finally:
            self.current_task = None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "agent_type": self.agent_type.value,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "status": self.status.value,
            "current_task": self.current_task,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.success_count / self.execution_count if self.execution_count > 0 else 0,
            "total_execution_time": self.total_execution_time,
            "total_tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "average_execution_time": self.total_execution_time / self.execution_count if self.execution_count > 0 else 0,
        }
    
    def reset_stats(self):
        """Reset agent statistics."""
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_time = 0.0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.last_execution = None
        self.status = AgentStatus.IDLE
        self.current_task = None
    
    def enable(self):
        """Enable the agent."""
        self.enabled = True
        self.status = AgentStatus.IDLE
    
    def disable(self):
        """Disable the agent."""
        self.enabled = False
        self.status = AgentStatus.DISABLED
        self.current_task = None