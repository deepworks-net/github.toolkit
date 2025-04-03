FROM python:3.9-slim

WORKDIR /action

RUN mkdir -p /action/commit/src

COPY src/ /action/commit/src/
COPY requirements.txt /action/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "/action/commit/src/git_commit_operations.py"]