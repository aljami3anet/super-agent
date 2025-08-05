"""
Tests for the agent system.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from autodev_agent.agents.base import (
    BaseAgent, AgentRequest, AgentResult, AgentType, AgentStatus
)
from autodev_agent.agents.planner import PlannerAgent
from autodev_agent.agents.coder import CoderAgent
from autodev_agent.agents.critic import CriticAgent
from autodev_agent.agents.tester import TesterAgent
from autodev_agent.agents.summarizer import SummarizerAgent
from autodev_agent.agents.orchestrator import AgentOrchestrator


class TestBaseAgent:
    """Test the base agent functionality."""
    
    def test_agent_initialization(self):
        """Test that agents are initialized correctly."""
        # Create a concrete agent for testing
        agent = PlannerAgent()
        
        assert agent.agent_type == AgentType.PLANNER
        assert agent.name == "Planner"
        assert agent.enabled is True
        assert agent.status == AgentStatus.IDLE
        assert agent.current_task is None
        assert agent.execution_count == 0
    
    def test_agent_stats(self):
        """Test agent statistics tracking."""
        agent = PlannerAgent()
        
        stats = agent.get_stats()
        
        assert "agent_type" in stats
        assert "name" in stats
        assert "enabled" in stats
        assert "status" in stats
        assert "execution_count" in stats
        assert "success_count" in stats
        assert "failure_count" in stats
        assert "success_rate" in stats
    
    def test_agent_enable_disable(self):
        """Test agent enable/disable functionality."""
        agent = PlannerAgent()
        
        # Test disable
        agent.disable()
        assert agent.enabled is False
        assert agent.status == AgentStatus.DISABLED
        assert agent.current_task is None
        
        # Test enable
        agent.enable()
        assert agent.enabled is True
        assert agent.status == AgentStatus.IDLE
    
    def test_agent_reset_stats(self):
        """Test agent statistics reset."""
        agent = PlannerAgent()
        
        # Simulate some executions
        agent.execution_count = 5
        agent.success_count = 3
        agent.failure_count = 2
        agent.total_execution_time = 10.5
        agent.total_tokens_used = 1000
        agent.total_cost = 5.25
        
        agent.reset_stats()
        
        assert agent.execution_count == 0
        assert agent.success_count == 0
        assert agent.failure_count == 0
        assert agent.total_execution_time == 0.0
        assert agent.total_tokens_used == 0
        assert agent.total_cost == 0.0
        assert agent.last_execution is None
        assert agent.status == AgentStatus.IDLE


class TestAgentRequest:
    """Test the AgentRequest model."""
    
    def test_agent_request_creation(self):
        """Test creating an AgentRequest."""
        request = AgentRequest(
            task="Test task",
            context={"key": "value"},
            parameters={"param": "value"},
            conversation_id="conv-123",
            user_id="user-456"
        )
        
        assert request.task == "Test task"
        assert request.context == {"key": "value"}
        assert request.parameters == {"param": "value"}
        assert request.conversation_id == "conv-123"
        assert request.user_id == "user-456"
    
    def test_agent_request_defaults(self):
        """Test AgentRequest with default values."""
        request = AgentRequest(task="Test task")
        
        assert request.task == "Test task"
        assert request.context is None
        assert request.parameters is None
        assert request.conversation_id is None
        assert request.user_id is None


class TestAgentResult:
    """Test the AgentResult dataclass."""
    
    def test_agent_result_creation(self):
        """Test creating an AgentResult."""
        result = AgentResult(
            success=True,
            output="Test output",
            metadata={"key": "value"},
            error=None,
            execution_time=1.5,
            tokens_used=100,
            cost=0.05
        )
        
        assert result.success is True
        assert result.output == "Test output"
        assert result.metadata == {"key": "value"}
        assert result.error is None
        assert result.execution_time == 1.5
        assert result.tokens_used == 100
        assert result.cost == 0.05
    
    def test_agent_result_defaults(self):
        """Test AgentResult with default values."""
        result = AgentResult(success=False, output="")
        
        assert result.success is False
        assert result.output == ""
        assert result.metadata == {}
        assert result.error is None
        assert result.execution_time == 0.0
        assert result.tokens_used == 0
        assert result.cost == 0.0


class TestPlannerAgent:
    """Test the Planner agent."""
    
    @pytest.mark.asyncio
    async def test_planner_execute(self):
        """Test planner agent execution."""
        agent = PlannerAgent()
        request = AgentRequest(task="Create a simple API")
        
        result = await agent.execute(request)
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert len(result.output) > 0
        assert result.execution_time > 0
    
    def test_planner_system_prompt(self):
        """Test planner system prompt."""
        agent = PlannerAgent()
        prompt = agent.get_system_prompt()
        
        assert "strategic planning" in prompt.lower()
        assert "task breakdown" in prompt.lower()
        assert "execution strategies" in prompt.lower()


class TestCoderAgent:
    """Test the Coder agent."""
    
    @pytest.mark.asyncio
    async def test_coder_execute(self):
        """Test coder agent execution."""
        agent = CoderAgent()
        request = AgentRequest(
            task="Create a FastAPI endpoint",
            context={"language": "python", "framework": "fastapi"}
        )
        
        result = await agent.execute(request)
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert len(result.output) > 0
        assert result.execution_time > 0
    
    def test_coder_system_prompt(self):
        """Test coder system prompt."""
        agent = CoderAgent()
        prompt = agent.get_system_prompt()
        
        assert "software developer" in prompt.lower()
        assert "code generation" in prompt.lower()
        assert "best practices" in prompt.lower()


class TestCriticAgent:
    """Test the Critic agent."""
    
    @pytest.mark.asyncio
    async def test_critic_execute(self):
        """Test critic agent execution."""
        agent = CriticAgent()
        request = AgentRequest(
            task="Review this code",
            context={"code": "def hello(): return 'Hello, World!'"}
        )
        
        result = await agent.execute(request)
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert len(result.output) > 0
        assert result.execution_time > 0
    
    def test_critic_system_prompt(self):
        """Test critic system prompt."""
        agent = CriticAgent()
        prompt = agent.get_system_prompt()
        
        assert "code reviewer" in prompt.lower()
        assert "quality" in prompt.lower()
        assert "security" in prompt.lower()


class TestTesterAgent:
    """Test the Tester agent."""
    
    @pytest.mark.asyncio
    async def test_tester_execute(self):
        """Test tester agent execution."""
        agent = TesterAgent()
        request = AgentRequest(
            task="Create tests for this code",
            context={"code": "def add(a, b): return a + b"}
        )
        
        result = await agent.execute(request)
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert len(result.output) > 0
        assert result.execution_time > 0
    
    def test_tester_system_prompt(self):
        """Test tester system prompt."""
        agent = TesterAgent()
        prompt = agent.get_system_prompt()
        
        assert "qa engineer" in prompt.lower()
        assert "testing" in prompt.lower()
        assert "test coverage" in prompt.lower()


class TestSummarizerAgent:
    """Test the Summarizer agent."""
    
    @pytest.mark.asyncio
    async def test_summarizer_execute(self):
        """Test summarizer agent execution."""
        agent = SummarizerAgent()
        request = AgentRequest(
            task="Summarize this conversation",
            context={"content": "This is a long conversation that needs summarization."}
        )
        
        result = await agent.execute(request)
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert len(result.output) > 0
        assert result.execution_time > 0
    
    def test_summarizer_system_prompt(self):
        """Test summarizer system prompt."""
        agent = SummarizerAgent()
        prompt = agent.get_system_prompt()
        
        assert "summarization" in prompt.lower()
        assert "concise" in prompt.lower()
        assert "context" in prompt.lower()


class TestAgentOrchestrator:
    """Test the Agent Orchestrator."""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = AgentOrchestrator()
        
        assert len(orchestrator.agents) == 5
        assert AgentType.PLANNER in orchestrator.agents
        assert AgentType.CODER in orchestrator.agents
        assert AgentType.CRITIC in orchestrator.agents
        assert AgentType.TESTER in orchestrator.agents
        assert AgentType.SUMMARIZER in orchestrator.agents
    
    @pytest.mark.asyncio
    async def test_orchestrator_workflow_execution(self):
        """Test complete workflow execution."""
        orchestrator = AgentOrchestrator()
        
        result = await orchestrator.execute_workflow(
            task="Create a simple API endpoint",
            context={"language": "python", "framework": "fastapi"}
        )
        
        assert "workflow_id" in result
        assert "status" in result
        assert "steps" in result
        assert len(result["steps"]) == 5  # All 5 agents
    
    def test_orchestrator_agent_status(self):
        """Test getting agent status."""
        orchestrator = AgentOrchestrator()
        
        status = orchestrator.get_agent_status()
        
        assert "planner" in status
        assert "coder" in status
        assert "critic" in status
        assert "tester" in status
        assert "summarizer" in status
        
        for agent_status in status.values():
            assert "name" in agent_status
            assert "enabled" in agent_status
            assert "status" in agent_status
            assert "stats" in agent_status
    
    def test_orchestrator_statistics(self):
        """Test orchestrator statistics."""
        orchestrator = AgentOrchestrator()
        
        stats = orchestrator.get_statistics()
        
        assert "total_workflows" in stats
        assert "successful_workflows" in stats
        assert "failed_workflows" in stats
        assert "success_rate" in stats
        assert "active_workflows" in stats
        assert "agent_status" in stats
    
    def test_orchestrator_agent_management(self):
        """Test agent enable/disable functionality."""
        orchestrator = AgentOrchestrator()
        
        # Test disable
        orchestrator.disable_agent(AgentType.PLANNER)
        planner = orchestrator.get_agent(AgentType.PLANNER)
        assert planner.enabled is False
        
        # Test enable
        orchestrator.enable_agent(AgentType.PLANNER)
        planner = orchestrator.get_agent(AgentType.PLANNER)
        assert planner.enabled is True
    
    def test_orchestrator_reset_statistics(self):
        """Test statistics reset."""
        orchestrator = AgentOrchestrator()
        
        # Simulate some workflows
        orchestrator.total_workflows = 10
        orchestrator.successful_workflows = 8
        orchestrator.failed_workflows = 2
        
        orchestrator.reset_statistics()
        
        assert orchestrator.total_workflows == 0
        assert orchestrator.successful_workflows == 0
        assert orchestrator.failed_workflows == 0
        assert len(orchestrator.workflow_history) == 0
        assert len(orchestrator.active_workflows) == 0
    
    def test_orchestrator_workflow_history(self):
        """Test workflow history management."""
        orchestrator = AgentOrchestrator()
        
        # Add some mock workflows
        orchestrator.workflow_history = [
            {"id": "wf-1", "status": "completed"},
            {"id": "wf-2", "status": "failed"},
            {"id": "wf-3", "status": "completed"},
        ]
        
        history = orchestrator.get_workflow_history(limit=2)
        assert len(history) == 2
        assert history[-1]["id"] == "wf-3"
    
    def test_orchestrator_workflow_status(self):
        """Test getting workflow status."""
        orchestrator = AgentOrchestrator()
        
        # Add a mock workflow
        workflow = {"id": "test-wf", "status": "running"}
        orchestrator.active_workflows["test-wf"] = workflow
        
        status = orchestrator.get_workflow_status("test-wf")
        assert status == workflow
        
        # Test non-existent workflow
        status = orchestrator.get_workflow_status("non-existent")
        assert status is None


class TestAgentErrorHandling:
    """Test agent error handling."""
    
    @pytest.mark.asyncio
    async def test_agent_timeout_handling(self):
        """Test agent timeout handling."""
        agent = PlannerAgent()
        agent.timeout = 0.1  # Very short timeout
        
        request = AgentRequest(task="This will timeout")
        
        # Mock the execute method to sleep longer than timeout
        async def slow_execute(request):
            await asyncio.sleep(1)
            return AgentResult(success=True, output="")
        
        agent.execute = slow_execute
        
        result = await agent.run(request)
        
        assert result.success is False
        assert "timeout" in result.error.lower()
    
    @pytest.mark.asyncio
    async def test_agent_retry_logic(self):
        """Test agent retry logic."""
        agent = PlannerAgent()
        agent.max_retries = 3
        
        request = AgentRequest(task="Test retry")
        
        # Mock execute to fail twice then succeed
        call_count = 0
        async def failing_execute(request):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return AgentResult(success=True, output="Success")
        
        agent.execute = failing_execute
        
        result = await agent.run(request)
        
        assert result.success is True
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_disabled_agent_execution(self):
        """Test that disabled agents don't execute."""
        agent = PlannerAgent()
        agent.disable()
        
        request = AgentRequest(task="Test disabled agent")
        
        result = await agent.run(request)
        
        assert result.success is False
        assert "disabled" in result.error.lower()
        assert agent.execution_count == 0  # Should not increment


