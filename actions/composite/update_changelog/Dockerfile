FROM python:3.9-slim

WORKDIR /action

# Install gh CLI and git
RUN apt-get update && \
    apt-get install -y git curl && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# Configure git to trust the workspace
RUN git config --global --add safe.directory /github/workspace

COPY update_changelog.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/update_changelog.py"]