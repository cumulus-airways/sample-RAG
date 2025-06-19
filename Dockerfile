FROM python:3.11-slim

# Set cache directory environment variables early
ENV TRANSFORMERS_CACHE=/tmp/hf_cache
ENV HF_HOME=/tmp/hf_cache
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create writable HuggingFace cache directory
RUN mkdir -p /tmp/hf_cache && chmod -R 777 /tmp/hf_cache

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# (Optional) Pre-download embedding model to cache it inside the image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Run your app
CMD ["python", "app.py"]

