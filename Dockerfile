FROM python:3.11-slim-buster

WORKDIR /ml_dev_app
COPY  . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    gcc \
    g++
RUN pip install --upgrade pip    
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "ml_dev_server:app", "--host", "0.0.0.0", "--port", "9100", "--workers", "8", "--limit-concurrency", "300"]