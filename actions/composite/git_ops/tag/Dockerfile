FROM python:3.9-slim

WORKDIR /action

RUN mkdir -p /action/tag/src

COPY src/ /action/tag/src/
COPY requirements.txt /action/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "/action/tag/src/git_tag_operations.py"]