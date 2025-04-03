FROM python:3.9-slim

WORKDIR /action

RUN mkdir -p /action/branch/src

COPY src/ /action/branch/src/
COPY requirements.txt /action/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "/action/branch/src/git_branch_operations.py"]