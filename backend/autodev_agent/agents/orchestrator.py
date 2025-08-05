"""
Agent Orchestrator

Coordinates all agents and manages the complete workflow from planning to execution.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from .base import BaseAgent, AgentRequest, AgentResult, AgentType, AgentStatus
from .planner import PlannerAgent
from .coder import CoderAgent
from .critic import CriticAgent
from .tester import TesterAgent
from .summarizer import SummarizerAgent
from ..services.logging import get_logger


class AgentOrchestrator:
    """Orchestrates the complete agent workflow."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Initialize all agents
        self.agents: Dict[AgentType, BaseAgent] = {
            AgentType.PLANNER: PlannerAgent(),
            AgentType.CODER: CoderAgent(),
            AgentType.CRITIC: CriticAgent(),
            AgentType.TESTER: TesterAgent(),
            AgentType.SUMMARIZER: SummarizerAgent(),
        }
        
        # Workflow state
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        
        # Statistics
        self.total_workflows = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
    
    async def execute_workflow(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        workflow_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute a complete workflow with all agents."""
        if workflow_id is None:
            workflow_id = str(uuid4())
        
        workflow = {
            "id": workflow_id,
            "task": task,
            "context": context or {},
            "user_id": user_id,
            "start_time": datetime.now(),
            "status": "running",
            "steps": [],
            "results": {},
            "error": None,
        }
        
        self.active_workflows[workflow_id] = workflow
        self.total_workflows += 1
        
        try:
            self.logger.info(f"Starting workflow {workflow_id} for task: {task}")
            
            # Step 1: Planning
            plan_result = await self._execute_planning(task, context, workflow_id)
            workflow["steps"].append({
                "agent": "planner",
                "status": "completed",
                "result": plan_result,
                "timestamp": datetime.now(),
            })
            
            if not plan_result["success"]:
                raise Exception(f"Planning failed: {plan_result['error']}")
            
            # Step 2: Coding
            code_result = await self._execute_coding(task, context, plan_result, workflow_id)
            workflow["steps"].append({
                "agent": "coder",
                "status": "completed",
                "result": code_result,
                "timestamp": datetime.now(),
            })
            
            if not code_result["success"]:
                raise Exception(f"Coding failed: {code_result['error']}")
            
            # Step 3: Code Review
            review_result = await self._execute_review(task, context, code_result, workflow_id)
            workflow["steps"].append({
                "agent": "critic",
                "status": "completed",
                "result": review_result,
                "timestamp": datetime.now(),
            })
            
            # Step 4: Testing
            test_result = await self._execute_testing(task, context, code_result, workflow_id)
            workflow["steps"].append({
                "agent": "tester",
                "status": "completed",
                "result": test_result,
                "timestamp": datetime.now(),
            })
            
            if not test_result["success"]:
                raise Exception(f"Testing failed: {test_result['error']}")
            
            # Step 5: Summarization
            summary_result = await self._execute_summarization(
                task, context, workflow["steps"], workflow_id
            )
            workflow["steps"].append({
                "agent": "summarizer",
                "status": "completed",
                "result": summary_result,
                "timestamp": datetime.now(),
            })
            
            # Workflow completed successfully
            workflow["status"] = "completed"
            workflow["end_time"] = datetime.now()
            workflow["duration"] = (workflow["end_time"] - workflow["start_time"]).total_seconds()
            
            self.successful_workflows += 1
            self.workflow_history.append(workflow)
            
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "steps": workflow["steps"],
                "summary": summary_result.get("output", ""),
                "duration": workflow["duration"],
            }
            
        except Exception as e:
            workflow["status"] = "failed"
            workflow["error"] = str(e)
            workflow["end_time"] = datetime.now()
            workflow["duration"] = (workflow["end_time"] - workflow["start_time"]).total_seconds()
            
            self.failed_workflows += 1
            self.workflow_history.append(workflow)
            
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "steps": workflow["steps"],
                "duration": workflow["duration"],
            }
        
        finally:
            # Clean up active workflow
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
    
    async def _execute_planning(
        self, task: str, context: Dict[str, Any], workflow_id: str
    ) -> Dict[str, Any]:
        """Execute the planning phase."""
        self.logger.info(f"Executing planning phase for workflow {workflow_id}")
        
        request = AgentRequest(
            task=task,
            context=context,
            conversation_id=workflow_id,
        )
        
        result = await self.agents[AgentType.PLANNER].run(request)
        
        return {
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata,
            "error": result.error,
            "execution_time": result.execution_time,
        }
    
    async def _execute_coding(
        self, task: str, context: Dict[str, Any], plan_result: Dict[str, Any], workflow_id: str
    ) -> Dict[str, Any]:
        """Execute the coding phase."""
        self.logger.info(f"Executing coding phase for workflow {workflow_id}")
        
        # Include planning results in context
        coding_context = {
            **context,
            "plan": plan_result.get("output", ""),
            "plan_metadata": plan_result.get("metadata", {}),
        }
        
        request = AgentRequest(
            task=task,
            context=coding_context,
            conversation_id=workflow_id,
        )
        
        result = await self.agents[AgentType.CODER].run(request)
        
        return {
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata,
            "error": result.error,
            "execution_time": result.execution_time,
        }
    
    async def _execute_review(
        self, task: str, context: Dict[str, Any], code_result: Dict[str, Any], workflow_id: str
    ) -> Dict[str, Any]:
        """Execute the code review phase."""
        self.logger.info(f"Executing review phase for workflow {workflow_id}")
        
        review_context = {
            **context,
            "code": code_result.get("output", ""),
            "code_metadata": code_result.get("metadata", {}),
        }
        
        request = AgentRequest(
            task=f"Review the generated code for: {task}",
            context=review_context,
            conversation_id=workflow_id,
        )
        
        result = await self.agents[AgentType.CRITIC].run(request)
        
        return {
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata,
            "error": result.error,
            "execution_time": result.execution_time,
        }
    
    async def _execute_testing(
        self, task: str, context: Dict[str, Any], code_result: Dict[str, Any], workflow_id: str
    ) -> Dict[str, Any]:
        """Execute the testing phase."""
        self.logger.info(f"Executing testing phase for workflow {workflow_id}")
        
        testing_context = {
            **context,
            "code": code_result.get("output", ""),
            "code_metadata": code_result.get("metadata", {}),
        }
        
        request = AgentRequest(
            task=f"Create tests for the generated code for: {task}",
            context=testing_context,
            conversation_id=workflow_id,
        )
        
        result = await self.agents[AgentType.TESTER].run(request)
        
        return {
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata,
            "error": result.error,
            "execution_time": result.execution_time,
        }
    
    async def _execute_summarization(
        self, task: str, context: Dict[str, Any], steps: List[Dict[str, Any]], workflow_id: str
    ) -> Dict[str, Any]:
        """Execute the summarization phase."""
        self.logger.info(f"Executing summarization phase for workflow {workflow_id}")
        
        # Create summary content from all steps
        summary_content = self._create_summary_content(task, steps)
        
        summary_context = {
            **context,
            "workflow_steps": steps,
            "task": task,
        }
        
        request = AgentRequest(
            task="Summarize the complete workflow execution",
            context=summary_context,
            conversation_id=workflow_id,
        )
        
        result = await self.agents[AgentType.SUMMARIZER].run(request)
        
        return {
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata,
            "error": result.error,
            "execution_time": result.execution_time,
        }
    
    def _create_summary_content(self, task: str, steps: List[Dict[str, Any]]) -> str:
        """Create content for summarization from workflow steps."""
        content = f"Task: {task}\n\n"
        content += "Workflow Execution Summary:\n\n"
        
        for i, step in enumerate(steps, 1):
            agent = step["agent"]
            result = step["result"]
            timestamp = step["timestamp"]
            
            content += f"Step {i}: {agent.title()} Agent\n"
            content += f"Timestamp: {timestamp}\n"
            content += f"Status: {'Success' if result.get('success') else 'Failed'}\n"
            content += f"Execution Time: {result.get('execution_time', 0):.2f}s\n"
            
            if result.get("error"):
                content += f"Error: {result['error']}\n"
            
            if result.get("output"):
                content += f"Output: {result['output'][:500]}...\n"
            
            content += "\n"
        
        return content
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        status = {}
        for agent_type, agent in self.agents.items():
            status[agent_type.value] = {
                "name": agent.name,
                "enabled": agent.enabled,
                "status": agent.status.value,
                "current_task": agent.current_task,
                "stats": agent.get_stats(),
            }
        return status
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow."""
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        
        # Check history
        for workflow in self.workflow_history:
            if workflow["id"] == workflow_id:
                return workflow
        
        return None
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent workflow history."""
        return self.workflow_history[-limit:] if self.workflow_history else []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "total_workflows": self.total_workflows,
            "successful_workflows": self.successful_workflows,
            "failed_workflows": self.failed_workflows,
            "success_rate": self.successful_workflows / self.total_workflows if self.total_workflows > 0 else 0,
            "active_workflows": len(self.active_workflows),
            "agent_status": self.get_agent_status(),
        }
    
    def reset_statistics(self):
        """Reset all statistics."""
        self.total_workflows = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.workflow_history.clear()
        self.active_workflows.clear()
        
        # Reset agent statistics
        for agent in self.agents.values():
            agent.reset_stats()
    
    def enable_agent(self, agent_type: AgentType):
        """Enable a specific agent."""
        if agent_type in self.agents:
            self.agents[agent_type].enable()
            self.logger.info(f"Enabled agent: {agent_type.value}")
    
    def disable_agent(self, agent_type: AgentType):
        """Disable a specific agent."""
        if agent_type in self.agents:
            self.agents[agent_type].disable()
            self.logger.info(f"Disabled agent: {agent_type.value}")
    
    def get_agent(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """Get a specific agent."""
        return self.agents.get(agent_type)
    
    def get_all_agents(self) -> Dict[AgentType, BaseAgent]:
        """Get all agents."""
        return self.agents.copy()