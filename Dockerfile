# Docker Configuration for Pi Bitcoin Miner
# For development and testing without actual hardware

FROM python:3.11-slim

LABEL maintainer="your.email@example.com"
LABEL description="Raspberry Pi Bitcoin Miner - Development Container"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs config

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MINING_MODE=test

# Expose dashboard port (for future web interface)
EXPOSE 8080

# Run in test mode by default
CMD ["python", "controller/main.py"]
