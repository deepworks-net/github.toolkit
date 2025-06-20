FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements if they exist
COPY requirements.txt* ./

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy implementation
COPY main.py .

# Set the entrypoint
ENTRYPOINT ["python", "/app/main.py"]