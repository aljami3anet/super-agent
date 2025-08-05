# AI Coder Agent System

[![CI](https://github.com/your-org/ai-coder-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/ai-coder-agent/actions/workflows/ci.yml)
[![Security](https://github.com/your-org/ai-coder-agent/actions/workflows/security.yml/badge.svg)](https://github.com/your-org/ai-coder-agent/actions/workflows/security.yml)
[![Coverage](https://codecov.io/gh/your-org/ai-coder-agent/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/ai-coder-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18](https://img.shields.io/badge/node.js-18-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-blue.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-blue.svg)](https://www.typescriptlang.org/)

A comprehensive AI-powered coding system with multi-agent orchestration, featuring autonomous code generation, testing, and deployment capabilities.

## 🚀 Features

- **Multi-Agent Architecture**: Planner, Coder, Critic, Tester, and Summarizer agents
- **Autonomous Workflows**: Complete development cycles from planning to deployment
- **Real-time Collaboration**: WebSocket-based live updates and streaming
- **Intelligent Code Generation**: Context-aware code creation with best practices
- **Automated Testing**: Comprehensive test generation and execution
- **Security-First**: Built-in vulnerability scanning and security checks
- **Observability**: Full OpenTelemetry integration with metrics, logs, and traces
- **Modern UI**: React + TypeScript + Tailwind CSS with dark mode support

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Frontend (React + TypeScript)"
        UI[User Interface]
        WS[WebSocket Client]
        API[API Client]
    end
    
    subgraph "Backend (FastAPI + Python)"
        API_GW[API Gateway]
        AUTH[Authentication]
        RATE[Rate Limiting]
        
        subgraph "Agent Orchestrator"
            PLANNER[Planner Agent]
            CODER[Coder Agent]
            CRITIC[Critic Agent]
            TESTER[Tester Agent]
            SUMMARIZER[Summarizer Agent]
        end
        
        subgraph "Tools & Services"
            TOOLS[Tool Functions]
            AI[AI Model Router]
            LOGS[Logging Service]
            DB[(PostgreSQL)]
        end
    end
    
    subgraph "Observability"
        OTEL[OpenTelemetry]
        PROM[Prometheus]
        GRAFANA[Grafana]
        JAEGER[Jaeger]
    end
    
    UI --> API_GW
    WS --> API_GW
    API --> API_GW
    API_GW --> AUTH
    API_GW --> RATE
    API_GW --> PLANNER
    PLANNER --> CODER
    CODER --> CRITIC
    CRITIC --> TESTER
    TESTER --> SUMMARIZER
    PLANNER --> TOOLS
    CODER --> TOOLS
    CRITIC --> TOOLS
    TESTER --> TOOLS
    SUMMARIZER --> TOOLS
    TOOLS --> AI
    TOOLS --> DB
    API_GW --> OTEL
    OTEL --> PROM
    OTEL --> GRAFANA
    OTEL --> JAEGER
```

## 🛠️ Technology Stack

### Backend
- **Python 3.11** - Core runtime
- **FastAPI** - High-performance web framework
- **OpenTelemetry** - Observability and tracing
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **Pydantic** - Data validation and settings
- **SQLAlchemy** - Database ORM
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Zustand** - Client state management
- **Framer Motion** - Animations

### DevOps & Quality
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Pytest** - Backend testing
- **Jest** - Frontend testing
- **Playwright** - E2E testing
- **Ruff** - Python linting
- **ESLint** - JavaScript linting
- **Pre-commit** - Git hooks

## 📦 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ai-coder-agent.git
   cd ai-coder-agent
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Or run locally**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   uvicorn autodev_agent.main:app --reload
   
   # Frontend
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

```bash
# Application
APP_NAME=AI Coder Agent
APP_VERSION=0.1.0
APP_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_coder_agent

# AI Models
OPENROUTER_API_KEY=your-api-key
OPENROUTER_MODELS=gpt-4,gpt-3.5-turbo,claude-3
PRIMARY_MODEL=gpt-4
FALLBACK_MODEL=gpt-3.5-turbo

# Observability
OTEL_ENDPOINT=http://localhost:4317
PROMETHEUS_PORT=9090

# Security
RATE_LIMIT_PER_MINUTE=100
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

### Agent Configuration

```yaml
agents:
  planner:
    enabled: true
    timeout: 300
    max_retries: 3
  
  coder:
    enabled: true
    timeout: 600
    max_retries: 3
  
  critic:
    enabled: true
    timeout: 300
    max_retries: 3
  
  tester:
    enabled: true
    timeout: 600
    max_retries: 3
  
  summarizer:
    enabled: true
    timeout: 300
    max_retries: 3
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest --cov=autodev_agent --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run test:coverage
npm run test:e2e
```

### All Tests
```bash
# Run all tests with coverage
make test
```

## 📊 Monitoring & Observability

### Metrics
- Application metrics via Prometheus
- Custom business metrics
- Performance indicators

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized log aggregation

### Tracing
- Distributed tracing with Jaeger
- Request flow visualization
- Performance bottleneck identification

### Dashboards
- Grafana dashboards for monitoring
- Real-time system health
- Custom alerting rules

## 🔒 Security

### Security Features
- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Rate Limiting**: API rate limiting
- **Input Validation**: Comprehensive input sanitization
- **CORS**: Cross-origin resource sharing
- **HTTPS**: TLS encryption
- **Secrets Management**: Secure environment variable handling

### Security Scanning
- **SAST**: Static application security testing
- **Dependency Scanning**: Automated vulnerability detection
- **Container Scanning**: Docker image security analysis
- **Secret Scanning**: Credential detection

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

### Cloud Deployment
- **AWS**: ECS/EKS deployment
- **GCP**: GKE deployment
- **Azure**: AKS deployment

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## 📚 API Documentation

### REST API
- **Base URL**: `http://localhost:8000/api/v1`
- **OpenAPI Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### WebSocket API
- **Logs Stream**: `ws://localhost:8000/ws/logs`
- **Real-time Updates**: `ws://localhost:8000/ws/updates`

### Key Endpoints

#### Agents
```http
GET    /api/v1/agents
GET    /api/v1/agents/{agent_type}
POST   /api/v1/agents/{agent_type}/execute
POST   /api/v1/agents/{agent_type}/enable
POST   /api/v1/agents/{agent_type}/disable
```

#### Workflows
```http
POST   /api/v1/workflows/execute
GET    /api/v1/workflows
GET    /api/v1/workflows/{workflow_id}
```

#### Tools
```http
GET    /api/v1/tools
POST   /api/v1/tools/{tool_name}/execute
```

#### Conversations
```http
GET    /api/v1/conversations
POST   /api/v1/conversations
GET    /api/v1/conversations/{conversation_id}
POST   /api/v1/conversations/{conversation_id}/messages
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

### Code Style
- **Python**: Black, Ruff, MyPy
- **TypeScript**: ESLint, Prettier
- **Commit Messages**: Conventional Commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/ai-coder-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-coder-agent/discussions)
- **Security**: [SECURITY.md](SECURITY.md)

### Community
- **Discord**: [Join our Discord](https://discord.gg/ai-coder-agent)
- **Twitter**: [@ai_coder_agent](https://twitter.com/ai_coder_agent)
- **Blog**: [Medium](https://medium.com/ai-coder-agent)

## 🗺️ Roadmap

### v1.0.0 (Current)
- ✅ Multi-agent architecture
- ✅ Real-time collaboration
- ✅ Comprehensive testing
- ✅ Security scanning
- ✅ Observability

### v1.1.0 (Planned)
- 🔄 Advanced code generation
- 🔄 Multi-language support
- 🔄 Team collaboration features
- 🔄 Advanced analytics

### v2.0.0 (Future)
- 🔮 AI model fine-tuning
- 🔮 Custom agent development
- 🔮 Enterprise features
- 🔮 Cloud-native deployment

## 🙏 Acknowledgments

- **FastAPI** team for the excellent web framework
- **React** team for the amazing UI library
- **OpenTelemetry** community for observability tools
- **Tailwind CSS** for the utility-first CSS framework
- All contributors and users of this project

---

**Made with ❤️ by the AI Coder Agent Team**

[![GitHub stars](https://img.shields.io/github/stars/your-org/ai-coder-agent)](https://github.com/your-org/ai-coder-agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/your-org/ai-coder-agent)](https://github.com/your-org/ai-coder-agent/network)
[![GitHub issues](https://img.shields.io/github/issues/your-org/ai-coder-agent)](https://github.com/your-org/ai-coder-agent/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/your-org/ai-coder-agent)](https://github.com/your-org/ai-coder-agent/pulls)
