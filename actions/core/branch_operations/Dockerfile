FROM python:3.9-slim

LABEL maintainer="Deepworks"

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy script
COPY main.py /app/main.py

# Make script executable
RUN chmod +x /app/main.py

# Set the entrypoint
ENTRYPOINT ["/app/main.py"]