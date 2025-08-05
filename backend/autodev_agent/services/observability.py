import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler, set_logger_provider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPHTTPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as OTLPHTTPMetricExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as OTLPHTTPLogExporter
import os


def setup_otel(service_name: str = "ai-coder-agent", otlp_endpoint: str = None):
    otlp_endpoint = otlp_endpoint or os.getenv("OTEL_ENDPOINT", "http://localhost:4317")
    resource = Resource(attributes={SERVICE_NAME: service_name})

    # Tracing
    tracer_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Metrics
    metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Logging
    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint=otlp_endpoint, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)

    logging.info(f"OpenTelemetry initialized for {service_name} at {otlp_endpoint}")

# Example Grafana dashboard JSON (to be imported in Grafana UI)
GRAFANA_DASHBOARD_JSON = {
  "title": "AI Coder Agent - Overview",
  "panels": [
    {
      "type": "graph",
      "title": "Request Duration (ms)",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_server_duration_seconds_bucket{service=\"ai-coder-agent\"}[5m])) by (le)) * 1000",
          "legendFormat": "95th Percentile",
        }
      ],
      "datasource": "Prometheus",
      "yaxes": [
        {"format": "ms", "label": "Duration (ms)"},
        {"format": "short"}
      ]
    },
    {
      "type": "stat",
      "title": "Active Workflows",
      "targets": [
        {
          "expr": "ai_coder_agent_active_workflows",
          "legendFormat": "Active Workflows"
        }
      ],
      "datasource": "Prometheus"
    },
    {
      "type": "stat",
      "title": "Error Rate",
      "targets": [
        {
          "expr": "sum(rate(http_server_requests_seconds_count{status=\"5xx\",service=\"ai-coder-agent\"}[5m])) / sum(rate(http_server_requests_seconds_count{service=\"ai-coder-agent\"}[5m]))",
          "legendFormat": "Error Rate"
        }
      ],
      "datasource": "Prometheus"
    },
    {
      "type": "logs",
      "title": "Agent Logs",
      "targets": [
        {
          "expr": "{app=\"ai-coder-agent\"}"
        }
      ],
      "datasource": "Loki"
    }
  ],
  "schemaVersion": 36,
  "version": 1,
  "refresh": "10s"
}