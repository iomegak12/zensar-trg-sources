# Multi-stage build for optimized Alpine-based Python image
# Stage 1: Builder stage
FROM python:3.11-alpine AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-alpine

# Set labels for metadata
LABEL maintainer="Zensar AI for Leaders"
LABEL description="Products Management MCP Server"
LABEL version="1.0.0"

# Install runtime dependencies only
RUN apk add --no-cache \
    libpq \
    libffi && \
    addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY product_management/ ./product_management/
COPY mcp_server.py .
COPY run_mcp_server.py .
COPY scripts/ ./scripts/
COPY .env.example .

# Create .env from example if not exists
RUN cp .env.example .env

# Create necessary directories
RUN mkdir -p dbs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_SERVER_HOST=0.0.0.0 \
    MCP_SERVER_PORT=50000 \
    DATABASE_PATH=dbs/products.db

# Expose port
EXPOSE 50000

# Run the MCP server
CMD ["python", "run_mcp_server.py"]
