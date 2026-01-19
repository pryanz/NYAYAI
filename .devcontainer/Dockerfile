# -------------------------------
# Base Image (CUDA 12.1 + Python compatible)
# -------------------------------
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------------
# System Dependencies (Python + OCR + CV)
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    curl \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    poppler-utils \
    libleptonica-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Make python default
RUN ln -s /usr/bin/python3 /usr/bin/python

# -------------------------------
# Workdir
# -------------------------------
WORKDIR /workspaces/NyayAI

# -------------------------------
# Python Dependencies
# -------------------------------
COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Application Code
# -------------------------------
COPY . .

# -------------------------------
# Default Command
# -------------------------------
CMD ["sleep", "infinity"]
