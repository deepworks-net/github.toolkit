FROM python:3.9-slim

WORKDIR /action
RUN apt-get update && \
    apt-get install -y git curl && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# Add environment setup script
RUN echo '#!/bin/sh\n\
export GH_TOKEN="$INPUT_GITHUB_TOKEN"\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

COPY release_notes.py /action/
COPY action.yml /action/

ENTRYPOINT ["/entrypoint.sh", "python", "/action/release_notes.py"]