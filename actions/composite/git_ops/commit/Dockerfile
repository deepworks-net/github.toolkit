FROM python:3.9-slim

WORKDIR /app

COPY src/ /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "/app/git_commit_operations.py"]