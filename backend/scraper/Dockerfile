FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper .

# Ensure logs go to stdout/stderr
ENV PYTHONUNBUFFERED=1

CMD ["scrapy", "crawl", "exito"]