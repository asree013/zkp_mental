# Multi-stage / Production Dockerfile for ZK-ML Mental Health FastAPI System
# =========================================================================
# Base Image: Python 3.11 Slim (Debian Bookworm)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.nargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# 1. Install System Dependencies & Noir (Nargo CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    tar \
    gzip \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Noir CLI (Nargo) via official noirup installer
RUN curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash \
    && /root/.nargo/bin/noirup -v 1.0.0-beta.22 || /root/.nargo/bin/noirup \
    && nargo --version

# 3. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy Application Source Code
COPY . .

# 5. Pre-train ML model & compile Noir circuit (must pass without error)
RUN python lib/train_ml_model.py && \
    cd circuit && nargo check

# 6. Expose FastAPI Server Port
EXPOSE 8000

# 7. Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 8. Start FastAPI Application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
