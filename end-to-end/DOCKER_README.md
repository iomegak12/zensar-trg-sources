# Docker Deployment Instructions

## Building the Docker Image

```bash
docker build -t agentic-rag .
```

## Running with Docker

### Option 1: Direct Docker Run
```bash
docker run -d \
  --name agentic-rag-container \
  -p 50000:50000 \
  -e AZURE_OPENAI_ENDPOINT="your_azure_endpoint" \
  -e AZURE_OPENAI_API_KEY="your_api_key" \
  -e AZURE_DEPLOYMENT_NAME="gpt-4o" \
  -e GOOGLE_SERPER_API_KEY="your_serper_key" \
  agentic-rag:latest
```

### Option 2: Using Docker Compose (Recommended)

1. Set your environment variables in your shell:
```bash
export AZURE_OPENAI_ENDPOINT="your_azure_endpoint"
export AZURE_OPENAI_API_KEY="your_api_key"
export AZURE_DEPLOYMENT_NAME="gpt-4o"
export GOOGLE_SERPER_API_KEY="your_serper_key"
```

2. Run with Docker Compose:
```bash
docker compose up -d
```

## Environment Variables

The following environment variables need to be set:

### Required
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key

### Optional
- `AZURE_DEPLOYMENT_NAME` - Default: "gpt-4o"
- `AZURE_API_VERSION` - Default: "2025-01-01-preview"
- `GOOGLE_SERPER_API_KEY` - For Google search functionality
- `API_PORT` - Default: 50000
- `ENVIRONMENT` - Default: "production"
- `RATE_LIMIT_ENABLED` - Default: false
- `CORS_ENABLED` - Default: true
- `LOG_LEVEL` - Default: "INFO"

## Accessing the Application

Once running, access the application at:
- **Web UI**: http://localhost:50000/ui
- **API Documentation**: http://localhost:50000/docs
- **Health Check**: http://localhost:50000/health
- **Metrics**: http://localhost:50000/metrics

## Monitoring (Optional)

To enable Prometheus and Grafana monitoring:

```bash
docker compose --profile monitoring up -d
```

This will also start:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## Health Checks

The container includes built-in health checks. Check container health:

```bash
docker ps
# Look for "healthy" status
```

## Logs

View application logs:
```bash
docker logs agentic-rag-container -f
```

## Stopping

```bash
# Using Docker Compose
docker compose down

# Using Docker directly
docker stop agentic-rag-container
docker rm agentic-rag-container
```