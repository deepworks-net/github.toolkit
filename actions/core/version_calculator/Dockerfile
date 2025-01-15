FROM python:3.9-slim

WORKDIR /action
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Configure git to trust the workspace
RUN git config --global --add safe.directory /github/workspace

COPY version_calculator.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/version_calculator.py"]
