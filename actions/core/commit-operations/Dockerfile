FROM python:3.9-slim

LABEL maintainer="Deepworks"
LABEL description="Generated from FCM"

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy implementation
COPY main.py /main.py
RUN chmod +x /main.py

ENTRYPOINT ["python3", "/main.py"]
