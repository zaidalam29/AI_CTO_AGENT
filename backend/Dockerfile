FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt || \
    (echo "Retrying installation..." && \
     pip install --no-cache-dir --default-timeout=200 -r requirements.txt)

# Copy application
COPY . .

# Create directories
RUN mkdir -p logs vector_store models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]