class TestAgentIntegration:
    """Integration tests for agent interactions."""
    
    @pytest.mark.asyncio
    async def test_agent_workflow_integration(self):
        """Test that agents work together in a workflow."""
        orchestrator = AgentOrchestrator()
        
        # Mock all agents to return successful results
        for agent in orchestrator.agents.values():
            async def mock_execute(request):
                return AgentResult(
                    success=True,
                    output=f"Mock output from {agent.name}",
                    execution_time=0.1,
                    tokens_used=50,
                    cost=0.01
                )
            agent.execute = mock_execute
        
        result = await orchestrator.execute_workflow(
            task="Create a simple web application",
            context={"framework": "react", "backend": "nodejs"}
        )
        
        assert result["status"] == "completed"
        assert len(result["steps"]) == 5
        
        # Verify each step was executed
        for step in result["steps"]:
            assert step["status"] == "completed"
            assert step["result"]["success"] is True
    
    @pytest.mark.asyncio
    async def test_agent_context_passing(self):
        """Test that context is passed correctly between agents."""
        orchestrator = AgentOrchestrator()
        
        # Track context passed to each agent
        context_log = []
        
        for agent in orchestrator.agents.values():
            async def mock_execute(request):
                context_log.append({
                    "agent": agent.name,
                    "context": request.context
                })
                return AgentResult(
                    success=True,
                    output="Mock output",
                    execution_time=0.1
                )
            agent.execute = mock_execute
        
        initial_context = {"language": "python", "framework": "fastapi"}
        
        await orchestrator.execute_workflow(
            task="Test context passing",
            context=initial_context
        )
        
        # Verify context was passed to all agents
        assert len(context_log) == 5
        
        # Verify each agent received some context
        for log_entry in context_log:
            assert log_entry["context"] is not None