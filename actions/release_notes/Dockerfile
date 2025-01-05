FROM python:3.9-slim

WORKDIR /action
RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /github/workspace

COPY release_notes.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/release_notes.py"]