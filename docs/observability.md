# Observability Guide

This document describes how to set up, monitor, and visualize observability for the AI Coder Agent system.

## Table of Contents
- [Overview](#overview)
- [OpenTelemetry Setup](#opentelemetry-setup)
- [Metrics](#metrics)
- [Logs](#logs)
- [Traces](#traces)
- [Prometheus Integration](#prometheus-integration)
- [Grafana Dashboards](#grafana-dashboards)
- [Jaeger Tracing](#jaeger-tracing)
- [Loki Log Aggregation](#loki-log-aggregation)
- [Alerting](#alerting)

## Overview

The system uses OpenTelemetry to export metrics, logs, and traces to an OTLP-compatible backend. Prometheus, Grafana, Jaeger, and Loki are recommended for monitoring, visualization, and log aggregation.

## OpenTelemetry Setup

- **Backend**: Exports traces, metrics, and logs to OTLP endpoint (default: `http://localhost:4317`)
- **Configuration**: Set `OTEL_ENDPOINT` in `.env` or environment
- **Initialization**: See `autodev_agent/services/observability.py`

## Metrics

- **Request duration**: Histogram of HTTP request durations
- **Active workflows**: Gauge of currently running workflows
- **Error rate**: Counter of 5xx responses
- **Custom business metrics**: Agent execution counts, success/failure rates

### Example Prometheus Query
```
histogram_quantile(0.95, sum(rate(http_server_duration_seconds_bucket{service="ai-coder-agent"}[5m])) by (le)) * 1000
```

## Logs

- **Structured JSON logs**: All logs are structured and can be exported to Loki or other log aggregation systems
- **Log levels**: DEBUG, INFO, WARNING, ERROR
- **Log context**: Includes request ID, agent type, workflow ID, etc.

## Traces

- **Distributed tracing**: All requests and agent executions are traced
- **Trace context**: Propagated across HTTP and WebSocket boundaries
- **Jaeger**: Visualize traces and identify bottlenecks

## Prometheus Integration

- **Scrape endpoint**: `/metrics` (exposed by FastAPI/OpenTelemetry)
- **Prometheus config**:
```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'ai-coder-agent-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

## Grafana Dashboards

- **Import dashboard**: Use the provided JSON in `autodev_agent/services/observability.py` (`GRAFANA_DASHBOARD_JSON`)
- **Panels**:
  - Request duration (95th percentile)
  - Active workflows
  - Error rate
  - Agent logs (via Loki)
- **Datasource**: Prometheus (metrics), Loki (logs)

## Jaeger Tracing

- **Jaeger UI**: http://localhost:16686
- **Search for service**: `ai-coder-agent`
- **Trace visualization**: End-to-end request and agent execution

## Loki Log Aggregation

- **Loki UI**: http://localhost:3100
- **Query logs**: `{app="ai-coder-agent"}`
- **Log search**: Filter by agent, workflow, or error

## Alerting

- **Prometheus alert rules**: See `alerting-rules.yml` in deployment guide
- **Common alerts**:
  - High error rate
  - High request duration
  - Database connection pool nearly full
- **Grafana alerts**: Configure in dashboard for real-time notifications

---

For more details, see the [Deployment Guide](DEPLOYMENT_GUIDE.md) and [Architecture Documentation](architecture.md).