FROM python:3.9-slim

LABEL maintainer="Deepworks"
LABEL description="Git tag operations"

COPY main.py /main.py

RUN chmod +x /main.py

ENTRYPOINT ["/main.py"]