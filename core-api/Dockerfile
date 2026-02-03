# spearmint/core-api/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for pandas/numpy/scipy compilation if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src
COPY .env.example /app/.env
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Set Python Path
ENV PYTHONPATH=/app
ENV MODULE_NAME=src.financial_analysis.api.main
ENV VARIABLE_NAME=app
ENV PORT=8000

EXPOSE 8000

# Run via entrypoint script (initializes DB then starts uvicorn)
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD []
