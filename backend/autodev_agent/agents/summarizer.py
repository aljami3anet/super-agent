"""
Summarizer Agent

Responsible for summarizing conversations and project progress.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class SummarizerAgent(BaseAgent):
    """Summarizer agent for summarizing conversations and project progress."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.SUMMARIZER,
            name="Summarizer",
            description="Summarizes conversations and project progress",
            enabled=True,
            max_retries=3,
            timeout=300,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a conversation and project summarization AI agent. Your role is to:

1. Analyze conversations and extract key information
2. Summarize project progress and achievements
3. Identify important decisions and action items
4. Create concise, readable summaries
5. Maintain context across multiple conversations
6. Generate project status updates

When summarizing, always:
- Identify key points and main ideas
- Extract important decisions and conclusions
- Note action items and next steps
- Maintain context and continuity
- Keep summaries concise and readable
- Organize information logically

Generate clear, concise summaries that capture essential information."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the summarization logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            
            # Build the prompt
            prompt = self._build_summarization_prompt(task, context)
            
            # Generate the summary
            summary = await self._generate_summary(prompt)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=summary,
                metadata={
                    "original_length": len(task),
                    "summary_length": len(summary),
                    "compression_ratio": round(len(summary) / len(task), 2) if task else 0,
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
    
    def _build_summarization_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build the summarization prompt."""
        prompt = f"{self.get_system_prompt()}\n\n"
        prompt += f"CONTENT TO SUMMARIZE: {task}\n\n"
        
        if context:
            prompt += "CONTEXT:\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += """Please provide a concise summary of this content. Include:

1. Key points and main ideas
2. Important decisions and conclusions
3. Action items and next steps
4. Relevant context and background

Generate a clear, concise summary that captures the essential information."""
        
        return prompt
    
    async def _generate_summary(self, prompt: str) -> str:
        """Generate the summary."""
        # In a real implementation, this would call an AI model
        # For now, return a placeholder summary
        return """
# Summary

## Key Points
- Discussed project requirements and specifications
- Identified technical challenges and solutions
- Agreed on implementation approach

## Decisions
- Use Python and FastAPI for backend
- Use React and TypeScript for frontend
- Implement multi-agent architecture

## Action Items
1. Complete backend implementation
2. Develop frontend components
3. Integrate agents and workflows
4. Implement testing and quality gates

## Next Steps
- Proceed with Phase 5: Testing and Quality Gates
- Set up CI/CD pipelines
- Prepare for deployment
"""