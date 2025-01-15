FROM python:3.9-slim

WORKDIR /action
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY git_tag_operations.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/git_tag_operations.py"]