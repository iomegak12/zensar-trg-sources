# 🤖 Agentic RAG - Enterprise RAG System with REST API

> **This Agentic RAG supports enterprise system RAG design with best practices**

A production-ready Agentic Retrieval-Augmented Generation (RAG) system built with LangChain, LangGraph, and FastAPI. Features self-reflective capabilities, safety guardrails, and comprehensive monitoring.

## 🌟 Features

### Core RAG Capabilities
- **🧠 Self-Reflective RAG**: Automatically rewrites questions and improves responses
- **🛡️ Safety Guardrails**: Input/output content filtering and safety checks
- **📊 Quality Grading**: Document relevance, hallucination detection, and answer quality assessment
- **🔄 Adaptive Workflow**: Dynamic routing based on content analysis
- **📚 Multi-Source Knowledge**: Support for web scraping, Wikipedia, Google Search, and Arxiv

### REST API Features
- **⚡ FastAPI**: High-performance async API with automatic OpenAPI documentation
- **🔒 Rate Limiting**: Configurable IP-based rate limiting (disabled by default)
- **🌐 CORS Support**: Cross-origin resource sharing with configurable origins
- **📈 Prometheus Metrics**: Built-in `/metrics` endpoint for monitoring
- **🏥 Health Checks**: Comprehensive health monitoring
- **🎨 Colorful Logging**: Beautiful console logs with colorama
- **🔄 Vector Store Refresh**: Runtime vector database reinitialization

### Enterprise Features
- **🐳 Docker Support**: Production-ready containerization
- **📊 Monitoring Stack**: Prometheus + Grafana integration
- **🔧 Configuration Management**: Environment-based configuration
- **📝 API Documentation**: Automatic Swagger/OpenAPI docs
- **🛡️ Security**: Non-root Docker user, input validation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Azure OpenAI account
- Google Serper API key (optional, for web search)

### Installation

1. **Clone and setup environment**
   ```bash
   git clone <repository-url>
   cd agentic-rag
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Setup vector store URLs**
   ```bash
   # Edit urls.txt with your knowledge base URLs
   echo "https://docs.python.org" >> urls.txt
   echo "https://fastapi.tiangolo.com" >> urls.txt
   ```

### Running the API

#### Development Mode
```bash
# Activate virtual environment first
source env/bin/activate  # On Windows: env\Scripts\activate

# Start the API server
python api/main.py
```

#### Production Mode
```bash
uvicorn api.main:app --host 0.0.0.0 --port 50000 --workers 4
```

#### Docker
```bash
# Build and run with Docker
docker build -t agentic-rag .
docker run -p 50000:50000 agentic-rag

# Or use docker-compose
docker-compose up -d
```

## 📖 API Documentation

Once the server is running, access:

- **API Documentation**: http://localhost:50000/docs
- **ReDoc Documentation**: http://localhost:50000/redoc
- **OpenAPI JSON**: http://localhost:50000/openapi.json

### Available Endpoints

#### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | Health check with system status |
| `POST` | `/query` | Query the Agentic RAG system |
| `POST` | `/refresh` | Refresh vector store (reinitialize) |
| `GET` | `/metrics` | Prometheus metrics |

#### Query Example

```bash
curl -X POST "http://localhost:50000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is machine learning?"
     }'
```

**Response:**
```json
{
  "answer": "Machine learning is a branch of artificial intelligence...",
  "metadata": {
    "input_safe": true,
    "relevance_score": "yes",
    "hallucination_score": "yes",
    "answer_score": "yes",
    "output_safe": true,
    "rewrites": 0
  },
  "processing_time": 2.45
}
```

## ⚙️ Configuration

All configuration is managed through environment variables. Key settings:

### API Configuration
```bash
API_PORT=50000                    # Server port
ENVIRONMENT=production            # Environment (development/production)
LOG_LEVEL=INFO                   # Logging level
```

### Rate Limiting
```bash
RATE_LIMIT_ENABLED=false         # Enable/disable rate limiting
RATE_LIMIT=100/minute           # Rate limit per IP
```

### CORS Settings
```bash
CORS_ENABLED=true               # Enable CORS
CORS_ORIGINS=*                  # Allowed origins (* for all)
```

### Azure OpenAI
```bash
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
AZURE_DEPLOYMENT_NAME=gpt-4o
AZURE_API_VERSION=2025-01-01-preview
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

## 📁 Project Structure

```
agentic-rag/
├── api/                         # FastAPI application
│   └── main.py                 # API server and endpoints
├── src/agentic_rag/            # Core RAG system
│   ├── __init__.py             # Package entry point
│   ├── config.py               # Configuration management
│   ├── prompts.py              # Centralized prompts
│   ├── main.py                 # Main AgenticRAG class
│   ├── core/                   # Core workflow components
│   ├── tools/                  # External tools
│   ├── guardrails/             # Safety mechanisms
│   └── graders/                # Quality assessment
├── tests/                      # Test suite
├── monitoring/                 # Monitoring configuration
├── docker-compose.yml          # Multi-service deployment
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── urls.txt                    # Knowledge base URLs
└── README.md                   # This file
```

## 🐳 Docker Deployment

### Simple Deployment
```bash
# Build the image
docker build -t agentic-rag .

# Run the container
docker run -d \
  --name agentic-rag-api \
  -p 50000:50000 \
  --env-file .env \
  agentic-rag
```

### Full Stack with Monitoring
```bash
# Start all services (API + Monitoring)
docker-compose --profile monitoring up -d

# Access services:
# - API: http://localhost:50000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

## 🧪 Testing

### Run Tests
```bash
# Activate environment
source env/bin/activate

# Run diagnostic tests
python tests/diagnostic.py

# Run functionality tests
python tests/agentic-rag-test.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using LangChain, LangGraph, FastAPI, and Azure OpenAI**