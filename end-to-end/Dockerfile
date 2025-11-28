# Use Python 3.11 Alpine for smaller image size
FROM python:3.11-alpine AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    g++ \
    make \
    curl \
    && rm -rf /var/cache/apk/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY api/ ./api/
COPY urls.txt .

# Copy UI files
COPY ui/ ./ui/

# Set environment variables (can be overridden at runtime)
ENV API_PORT=50000 \
    ENVIRONMENT=production \
    RATE_LIMIT_ENABLED=false \
    CORS_ENABLED=true \
    CORS_ORIGINS=* \
    LOG_LEVEL=INFO \
    DEFAULT_URLS_FALLBACK=true \
    USER_AGENT="AgenticRAG/1.0 (Educational Research Tool)"

# Create non-root user for security
RUN adduser -D -s /bin/sh appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 50000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50000/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "50000"]