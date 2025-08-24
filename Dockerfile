# Python slim image
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose health port
EXPOSE 8080

# Default to production log level unless overridden
ENV LOG_LEVEL=INFO

# Start the bot
CMD ["python", "-m", "app.bot"]
