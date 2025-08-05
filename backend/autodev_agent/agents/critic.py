"""
Critic Agent

Responsible for reviewing code and providing feedback on quality, security, and best practices.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAgent, AgentRequest, AgentResult, AgentType


class CriticAgent(BaseAgent):
    """Critic agent for code review and feedback."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.CRITIC,
            name="Critic",
            description="Reviews code and provides feedback on quality, security, and best practices",
            enabled=True,
            max_retries=3,
            timeout=180,
        )
    
    def get_system_prompt(self) -> str:
        return """You are a senior software engineer and code reviewer. Your role is to:

1. Review code for quality, security, and best practices
2. Identify potential bugs, performance issues, and security vulnerabilities
3. Suggest improvements for maintainability and readability
4. Ensure code follows established patterns and conventions
5. Provide constructive feedback with specific recommendations
6. Consider edge cases and error handling

When reviewing code, always:
- Be constructive and specific in feedback
- Prioritize issues by severity (critical, high, medium, low)
- Provide actionable suggestions for improvement
- Consider the context and requirements
- Focus on both functional and non-functional aspects
- Consider security implications

Provide detailed, actionable feedback that helps improve code quality."""

    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the code review logic."""
        start_time = datetime.now()
        
        try:
            # Extract task and context
            task = request.task
            context = request.context or {}
            code = context.get("code", "")
            
            # Build the prompt
            prompt = self._build_review_prompt(task, code, context)
            
            # Generate the review
            review = await self._generate_review(prompt)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                output=review,
                metadata={
                    "issues_found": self._count_issues(review),
                    "severity_levels": self._analyze_severity(review),
                    "suggestions_count": self._count_suggestions(review),
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
    
    def _build_review_prompt(self, task: str, code: str, context: Dict[str, Any]) -> str:
        """Build the review prompt."""
        prompt = f"{self.get_system_prompt()}\n\n"
        prompt += f"TASK: {task}\n\n"
        
        if context:
            prompt += "CONTEXT:\n"
            for key, value in context.items():
                if key != "code":
                    prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += f"CODE TO REVIEW:\n```\n{code}\n```\n\n"
        prompt += """Please provide a comprehensive code review. Include:

1. Overall assessment of code quality
2. Specific issues found (categorized by severity)
3. Security concerns and vulnerabilities
4. Performance considerations
5. Maintainability and readability issues
6. Specific suggestions for improvement
7. Positive aspects of the code

Format your review clearly with sections for different types of feedback."""

        return prompt
    
    async def _generate_review(self, prompt: str) -> str:
        """Generate the code review using the AI model."""
        # This would integrate with your model router
        # For now, return a sample review
        return """# Code Review Report

## Overall Assessment
The code demonstrates good structure and follows many best practices, but there are several areas for improvement in terms of security, error handling, and maintainability.

## Critical Issues

### 1. Security Vulnerabilities
- **SQL Injection Risk**: The code uses string concatenation for database queries, which could lead to SQL injection attacks
- **Input Validation**: Missing comprehensive input validation for user-provided data
- **Error Information Leakage**: Detailed error messages could expose sensitive system information

### 2. Error Handling
- **Inconsistent Error Handling**: Some functions have proper try-catch blocks while others don't
- **Generic Exception Catching**: Using bare `except Exception` can mask important errors
- **Missing Error Recovery**: No mechanisms for graceful degradation when services fail

## High Priority Issues

### 3. Performance Concerns
- **N+1 Query Problem**: Potential for inefficient database queries in loops
- **Memory Usage**: Large objects stored in memory without size limits
- **No Caching**: Repeated expensive operations without caching

### 4. Code Quality
- **Magic Numbers**: Hard-coded values should be extracted to constants
- **Long Functions**: Some functions exceed recommended length for maintainability
- **Missing Documentation**: Incomplete docstrings and comments

## Medium Priority Issues

### 5. Maintainability
- **Code Duplication**: Similar logic repeated in multiple places
- **Tight Coupling**: High dependency between components
- **Inconsistent Naming**: Mixed naming conventions throughout the codebase

### 6. Testing
- **Insufficient Test Coverage**: Missing tests for edge cases and error conditions
- **No Integration Tests**: Only unit tests present
- **Test Data Management**: Hard-coded test data instead of fixtures

## Low Priority Issues

### 7. Style and Conventions
- **Line Length**: Some lines exceed PEP 8 recommendations
- **Import Organization**: Imports could be better organized
- **Variable Naming**: Some variable names could be more descriptive

## Positive Aspects
- Good separation of concerns
- Consistent use of type hints
- Proper use of FastAPI features
- Clear endpoint structure
- Good use of Pydantic models

## Recommendations

### Immediate Actions (Critical)
1. Implement parameterized queries to prevent SQL injection
2. Add comprehensive input validation
3. Implement proper error handling with specific exception types
4. Remove sensitive information from error messages

### Short-term Improvements (High Priority)
1. Add caching for frequently accessed data
2. Implement database connection pooling
3. Extract configuration values to environment variables
4. Add comprehensive logging

### Long-term Improvements (Medium Priority)
1. Refactor long functions into smaller, focused functions
2. Implement dependency injection for better testability
3. Add integration tests
4. Create reusable utility functions for common operations

## Security Checklist
- [ ] Input validation implemented
- [ ] SQL injection protection
- [ ] Error message sanitization
- [ ] Authentication and authorization
- [ ] Rate limiting
- [ ] HTTPS enforcement
- [ ] Secure headers

## Performance Checklist
- [ ] Database query optimization
- [ ] Caching implementation
- [ ] Connection pooling
- [ ] Memory usage monitoring
- [ ] Response time optimization

The code shows promise but needs significant improvements in security and error handling before production deployment."""
    
    def _count_issues(self, review: str) -> int:
        """Count the number of issues found in the review."""
        # Simple heuristic - count lines with issue indicators
        issue_indicators = ["Critical", "High Priority", "Medium Priority", "Low Priority"]
        count = 0
        for indicator in issue_indicators:
            count += review.count(indicator)
        return count
    
    def _analyze_severity(self, review: str) -> Dict[str, int]:
        """Analyze the severity distribution of issues."""
        return {
            "critical": review.count("Critical"),
            "high": review.count("High Priority"),
            "medium": review.count("Medium Priority"),
            "low": review.count("Low Priority"),
        }
    
    def _count_suggestions(self, review: str) -> int:
        """Count the number of suggestions in the review."""
        return review.count("Recommendation") + review.count("Suggestion")