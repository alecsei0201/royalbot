
# RoyalBot: production Dockerfile (Fly.io, music-ready, no HTTP port)
# - Python 3.12 slim base
# - FFmpeg + libopus for voice/music
# - Installs requirements (expects discord.py 2.x, PyNaCl, yt-dlp, humanize in requirements.txt)
# - Runs the bot with `python -m app.bot`

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# System deps: ffmpeg for streaming, libopus for voice
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for better build caching
COPY requirements.txt ./
# If requirements.txt is missing some libs, you can also pin here, but
# we rely on requirements.txt to keep a single source of truth.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Default command (Fly will run this)
CMD ["python", "-m", "app.bot"]