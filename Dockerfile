FROM python:3.10-slim

# Install git to clone repo during build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install unstructured

WORKDIR /app

# Clone repo during build
RUN git clone https://github.com/Keerthana1695/sample-RAG.git repo

# Copy your app code into image
COPY app.py .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask requests langchain langchain-community elasticsearch sentence-transformers

# Set environment variable if needed
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
