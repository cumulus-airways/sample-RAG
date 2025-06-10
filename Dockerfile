FROM python:3.11-slim

# Install git to clone repo during build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your app code into image
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variable if needed
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
