# Deployment Guide

This guide covers various deployment options for the AI Coder Agent System, from local development to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)
- [Monitoring & Observability](#monitoring--observability)
- [Security Hardening](#security-hardening)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **CPU**: 4+ cores (8+ recommended for production)
- **RAM**: 8GB+ (16GB+ recommended for production)
- **Storage**: 50GB+ SSD
- **Network**: Stable internet connection for AI model access

### Software Requirements

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.11+
- **Node.js**: 18+
- **PostgreSQL**: 15+
- **Redis**: 7.0+

## Local Development

### Quick Start

1. **Clone and setup**
   ```bash
   git clone https://github.com/your-org/ai-coder-agent.git
   cd ai-coder-agent
   cp .env.example .env
   ```

2. **Configure environment**
   ```bash
   # Edit .env file with your settings
   nano .env
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup

1. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database setup**
   ```bash
   # Start PostgreSQL
   docker run -d --name postgres \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=ai_coder_agent \
     -p 5432:5432 \
     postgres:15
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Start backend**
   ```bash
   cd backend
   uvicorn autodev_agent.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Docker Deployment

### Development Environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Environment

1. **Create production compose file**
   ```bash
   cp docker-compose.yml docker-compose.prod.yml
   ```

2. **Configure production settings**
   ```yaml
   # docker-compose.prod.yml
   version: '3.8'
   services:
     backend:
       build: ./backend
       environment:
         - APP_ENV=production
         - DATABASE_URL=postgresql://user:pass@postgres:5432/ai_coder_agent
       depends_on:
         - postgres
         - redis
       restart: unless-stopped
       
     frontend:
       build: ./frontend
       ports:
         - "80:80"
       depends_on:
         - backend
       restart: unless-stopped
       
     postgres:
       image: postgres:15
       environment:
         - POSTGRES_PASSWORD=secure_password
         - POSTGRES_DB=ai_coder_agent
       volumes:
         - postgres_data:/var/lib/postgresql/data
       restart: unless-stopped
       
     redis:
       image: redis:7-alpine
       restart: unless-stopped
       
     nginx:
       image: nginx:alpine
       ports:
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       depends_on:
         - frontend
         - backend
       restart: unless-stopped
   
   volumes:
     postgres_data:
   ```

3. **Deploy to production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Docker Images

#### Backend Image
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "autodev_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Image
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3.0+

### Helm Chart

1. **Create Helm chart structure**
   ```
   k8s/
   ├── Chart.yaml
   ├── values.yaml
   ├── templates/
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   ├── ingress.yaml
   │   ├── configmap.yaml
   │   └── secret.yaml
   ```

2. **Deploy with Helm**
   ```bash
   # Add Helm repository
   helm repo add ai-coder-agent https://your-org.github.io/ai-coder-agent
   
   # Install chart
   helm install ai-coder-agent ai-coder-agent/ai-coder-agent \
     --set environment=production \
     --set database.password=secure_password
   ```

### Manual Kubernetes Deployment

1. **Create namespace**
   ```bash
   kubectl create namespace ai-coder-agent
   ```

2. **Apply secrets**
   ```bash
   kubectl apply -f k8s/secrets.yaml
   ```

3. **Deploy services**
   ```bash
   kubectl apply -f k8s/
   ```

4. **Verify deployment**
   ```bash
   kubectl get pods -n ai-coder-agent
   kubectl get services -n ai-coder-agent
   ```

### Kubernetes Manifests

#### Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-coder-agent-backend
  namespace: ai-coder-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-coder-agent-backend
  template:
    metadata:
      labels:
        app: ai-coder-agent-backend
    spec:
      containers:
      - name: backend
        image: your-registry/ai-coder-agent-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-coder-agent-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-coder-agent-backend
  namespace: ai-coder-agent
spec:
  selector:
    app: ai-coder-agent-backend
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

#### Ingress
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ai-coder-agent-ingress
  namespace: ai-coder-agent
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - ai-coder-agent.your-domain.com
    secretName: ai-coder-agent-tls
  rules:
  - host: ai-coder-agent.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ai-coder-agent-frontend
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: ai-coder-agent-backend
            port:
              number: 80
```

## Cloud Deployment

### AWS Deployment

#### ECS Deployment

1. **Create ECS cluster**
   ```bash
   aws ecs create-cluster --cluster-name ai-coder-agent
   ```

2. **Create task definition**
   ```json
   {
     "family": "ai-coder-agent",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "1024",
     "memory": "2048",
     "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "your-registry/ai-coder-agent-backend:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "APP_ENV",
             "value": "production"
           }
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/ai-coder-agent",
             "awslogs-region": "us-west-2",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

3. **Deploy service**
   ```bash
   aws ecs create-service \
     --cluster ai-coder-agent \
     --service-name ai-coder-agent-service \
     --task-definition ai-coder-agent:1 \
     --desired-count 2 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
   ```

#### EKS Deployment

1. **Create EKS cluster**
   ```bash
   eksctl create cluster \
     --name ai-coder-agent \
     --region us-west-2 \
     --nodegroup-name standard-workers \
     --node-type t3.medium \
     --nodes 3 \
     --nodes-min 1 \
     --nodes-max 4
   ```

2. **Deploy with Helm**
   ```bash
   helm install ai-coder-agent ./k8s \
     --set environment=production \
     --set ingress.enabled=true \
     --set ingress.host=ai-coder-agent.your-domain.com
   ```

### Google Cloud Platform

#### GKE Deployment

1. **Create GKE cluster**
   ```bash
   gcloud container clusters create ai-coder-agent \
     --zone us-central1-a \
     --num-nodes 3 \
     --machine-type e2-medium
   ```

2. **Deploy application**
   ```bash
   kubectl apply -f k8s/
   ```

### Azure

#### AKS Deployment

1. **Create AKS cluster**
   ```bash
   az aks create \
     --resource-group ai-coder-agent-rg \
     --name ai-coder-agent-cluster \
     --node-count 3 \
     --enable-addons monitoring \
     --generate-ssh-keys
   ```

2. **Deploy application**
   ```bash
   kubectl apply -f k8s/
   ```

## Production Considerations

### Performance Optimization

1. **Database optimization**
   ```sql
   -- Create indexes
   CREATE INDEX idx_conversations_user_id ON conversations(user_id);
   CREATE INDEX idx_workflows_status ON workflows(status);
   CREATE INDEX idx_logs_timestamp ON logs(timestamp);
   
   -- Configure connection pooling
   -- In alembic/env.py
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=30,
       pool_pre_ping=True
   )
   ```

2. **Caching strategy**
   ```python
   # Redis caching
   from redis import Redis
   from functools import wraps
   
   redis_client = Redis(host='localhost', port=6379, db=0)
   
   def cache_result(ttl=300):
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
               result = redis_client.get(cache_key)
               if result is None:
                   result = func(*args, **kwargs)
                   redis_client.setex(cache_key, ttl, result)
               return result
           return wrapper
       return decorator
   ```

3. **Load balancing**
   ```nginx
   # nginx.conf
   upstream backend {
       least_conn;
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   
   server {
       listen 80;
       server_name ai-coder-agent.your-domain.com;
       
       location / {
           proxy_pass http://frontend;
       }
       
       location /api {
           proxy_pass http://backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Security Hardening

1. **SSL/TLS configuration**
   ```nginx
   server {
       listen 443 ssl http2;
       ssl_certificate /etc/nginx/ssl/cert.pem;
       ssl_certificate_key /etc/nginx/ssl/key.pem;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
   }
   ```

2. **Security headers**
   ```python
   # FastAPI middleware
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   from fastapi.middleware.trustedhost import TrustedHostMiddleware
   
   app = FastAPI()
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-domain.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   
   app.add_middleware(
       TrustedHostMiddleware,
       allowed_hosts=["your-domain.com", "*.your-domain.com"]
   )
   ```

3. **Rate limiting**
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
   
   @app.get("/api/v1/agents")
   @limiter.limit("100/minute")
   async def get_agents(request: Request):
       return {"agents": []}
   ```

## Monitoring & Observability

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-coder-agent-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Grafana Dashboards

1. **Application metrics**
   - Request rate, response time, error rate
   - Database connection pool status
   - Agent execution metrics

2. **Infrastructure metrics**
   - CPU, memory, disk usage
   - Network I/O
   - Container resource usage

3. **Business metrics**
   - Workflow completion rate
   - Agent success/failure rates
   - User activity patterns

### Alerting Rules

```yaml
# alerting-rules.yml
groups:
  - name: ai-coder-agent
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          
      - alert: DatabaseConnectionHigh
        expr: database_connections > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: Database connection pool nearly full
```

## Troubleshooting

### Common Issues

1. **Database connection errors**
   ```bash
   # Check database connectivity
   docker exec -it postgres psql -U postgres -d ai_coder_agent
   
   # Check connection pool
   SELECT * FROM pg_stat_activity;
   ```

2. **Memory issues**
   ```bash
   # Check memory usage
   docker stats
   
   # Increase memory limits
   docker-compose up -d --scale backend=2
   ```

3. **Performance issues**
   ```bash
   # Check logs
   docker-compose logs -f backend
   
   # Monitor metrics
   curl http://localhost:8000/metrics
   ```

### Debug Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec backend python -c "import autodev_agent; print('OK')"

# Check database migrations
docker-compose exec backend alembic current

# Monitor resource usage
docker stats

# Check network connectivity
docker-compose exec backend ping postgres
```

### Performance Tuning

1. **Database optimization**
   ```sql
   -- Analyze table statistics
   ANALYZE conversations;
   ANALYZE workflows;
   
   -- Check slow queries
   SELECT query, calls, total_time, mean_time
   FROM pg_stat_statements
   ORDER BY mean_time DESC
   LIMIT 10;
   ```

2. **Application tuning**
   ```python
   # Increase worker processes
   uvicorn autodev_agent.main:app --workers 4 --host 0.0.0.0 --port 8000
   
   # Enable profiling
   import cProfile
   import pstats
   
   profiler = cProfile.Profile()
   profiler.enable()
   # Your code here
   profiler.disable()
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats()
   ```

## Backup & Recovery

### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U postgres ai_coder_agent > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U postgres ai_coder_agent < backup.sql
```

### File System Backup

```bash
# Backup logs and data
tar -czf backup-$(date +%Y%m%d).tar.gz logs/ memory/ summaries/

# Restore backup
tar -xzf backup-20231201.tar.gz
```

### Automated Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Database backup
docker-compose exec -T postgres pg_dump -U postgres ai_coder_agent > $BACKUP_DIR/db_$DATE.sql

# File backup
tar -czf $BACKUP_DIR/files_$DATE.tar.gz logs/ memory/ summaries/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 512M
```

### Auto-scaling

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-coder-agent-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-coder-agent-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

This deployment guide provides comprehensive instructions for deploying the AI Coder Agent System in various environments, from local development to production-scale deployments.