# Contributing to AI Coder Agent

Thank you for your interest in contributing to the AI Coder Agent project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Community](#community)

## Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment for our community include:

- Using welcoming and inclusive language
- Being respectful of differing opinions, viewpoints, and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- The use of sexualized language or imagery, and sexual attention or advances
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Violations of the Code of Conduct may be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Docker (optional but recommended)

### Fork and Clone

1. **Fork the repository**
   - Go to [https://github.com/your-org/ai-coder-agent](https://github.com/your-org/ai-coder-agent)
   - Click the "Fork" button in the top right

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-coder-agent.git
   cd ai-coder-agent
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/your-org/ai-coder-agent.git
   ```

## Development Setup

### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up pre-commit hooks**
   ```bash
   npx husky install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

### Database Setup

1. **Start PostgreSQL**
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=ai_coder_agent \
     -p 5432:5432 \
     postgres:15
   ```

2. **Run migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

## Contributing Guidelines

### Issue Reporting

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Use the issue template** and provide all requested information
3. **Include reproduction steps** for bugs
4. **Add screenshots** for UI issues
5. **Specify your environment** (OS, browser, etc.)

### Feature Requests

When requesting features:

1. **Describe the problem** you're trying to solve
2. **Explain why** this feature is needed
3. **Provide use cases** and examples
4. **Consider alternatives** and trade-offs
5. **Include mockups** if applicable

### Bug Reports

When reporting bugs:

1. **Use the bug report template**
2. **Provide minimal reproduction steps**
3. **Include error messages and stack traces**
4. **Specify the expected vs actual behavior**
5. **Add environment details**

### Pull Requests

#### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend && pytest
   
   # Frontend tests
   cd frontend && npm test
   
   # All tests
   make test
   ```

4. **Update documentation**
   - Update README.md if needed
   - Add docstrings for new functions
   - Update API documentation

#### PR Guidelines

1. **Use conventional commit messages**
   ```
   feat: add new agent type
   fix(auth): resolve login issue
   docs: update API documentation
   ```

2. **Keep PRs focused and small**
   - One feature/fix per PR
   - Keep changes under 500 lines when possible
   - Break large changes into multiple PRs

3. **Write descriptive PR descriptions**
   - Explain what the PR does
   - Link related issues
   - Include testing instructions
   - Add screenshots for UI changes

4. **Request reviews**
   - Tag relevant maintainers
   - Add appropriate labels
   - Respond to review comments promptly

## Code Style

### Python (Backend)

We use the following tools for Python code quality:

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **MyPy**: Type checking
- **isort**: Import sorting

#### Style Guidelines

1. **Follow PEP 8** with Black formatting
2. **Use type hints** for all function parameters and return values
3. **Write docstrings** for all public functions and classes
4. **Use meaningful variable names**
5. **Keep functions small and focused**

Example:
```python
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    """User model for authentication."""
    
    id: int
    username: str
    email: str
    is_active: bool = True


def get_user_by_id(user_id: int) -> Optional[User]:
    """Retrieve a user by their ID.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        User object if found, None otherwise
    """
    # Implementation here
    pass
```

### TypeScript/JavaScript (Frontend)

We use the following tools for frontend code quality:

- **ESLint**: Linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking

#### Style Guidelines

1. **Use TypeScript** for all new code
2. **Follow ESLint rules** strictly
3. **Use meaningful component and function names**
4. **Write JSDoc comments** for complex functions
5. **Use React hooks** appropriately

Example:
```typescript
import React, { useState, useEffect } from 'react';

interface User {
  id: number;
  username: string;
  email: string;
  isActive: boolean;
}

interface UserListProps {
  /** Callback when a user is selected */
  onUserSelect: (user: User) => void;
  /** List of users to display */
  users: User[];
}

/**
 * Displays a list of users with selection functionality
 */
export const UserList: React.FC<UserListProps> = ({ 
  onUserSelect, 
  users 
}) => {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  useEffect(() => {
    if (selectedUser) {
      onUserSelect(selectedUser);
    }
  }, [selectedUser, onUserSelect]);

  return (
    <div className="user-list">
      {users.map((user) => (
        <div
          key={user.id}
          className={`user-item ${selectedUser?.id === user.id ? 'selected' : ''}`}
          onClick={() => setSelectedUser(user)}
        >
          <span>{user.username}</span>
          <span>{user.email}</span>
        </div>
      ))}
    </div>
  );
};
```

### Git Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat: add new planner agent type
fix(auth): resolve token expiration issue
docs: update API documentation
style: format code with black
refactor(agents): simplify orchestrator logic
test: add unit tests for critic agent
chore: update dependencies
```

## Testing

### Backend Testing

1. **Unit tests**
   ```bash
   cd backend
   pytest tests/unit/
   ```

2. **Integration tests**
   ```bash
   pytest tests/integration/
   ```

3. **All tests with coverage**
   ```bash
   pytest --cov=autodev_agent --cov-report=html
   ```

### Frontend Testing

1. **Unit tests**
   ```bash
   cd frontend
   npm test
   ```

2. **E2E tests**
   ```bash
   npm run test:e2e
   ```

3. **Coverage report**
   ```bash
   npm run test:coverage
   ```

### Test Guidelines

1. **Write tests for all new functionality**
2. **Use descriptive test names**
3. **Follow AAA pattern** (Arrange, Act, Assert)
4. **Mock external dependencies**
5. **Test edge cases and error conditions**

Example:
```python
import pytest
from unittest.mock import Mock, patch
from autodev_agent.agents.planner import PlannerAgent


class TestPlannerAgent:
    """Test the Planner agent functionality."""
    
    def test_planner_executes_successfully(self):
        """Test that planner agent executes without errors."""
        # Arrange
        agent = PlannerAgent()
        request = AgentRequest(task="Create a simple API")
        
        # Act
        result = await agent.execute(request)
        
        # Assert
        assert result.success is True
        assert len(result.output) > 0
        assert result.execution_time > 0
```

## Pull Request Process

### Review Process

1. **Automated checks** must pass
   - CI/CD pipeline
   - Code coverage
   - Security scans
   - Linting and formatting

2. **Code review** by maintainers
   - At least one approval required
   - Address all review comments
   - Update PR based on feedback

3. **Final checks**
   - All tests pass
   - Documentation updated
   - No merge conflicts

### Review Guidelines

#### For Contributors

1. **Respond promptly** to review comments
2. **Be open to feedback** and suggestions
3. **Explain your reasoning** when needed
4. **Make requested changes** or explain why not
5. **Thank reviewers** for their time

#### For Reviewers

1. **Be constructive** and respectful
2. **Focus on the code**, not the person
3. **Explain your reasoning** for suggestions
4. **Be specific** about what needs to change
5. **Approve promptly** when satisfied

### Merge Process

1. **Squash and merge** for feature branches
2. **Rebase and merge** for hotfixes
3. **Delete feature branches** after merge
4. **Update version** if needed
5. **Create release notes**

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Create release branch**
   ```bash
   git checkout -b release/v1.2.0
   ```

2. **Update version numbers**
   - `backend/autodev_agent/__init__.py`
   - `frontend/package.json`
   - `CHANGELOG.md`

3. **Update documentation**
   - README.md badges
   - API documentation
   - Deployment guides

4. **Create release notes**
   - List new features
   - Document breaking changes
   - Include migration guide if needed

5. **Tag and release**
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

6. **Deploy to production**
   - Run deployment pipeline
   - Verify deployment
   - Monitor for issues

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Changelog updated
- [ ] Release notes written
- [ ] Security scan passed
- [ ] Performance tests passed
- [ ] Deployment tested

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Discord**: Real-time chat and community
- **Email**: security@your-org.com for security issues

### Getting Help

1. **Check documentation** first
2. **Search existing issues** for similar problems
3. **Ask in Discussions** for general questions
4. **Create an issue** for bugs or feature requests
5. **Join Discord** for real-time help

### Recognition

We recognize contributors in several ways:

1. **Contributor hall of fame** in README.md
2. **Release notes** mention significant contributors
3. **GitHub stars** and badges
4. **Community shoutouts** in discussions

### Mentorship

We offer mentorship for new contributors:

1. **Good first issues** labeled for beginners
2. **Mentor assignments** for complex features
3. **Code review guidance** for new contributors
4. **Documentation** for common tasks

## Security

### Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. **Email** security@your-org.com
3. **Include** detailed reproduction steps
4. **Wait** for acknowledgment and response
5. **Follow** responsible disclosure guidelines

### Security Guidelines

1. **Never commit secrets** or sensitive data
2. **Use environment variables** for configuration
3. **Validate all inputs** thoroughly
4. **Follow OWASP guidelines** for web security
5. **Keep dependencies updated**

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

If you have questions about contributing:

1. **Check this document** first
2. **Search existing issues** for similar questions
3. **Ask in Discussions** for general questions
4. **Email** maintainers for specific concerns

Thank you for contributing to AI Coder Agent! 🚀