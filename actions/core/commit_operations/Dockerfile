FROM python:3.9-slim

LABEL maintainer="Deepworks"
LABEL description="Git commit operations"

# Install git and optimize image size in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip cache purge

COPY main.py /main.py

RUN chmod +x /main.py

ENTRYPOINT ["/main.py"]