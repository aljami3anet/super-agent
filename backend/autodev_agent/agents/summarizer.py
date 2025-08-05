"""
Summarizer Agent

Responsible for summarizing conversations and code to maintain context and reduce memory usage.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class SummarizerAgent(BaseAgent):
    """Summarizer agent for conversation and code summarization."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.SUMMARIZER,
            name="Summarizer",
            description="Summarizes conversations and code to maintain context and reduce memory usage",
            enabled=True,
            max_retries=3,
            timeout=120,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a summarization specialist AI agent. Your role is to:

1. Create concise, accurate summaries of conversations and code
2. Preserve important context and key information
3. Identify and highlight critical decisions and actions
4. Maintain chronological order of events
5. Extract actionable insights and next steps
6. Reduce information while maintaining essential details

When summarizing, always:
- Focus on the most important information
- Preserve context that will be needed later
- Highlight decisions, actions, and outcomes
- Include any errors, issues, or lessons learned
- Maintain a clear timeline of events
- Extract key insights and patterns

Create summaries that are both concise and comprehensive."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the summarization logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            content = context.get("content", "")
            
            # Build the prompt
            prompt = self._build_summarization_prompt(task, content, context)
            
            # Generate the summary
            summary = await self._generate_summary(prompt)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=summary,
                metadata={
                    "original_length": len(content),
                    "summary_length": len(summary),
                    "compression_ratio": len(summary) / len(content) if content else 0,
                    "key_points": self._extract_key_points(summary),
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
    
    def _build_summarization_prompt(self, task: str, content: str, context: Dict[str, Any]) -> str:
        """Build the summarization prompt."""
        prompt = f"{self.get_system_prompt()}\n\n"
        prompt += f"TASK: {task}\n\n"
        
        if context:
            prompt += "CONTEXT:\n"
            for key, value in context.items():
                if key != "content":
                    prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += f"CONTENT TO SUMMARIZE:\n```\n{content}\n```\n\n"
        prompt += """Please create a comprehensive summary. Include:

1. Key decisions and actions taken
2. Important context and background information
3. Outcomes and results achieved
4. Issues encountered and how they were resolved
5. Lessons learned and insights gained
6. Next steps or pending actions
7. Critical information for future reference

Format your summary clearly with sections for different types of information."""

        return prompt
    
    async def _generate_summary(self, prompt: str) -> str:
        """Generate the summary using the AI model."""
        # This would integrate with your model router
        # For now, return a sample summary
        return """# Conversation Summary

## Overview
This session focused on developing a comprehensive AI Coder Agent system with multi-agent orchestration. The team worked on implementing the core architecture and establishing the foundational components.

## Key Decisions Made

### Architecture Decisions
- **Monorepo Structure**: Chose to organize backend (Python) and frontend (React) in a single repository for better coordination
- **Agent System**: Implemented a multi-agent architecture with specialized roles (Planner, Coder, Critic, Tester, Summarizer)
- **Technology Stack**: Selected FastAPI for backend, React + TypeScript for frontend, PostgreSQL for persistence
- **Observability**: Integrated OpenTelemetry for comprehensive monitoring and tracing

### Implementation Decisions
- **Configuration Management**: Used Pydantic for robust configuration with environment variable precedence
- **Error Handling**: Implemented comprehensive error handling with retry logic and fallback mechanisms
- **Testing Strategy**: Established multi-level testing approach (unit, integration, E2E)
- **Documentation**: Created comprehensive documentation with architecture diagrams and deployment guides

## Actions Completed

### Phase 1: Project Initialization ✅
- Created monorepo skeleton with proper directory structure
- Set up Git repository with initial commit
- Added essential project files (.gitignore, LICENSE, README.md, etc.)
- Configured Docker and Docker Compose for containerization
- Established documentation and infrastructure folders

### Phase 2: Backend Scaffold ✅
- Implemented comprehensive Python package structure
- Created FastAPI application with health checks and API routes
- Integrated OpenTelemetry for observability
- Implemented logging system with JSON and human-readable formats
- Created tool functions for file operations, Git, and system tasks
- Established agent base classes and orchestration framework
- Implemented PostgreSQL data layer with health checks

### Phase 3: Frontend Scaffold ✅
- Set up React application with Vite and TypeScript
- Implemented Tailwind CSS with dark mode support
- Created core UI components (AppShell, Sidebar, ThemeProvider)
- Built responsive pages (Dashboard, Logs, Config, Agents, Conversations)
- Established testing setup with Jest and React Testing Library

## Outcomes Achieved

### Technical Achievements
- **Modular Architecture**: Successfully implemented a clean, modular architecture that separates concerns
- **Comprehensive Tooling**: Created extensive tool functions for development automation
- **Modern UI**: Built a responsive, accessible frontend with modern design patterns
- **Robust Configuration**: Implemented flexible configuration management system
- **Observability**: Established comprehensive monitoring and logging infrastructure

### Quality Improvements
- **Error Handling**: Implemented robust error handling with retry logic
- **Testing**: Established comprehensive testing framework
- **Documentation**: Created detailed documentation with architecture diagrams
- **Code Quality**: Maintained high code quality with proper typing and linting

## Issues Encountered and Resolutions

### Technical Challenges
1. **Token Limits**: Encountered token limit issues when creating large package.json files
   - **Resolution**: Broke down large files into smaller, manageable chunks
   
2. **Path Mapping**: Complex TypeScript path mapping configuration
   - **Resolution**: Carefully configured Vite and TypeScript for proper module resolution
   
3. **Theme Integration**: Dark mode implementation with system preference detection
   - **Resolution**: Implemented comprehensive theme provider with localStorage persistence

### Process Improvements
1. **Task Management**: Improved task tracking and progress monitoring
   - **Resolution**: Enhanced to-do list with detailed progress tracking
   
2. **Documentation**: Ensured comprehensive documentation throughout development
   - **Resolution**: Created detailed README, CHANGELOG, and architecture documentation

## Lessons Learned

### Technical Insights
- **Modular Design**: Breaking down complex systems into specialized agents improves maintainability
- **Configuration First**: Establishing robust configuration management early prevents technical debt
- **Observability**: Implementing monitoring from the start provides valuable insights
- **Testing Strategy**: Multi-level testing approach ensures quality at all levels

### Process Insights
- **Incremental Development**: Building in phases allows for better quality control
- **Documentation**: Maintaining documentation alongside development improves project clarity
- **Tool Integration**: Comprehensive tooling improves developer experience significantly

## Next Steps

### Immediate Actions
1. **Phase 4 Implementation**: Begin agent workflow and orchestration implementation
2. **Model Integration**: Integrate with actual AI models for agent functionality
3. **Testing**: Implement comprehensive test suites for all components
4. **Documentation**: Complete API documentation and deployment guides

### Short-term Goals
1. **Agent Orchestration**: Implement the complete agent workflow system
2. **Real-time Updates**: Add WebSocket/SSE for real-time status updates
3. **Git Integration**: Implement granular Git operations and commit management
4. **Cost Tracking**: Add budget and cost tracking functionality

### Long-term Vision
1. **Production Deployment**: Prepare for production deployment with monitoring
2. **Performance Optimization**: Optimize for high performance and scalability
3. **Feature Expansion**: Add advanced features like conversation summarization
4. **Community Building**: Establish contribution guidelines and community engagement

## Critical Information for Future Reference

### Architecture Decisions
- Multi-agent system with specialized roles
- Monorepo structure for coordinated development
- OpenTelemetry for comprehensive observability
- PostgreSQL for persistent data storage
- React + TypeScript for modern frontend

### Key Dependencies
- Python 3.11+ for backend
- Node.js 18+ for frontend
- PostgreSQL for database
- Redis for caching
- Docker for containerization

### Configuration Requirements
- OpenRouter API key for AI model access
- Database connection strings
- Environment-specific configuration
- Security settings and CORS configuration

This session established a solid foundation for the AI Coder Agent system with comprehensive architecture, robust tooling, and modern development practices."""
    
    def _extract_key_points(self, summary: str) -> List[str]:
        """Extract key points from the summary."""
        # Simple heuristic to extract key points
        key_points = []
        lines = summary.split('\n')
        for line in lines:
            if line.strip().startswith('- ') or line.strip().startswith('• '):
                key_points.append(line.strip()[2:])
        return key_points[:10]  # Limit to 10 key points