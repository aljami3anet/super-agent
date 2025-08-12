graph TB
    %% ── Sub‑graphs (id + title) ─────────────────────────────
    subgraph FRONTEND["Frontend (React + TypeScript + Tailwind)"]
        UI[User Interface]
        WS[WebSocket Client]
        THEME[Theme Provider]
    end

    subgraph BACKEND["Backend (Python 3.11 + FastAPI)"]
        API[FastAPI Server]
        ORCH[Agent Orchestrator]          %% renamed from AGENTS
        TOOLS[Tool Functions]
        DB[(PostgreSQL)]                  %% cylinder shape for a DB
        REDIS[(Redis)]                    %% cylinder shape for Redis
    end

    subgraph AGENT_CLUSTER["Agents"]
        PLANNER[Planner Agent]
        CODER[Coder Agent]
        CRITIC[Critic Agent]
        TESTER[Tester Agent]
        SUMMARIZER[Summarizer Agent]
    end

    subgraph OBSERV["Observability"]
        OTEL[OpenTelemetry Collector]
        PROM[Prometheus]
        GRAFANA[Grafana]
        JAEGER[Jaeger]
    end

    subgraph EXT_SERVICES["External Services"]
        OPENROUTER[OpenRouter API]
        GITHUB[GitHub]
    end

    %% ── Connections ───────────────────────────────────────────────
    UI --> WS
    WS --> API
    THEME --> UI

    API --> ORCH
    ORCH --> PLANNER
    ORCH --> CODER
    ORCH --> CRITIC
    ORCH --> TESTER
    ORCH --> SUMMARIZER
    ORCH --> TOOLS
    TOOLS --> DB
    TOOLS --> REDIS
    TOOLS --> GITHUB
    ORCH --> OPENROUTER

    API --> OTEL
    OTEL --> PROM
    OTEL --> JAEGER
    PROM --> GRAFANA
