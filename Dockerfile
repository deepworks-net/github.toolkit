# From the Base Image
FROM python:3.9-slim

WORKDIR /docs

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Default command (can be overridden)
# Should the port be able to be set?
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]