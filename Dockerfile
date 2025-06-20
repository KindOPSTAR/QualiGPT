# Multi-stage build for QualiGPT Flask Application
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=qualigpt-webapp.py
ENV FLASK_ENV=production

# Create non-root user
RUN groupadd -r qualigpt && useradd -r -g qualigpt qualigpt

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create necessary directories
RUN mkdir -p /app/templates /app/nltk_data && \
    chown -R qualigpt:qualigpt /app

# Copy application files
COPY --chown=qualigpt:qualigpt qualigpt-webapp.py .
COPY --chown=qualigpt:qualigpt templates/ templates/
COPY --chown=qualigpt:qualigpt requirements.txt .

# Pre-download NLTK data during build for faster startup
USER qualigpt
RUN python -c "import nltk; nltk.download('punkt_tab', download_dir='/app/nltk_data')"

# Install Gunicorn for production serving
USER root
RUN pip install --no-cache-dir gunicorn

# Switch back to non-root user
USER qualigpt

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/', timeout=10)" || exit 1

# Create Gunicorn configuration
USER root
RUN echo 'bind = "0.0.0.0:5000"' > /app/gunicorn.conf.py && \
    echo 'workers = 4' >> /app/gunicorn.conf.py && \
    echo 'worker_class = "sync"' >> /app/gunicorn.conf.py && \
    echo 'worker_connections = 1000' >> /app/gunicorn.conf.py && \
    echo 'timeout = 120' >> /app/gunicorn.conf.py && \
    echo 'keepalive = 2' >> /app/gunicorn.conf.py && \
    echo 'max_requests = 1000' >> /app/gunicorn.conf.py && \
    echo 'max_requests_jitter = 100' >> /app/gunicorn.conf.py && \
    echo 'preload_app = True' >> /app/gunicorn.conf.py && \
    chown qualigpt:qualigpt /app/gunicorn.conf.py

USER qualigpt

# Command to run the application
CMD ["gunicorn", "--config", "gunicorn.conf.py", "qualigpt-webapp:app"]
