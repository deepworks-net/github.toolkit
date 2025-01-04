# Dockerfile for Version Calculation GitHub Action
FROM python:3.9-slim

# Set working directory
WORKDIR /action

# Copy the script into the container
COPY version_calculation.py /action/version_calculation.py

# Set entrypoint to execute the script
ENTRYPOINT ["python", "/action/version_calculation.py"]
