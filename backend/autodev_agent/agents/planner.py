"""
Planner Agent

Responsible for breaking down complex tasks into actionable steps and creating execution strategies.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class PlannerAgent(BaseAgent):
    """Planner agent for task decomposition and strategy creation."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.PLANNER,
            name="Planner",
            description="Breaks down complex tasks into actionable steps and creates execution strategies",
            enabled=True,
            max_retries=3,
            timeout=120,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a strategic planning AI agent. Your role is to:

1. Analyze complex tasks and break them down into clear, actionable steps
2. Create execution strategies that optimize for efficiency and quality
3. Identify potential challenges and dependencies
4. Prioritize tasks based on importance and dependencies
5. Consider resource constraints and time limitations

When planning, always:
- Break tasks into specific, measurable steps
- Identify dependencies between steps
- Estimate effort and time requirements
- Consider potential risks and mitigation strategies
- Ensure the plan is realistic and achievable

Output your plan in a structured format that can be easily parsed and executed by other agents."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the planning logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            
            # Build the prompt
            prompt = self._build_planning_prompt(task, context)
            
            # Call the AI model (this would integrate with your model router)
            # For now, we'll simulate the response
            plan = await self._generate_plan(prompt)
            
            # Parse and structure the plan
            structured_plan = self._parse_plan(plan)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=plan,
                metadata={
                    "structured_plan": structured_plan,
                    "steps_count": len(structured_plan.get("steps", [])),
                    "estimated_duration": structured_plan.get("estimated_duration"),
                    "priority": structured_plan.get("priority"),
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
        
        prompt += """Please create a detailed plan for this task. Include:

1. Task breakdown into specific steps
2. Dependencies between steps
3. Estimated effort for each step
4. Potential risks and mitigation strategies
5. Success criteria for each step
6. Overall timeline and milestones

Format your response as a structured plan that can be easily parsed."""

        return prompt
    
    async def _generate_plan(self, prompt: str) -> str:
        """Generate the plan using the AI model."""
        # This would integrate with your model router
        # For now, return a sample plan
        return """# Task Execution Plan

## Overview
Break down the given task into manageable steps with clear dependencies and success criteria.

## Steps

### Step 1: Analysis and Requirements Gathering
- **Description**: Understand the task requirements and constraints
- **Effort**: 2-4 hours
- **Dependencies**: None
- **Success Criteria**: Clear understanding of requirements documented
- **Risks**: Incomplete requirements
- **Mitigation**: Ask clarifying questions, document assumptions

### Step 2: Design and Architecture
- **Description**: Create high-level design and architecture
- **Effort**: 4-8 hours
- **Dependencies**: Step 1
- **Success Criteria**: Architecture diagram and design document
- **Risks**: Over-engineering or under-designing
- **Mitigation**: Review with stakeholders, consider alternatives

### Step 3: Implementation
- **Description**: Implement the solution following the design
- **Effort**: 8-16 hours
- **Dependencies**: Step 2
- **Success Criteria**: Working implementation with tests
- **Risks**: Scope creep, technical debt
- **Mitigation**: Regular reviews, incremental development

### Step 4: Testing and Validation
- **Description**: Test the implementation thoroughly
- **Effort**: 4-8 hours
- **Dependencies**: Step 3
- **Success Criteria**: All tests pass, no critical bugs
- **Risks**: Incomplete testing
- **Mitigation**: Automated tests, manual testing checklist

### Step 5: Documentation and Deployment
- **Description**: Document the solution and deploy
- **Effort**: 2-4 hours
- **Dependencies**: Step 4
- **Success Criteria**: Documentation complete, deployed successfully
- **Risks**: Poor documentation, deployment issues
- **Mitigation**: Documentation templates, deployment checklist

## Timeline
- **Total Estimated Duration**: 20-40 hours
- **Critical Path**: Steps 1 → 2 → 3 → 4 → 5
- **Milestones**: Requirements (Day 1), Design (Day 2-3), Implementation (Day 4-7), Testing (Day 8-9), Deployment (Day 10)

## Priority
High - This is a core functionality that affects the entire system."""
    
    def _parse_plan(self, plan: str) -> Dict[str, Any]:
        """Parse the plan into a structured format."""
        # This would parse the markdown/structured plan
        # For now, return a basic structure
        return {
            "steps": [
                {
                    "id": 1,
                    "name": "Analysis and Requirements Gathering",
                    "description": "Understand the task requirements and constraints",
                    "effort": "2-4 hours",
                    "dependencies": [],
                    "success_criteria": "Clear understanding of requirements documented",
                    "risks": ["Incomplete requirements"],
                    "mitigation": ["Ask clarifying questions", "Document assumptions"]
                },
                {
                    "id": 2,
                    "name": "Design and Architecture",
                    "description": "Create high-level design and architecture",
                    "effort": "4-8 hours",
                    "dependencies": [1],
                    "success_criteria": "Architecture diagram and design document",
                    "risks": ["Over-engineering", "Under-designing"],
                    "mitigation": ["Review with stakeholders", "Consider alternatives"]
                },
                {
                    "id": 3,
                    "name": "Implementation",
                    "description": "Implement the solution following the design",
                    "effort": "8-16 hours",
                    "dependencies": [2],
                    "success_criteria": "Working implementation with tests",
                    "risks": ["Scope creep", "Technical debt"],
                    "mitigation": ["Regular reviews", "Incremental development"]
                },
                {
                    "id": 4,
                    "name": "Testing and Validation",
                    "description": "Test the implementation thoroughly",
                    "effort": "4-8 hours",
                    "dependencies": [3],
                    "success_criteria": "All tests pass, no critical bugs",
                    "risks": ["Incomplete testing"],
                    "mitigation": ["Automated tests", "Manual testing checklist"]
                },
                {
                    "id": 5,
                    "name": "Documentation and Deployment",
                    "description": "Document the solution and deploy",
                    "effort": "2-4 hours",
                    "dependencies": [4],
                    "success_criteria": "Documentation complete, deployed successfully",
                    "risks": ["Poor documentation", "Deployment issues"],
                    "mitigation": ["Documentation templates", "Deployment checklist"]
                }
            ],
            "estimated_duration": "20-40 hours",
            "priority": "High",
            "critical_path": [1, 2, 3, 4, 5],
            "milestones": [
                {"day": 1, "milestone": "Requirements"},
                {"day": 2, "milestone": "Design"},
                {"day": 4, "milestone": "Implementation"},
                {"day": 8, "milestone": "Testing"},
                {"day": 10, "milestone": "Deployment"}
            ]
        }