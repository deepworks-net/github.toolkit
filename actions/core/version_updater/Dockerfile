FROM python:3.9-slim

WORKDIR /action

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Configure git for workspace
RUN git config --global --add safe.directory /github/workspace

# Install Python dependencies
COPY requirements.txt /action/
RUN pip install --no-cache-dir -r requirements.txt

# Copy action files
COPY *.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/main.py"]