# Generated from FCM - DO NOT EDIT
FROM python:3.9-slim

# Install system requirements
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy implementation
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
