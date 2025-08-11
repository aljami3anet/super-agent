"""
Orchestrator Agent

Responsible for coordinating and managing the execution of other agents.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType
from .coder import CoderAgent
from .critic import CriticAgent
from .planner import PlannerAgent
from .summarizer import SummarizerAgent
from .tester import TesterAgent

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    """Orchestrator agent for coordinating and managing other agents."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.PLANNER,  # Using PLANNER type as there's no ORCHESTRATOR type
            name="Orchestrator",
            description="Coordinates and manages the execution of other agents",
            enabled=True,
            max_retries=3,
            timeout=600,  # Longer timeout for orchestration
        )
        
        # Initialize agents
        self.agents = {
            "planner": PlannerAgent(),
            "coder": CoderAgent(),
            "critic": CriticAgent(),
            "tester": TesterAgent(),
            "summarizer": SummarizerAgent(),
        }
    
    def get_system_prompt(self) -> str:
        return """You are an orchestration AI agent. Your role is to:

1. Coordinate and manage the execution of other agents
2. Determine the optimal sequence of agent operations
3. Handle errors and retries appropriately
4. Aggregate results from multiple agents
5. Ensure efficient resource utilization
6. Monitor and track progress of agent execution

When orchestrating, always:
- Consider dependencies between agents
- Optimize for efficiency and quality
- Handle errors gracefully with retries
- Aggregate and synthesize results
- Monitor resource usage and constraints
- Provide clear status updates

Generate effective orchestration plans that maximize productivity and quality."""
    
    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the orchestration logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            
            # Execute the agent workflow
            result = await self._execute_workflow(task, context)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=result["success"],
                output=result["output"],
                metadata={
                    "agents_executed": result["agents_executed"],
                    "total_execution_time": result["total_execution_time"],
                    "workflow_steps": result["workflow_steps"],
                },
                execution_time=execution_time,
                tokens_used=result.get("tokens_used", 0),
                cost=result.get("cost", 0.0),
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Orchestration failed: {e}")
            return AgentResult(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time
            )
    
    async def _execute_workflow(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent workflow."""
        workflow_steps = []
        agents_executed = []
        total_execution_time = 0.0
        total_tokens_used = 0
        total_cost = 0.0
        
        # Step 1: Planning
        logger.info("Starting planning phase")
        workflow_steps.append("Planning")
        
        planner_request = AgentRequest(
            task=task,
            context=context,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )
        
        planner_result = await self.agents["planner"].run(planner_request)
        agents_executed.append("planner")
        total_execution_time += planner_result.execution_time
        total_tokens_used += planner_result.tokens_used
        total_cost += planner_result.cost
        
        if not planner_result.success:
            return {
                "success": False,
                "output": "Planning failed",
                "agents_executed": agents_executed,
                "total_execution_time": total_execution_time,
                "workflow_steps": workflow_steps,
                "tokens_used": total_tokens_used,
                "cost": total_cost,
            }
        
        # Step 2: Coding
        logger.info("Starting coding phase")
        workflow_steps.append("Coding")
        
        coder_context = {
            **context,
            "plan": planner_result.output,
        }
        
        coder_request = AgentRequest(
            task=task,
            context=coder_context,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )
        
        coder_result = await self.agents["coder"].run(coder_request)
        agents_executed.append("coder")
        total_execution_time += coder_result.execution_time
        total_tokens_used += coder_result.tokens_used
        total_cost += coder_result.cost
        
        if not coder_result.success:
            return {
                "success": False,
                "output": "Coding failed",
                "agents_executed": agents_executed,
                "total_execution_time": total_execution_time,
                "workflow_steps": workflow_steps,
                "tokens_used": total_tokens_used,
                "cost": total_cost,
            }
        
        # Step 3: Critique
        logger.info("Starting critique phase")
        workflow_steps.append("Critique")
        
        critic_context = {
            **context,
            "plan": planner_result.output,
            "code": coder_result.output,
        }
        
        critic_request = AgentRequest(
            task=task,
            context=critic_context,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )
        
        critic_result = await self.agents["critic"].run(critic_request)
        agents_executed.append("critic")
        total_execution_time += critic_result.execution_time
        total_tokens_used += critic_result.tokens_used
        total_cost += critic_result.cost
        
        # Step 4: Testing
        logger.info("Starting testing phase")
        workflow_steps.append("Testing")
        
        tester_context = {
            **context,
            "plan": planner_result.output,
            "code": coder_result.output,
            "critique": critic_result.output,
        }
        
        tester_request = AgentRequest(
            task=task,
            context=tester_context,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )
        
        tester_result = await self.agents["tester"].run(tester_request)
        agents_executed.append("tester")
        total_execution_time += tester_result.execution_time
        total_tokens_used += tester_result.tokens_used
        total_cost += tester_result.cost
        
        # Step 5: Summarization
        logger.info("Starting summarization phase")
        workflow_steps.append("Summarization")
        
        summarizer_context = {
            **context,
            "plan": planner_result.output,
            "code": coder_result.output,
            "critique": critic_result.output,
            "test_results": tester_result.output,
        }
        
        summarizer_request = AgentRequest(
            task=task,
            context=summarizer_context,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )
        
        summarizer_result = await self.agents["summarizer"].run(summarizer_request)
        agents_executed.append("summarizer")
        total_execution_time += summarizer_result.execution_time
        total_tokens_used += summarizer_result.tokens_used
        total_cost += summarizer_result.cost
        
        # Combine results
        output = f"""
# Execution Summary

## Plan
{planner_result.output}

## Code
{coder_result.output}

## Critique
{critic_result.output}

## Test Results
{tester_result.output}

## Summary
{summarizer_result.output}
"""
        
        return {
            "success": True,
            "output": output,
            "agents_executed": agents_executed,
            "total_execution_time": total_execution_time,
            "workflow_steps": workflow_steps,
            "tokens_used": total_tokens_used,
            "cost": total_cost,
        }