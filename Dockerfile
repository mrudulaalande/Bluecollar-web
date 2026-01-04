FROM python:3.11-slim

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies required for builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create necessary directories
RUN mkdir -p uploads/profiles

# Expose the standard Cloud Run port
EXPOSE 8080

# Make start script executable
RUN chmod +x start.sh

# The start.sh script handles routing between API/UI via SERVICE_TYPE env var
CMD ["./start.sh"]
