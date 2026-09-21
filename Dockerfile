FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "src"]