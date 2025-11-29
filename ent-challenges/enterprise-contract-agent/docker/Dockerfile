FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model for PII detection
RUN python -m spacy download en_core_web_lg

# Copy application code
COPY src/ ./src/
COPY sample_contracts/ ./sample_contracts/

# Create output directory
RUN mkdir -p /app/output

# Expose ports
EXPOSE 8000 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "src.main"]
