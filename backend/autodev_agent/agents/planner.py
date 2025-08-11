"""
Planner Agent

Responsible for planning and organizing tasks to be completed by other agents.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class PlannerAgent(BaseAgent):
    """Planner agent for task planning and organization."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.PLANNER,
            name="Planner",
            description="Plans and organizes tasks to be completed by other agents",
            enabled=True,
            max_retries=3,
            timeout=300,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a task planning AI agent. Your role is to:

1. Analyze user requests and break them down into manageable tasks
2. Create a structured plan with clear steps and dependencies
3. Assign tasks to appropriate specialized agents
4. Consider resource constraints and time requirements
5. Identify potential risks and mitigation strategies
6. Provide clear instructions and context for each task

When planning, always:
- Consider the overall goal and objectives
- Break down complex tasks into smaller, manageable steps
- Identify dependencies between tasks
- Estimate time and resource requirements
- Consider potential risks and challenges
- Provide clear, actionable instructions

Generate comprehensive plans that enable efficient task execution."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the planning logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            
            # Build the prompt
            prompt = self._build_planning_prompt(task, context)
            
            # Generate the plan
            plan = await self._generate_plan(prompt)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=plan,
                metadata={
                    "task_count": self._count_tasks(plan),
                    "estimated_duration": self._estimate_duration(plan),
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
    
    def _build_planning_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build the planning prompt."""
        prompt = f"{self.get_system_prompt()}\n\n"
        prompt += f"TASK: {task}\n\n"
        
        if context:
            prompt += "CONTEXT:\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += """Please create a comprehensive plan for this task. Include:

1. Overall goal and objectives
2. Breakdown into specific tasks and subtasks
3. Dependencies between tasks
4. Resource requirements and constraints
5. Timeline and milestones
6. Risk assessment and mitigation strategies
7. Success criteria and metrics

Generate a structured plan that can be executed by specialized agents."""
        
        return prompt
    
    async def _generate_plan(self, prompt: str) -> str:
        """Generate the plan."""
        # In a real implementation, this would call an AI model
        # For now, return a placeholder plan
        return """
# Project Plan

## Goal
Complete the requested task efficiently and effectively.

## Tasks
1. Analyze requirements
2. Design solution
3. Implement solution
4. Test solution
5. Deploy solution

## Timeline
- Task 1: 1 day
- Task 2: 2 days
- Task 3: 3 days
- Task 4: 1 day
- Task 5: 1 day

## Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 3
- Task 5 depends on Task 4

## Risks
- Technical challenges
- Resource constraints
- Time constraints

## Mitigation
- Regular progress reviews
- Contingency planning
- Resource optimization
"""
    
    def _count_tasks(self, plan: str) -> int:
        """Count the number of tasks in a plan."""
        # Simple heuristic: count lines that start with a number
        lines = plan.split('\n')
        return sum(1 for line in lines if line.strip() and line.strip()[0].isdigit())
    
    def _estimate_duration(self, plan: str) -> str:
        """Estimate the duration of a plan."""
        # Simple heuristic: return a fixed estimate
        return "5 days"