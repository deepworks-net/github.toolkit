FROM python:3.9-slim

WORKDIR /action
RUN apt-get update && \
    apt-get install -y git curl && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /github/workspace

RUN mkdir -p /action/branch/src /action/commit/src /action/tag/src

COPY git_ops.py /action/
COPY action.yml /action/
COPY branch/src/git_branch_operations.py /action/branch/src/
COPY commit/src/git_commit_operations.py /action/commit/src/
COPY tag/src/git_tag_operations.py /action/tag/src/

ENTRYPOINT ["python", "/action/git_ops.py"]
