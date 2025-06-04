FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for Playwright and general use
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libnss3 \
    libnss3-tools \
    libnspr4 \
    dbus \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxext6 \
    libxfixes3 \
    libx11-6 \
    libx11-xcb1 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libexpat1 \
    libxcb1 \
    libatspi2.0-0 \
    libdrm2 \
    libxshmfence1 \
    libxinerama1 \
    libxtst6 \
    fonts-liberation \
    ca-certificates \
    wget \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install firefox chromium

COPY scraper .

# Ensure logs go to stdout/stderr
ENV PYTHONUNBUFFERED=1

CMD ["scrapy", "crawl", "exito"]