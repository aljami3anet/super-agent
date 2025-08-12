**Short answer:**  
It’s a **syntax** problem, not a logical one. The way the sub‑graphs are declared (`subgraph "Frontend (React + TypeScript + Tailwind)"`) works in the latest online editor, but GitHub’s built‑in Mermaid version still expects the older *“id + optional title”* form. Because the quoted string is interpreted as the **sub‑graph ID**, which may not contain spaces or special characters, GitHub fails to parse the diagram and either shows an empty box or an error.

Below is a minimal, drop‑in replacement that renders correctly on GitHub. The only changes are:

1. **Give each sub‑graph a plain identifier** (letters, numbers, underscores).  
2. **Add the human‑readable title in square brackets** after the identifier.  
3. (Optional) rename a few node IDs to avoid confusion with the sub‑graph IDs – this isn’t required but makes the diagram easier to read.

```mermaid
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
```

### Why this works

| What you had | Why it fails on GitHub | What the fix does |
|--------------|-----------------------|-------------------|
| `subgraph "Frontend (React + TypeScript + Tailwind)"` | The quoted string is taken as the **sub‑graph ID**. IDs may not contain spaces, parentheses, “+”, etc., so the parser aborts. | `subgraph FRONTEND["Frontend (React + TypeScript + Tailwind)"]` – `FRONTEND` is a legal ID, the text in brackets is shown as the title. |
| Similar quoted titles for the other sub‑graphs | Same issue for each block. | Each block now follows `subgraph <ID>["<Title>"]`. |
| Node ID `AGENTS` lives inside the *Backend* sub‑graph while you also use the word “Agents” as a sub‑graph name | No direct error, but it makes the diagram harder to read because the ID clashes with a cluster concept. | Renamed the orchestrator node to `ORCH` (or any other legal identifier). |

### Quick checklist for future Mermaid diagrams on GitHub

1. **Sub‑graphs** – `subgraph ID["Title"] … end`. The `ID` must be a simple token (letters, digits, `_`).  
2. **Node IDs** – Must be unique across the whole diagram; they can be anything that matches the same rule as IDs.  
3. **Shape shortcuts** – `[(text)]` for a cylinder (database), `[text]` for a rectangle, `(text)` for a circle, `{text}` for a diamond, `((text))` for a sub‑routine. All of these are supported by GitHub’s Mermaid version.  
4. **Edge definitions** – You can declare edges before or after the target nodes; both are fine.  
5. **Markdown wrapper** – Use triple back‑ticks with the literal `mermaid` language (` ```mermaid `). No extra HTML or `<script>` tags are needed.  

### Optional niceties (purely visual)

If you want each cluster to have a distinct background colour, you can add a tiny style block at the top of the diagram:

```mermaid
%%{init: {"theme":"neutral","themeVariables":{"primaryColor":"#0d6efd","secondaryColor":"#6c757d"}}}%%
```

Or you can use `classDef`/`class` statements after the graph to colour individual nodes or clusters.

---

**Bottom line:** Switch to the `subgraph ID["Title"]` form, keep IDs simple, and the diagram will render perfectly on GitHub. If you still see issues, open the file in the **GitHub “Raw” view** and click the **“Open in Mermaid Live Editor”** link that appears under the diagram – it will show you the exact parsing error GitHub is hitting. Feel free to drop the updated code back here if anything still looks off!
