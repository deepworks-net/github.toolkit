# Core Action: Branch Operations

## Overview

The Branch Operations action is a core (atomic) action that provides a complete interface for managing Git branches in GitHub Actions workflows. It handles creation, deletion, checkout, merging, and listing of branches with robust error handling.

## Usage

```yaml
- name: Create Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
  with:
    action: create
    branch_name: feature/my-feature
    base_branch: develop
    remote: true
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `action` | Branch operation to perform (create, delete, list, checkout, merge, push) | Yes | N/A |
| `branch_name` | Name of the branch to operate on | No* | N/A |
| `base_branch` | Base branch for creating or merging | No | `main` |
| `force` | Force operation (used with delete, checkout, or merge) | No | `false` |
| `message` | Commit message for merge operations | No | N/A |
| `pattern` | Pattern for listing branches (e.g. "feature/*") | No | N/A |
| `remote` | Include remote operations (push/delete remote branch) | No | `false` |

*Required for all actions except 'list'

## Outputs

| Output | Description |
|--------|-------------|
| `branches` | Comma-separated list of branches (when using list action) |
| `result` | Operation result (success/failure) |
| `current_branch` | Current branch after operation |

## Behavior Matrix

### Create Operation

- Creates a new branch from specified base branch
- Pulls latest changes from base branch first
- Optionally pushes to remote if `remote: true`
- Sets current_branch to the newly created branch

### Delete Operation

- Deletes the specified branch
- Optionally deletes remote branch if `remote: true`
- Automatically switches to another branch if deleting current
- Supports force delete with `force: true`

### Checkout Operation

- Checks out the specified branch
- Supports force checkout with `force: true` to discard local changes
- Sets current_branch to the checked out branch

### Merge Operation

- Merges specified branch into current or base branch
- Supports custom commit message with `message`
- Supports force merge with `force: true` to automatically resolve conflicts
- Sets current_branch to branch being merged into

### List Operation

- Lists branches matching optional pattern
- Includes remote branches if `remote: true`
- Returns branches as comma-separated list in output

### Push Operation

- Pushes branch to remote
- Supports force push with `force: true`
- Defaults to current branch if branch_name not specified

## Error Cases

The action will fail with clear error messages in these cases:

1. **Invalid Action**
   - Action parameter is missing or not one of: create, delete, list, checkout, merge, push

2. **Missing Branch Name**
   - Branch name not provided for operations that require it

3. **Git Errors**
   - Branch already exists (when creating)
   - Branch doesn't exist (when deleting, checking out, merging)
   - Merge conflicts (when not using force)

4. **Remote Operation Failures**
   - Remote push/delete errors
   - Authentication issues
   - Network problems

## Examples

### Create and Push Feature Branch

```yaml
- name: Create Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
  with:
    action: create
    branch_name: feature/my-feature
    base_branch: develop
    remote: true
```

### List Feature Branches

```yaml
- name: List Feature Branches
  id: list-branches
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
  with:
    action: list
    pattern: 'feature/*'

- name: Show Branches
  run: echo "Found branches: {% raw %}${{ steps.list-branches.outputs.branches }}{% endraw %}"
```

### Merge and Delete Branch

```yaml
- name: Merge Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
  with:
    action: merge
    branch_name: feature/completed-feature
    base_branch: main
    message: "Merge feature branch into main"

- name: Delete Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
  with:
    action: delete
    branch_name: feature/completed-feature
    remote: true
```

### Feature Branch Workflow Example

```yaml
jobs:
  feature-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Create a new feature branch
      - name: Create Feature Branch
        id: create-branch
        uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
        with:
          action: create
          branch_name: feature/new-feature
          base_branch: develop
          remote: true

      # Make changes and commit them...

      # Push the feature branch
      - name: Push Feature Branch
        uses: deepworks-net/github.toolkit/actions/core/branch_operations@v1
        with:
          action: push
          branch_name: feature/new-feature
```

## Implementation

### Core Files

- `main.py`: Branch operations logic and GitBranchOperations class
- `action.yml`: Action metadata and input/output definitions
- `Dockerfile`: Standardized container configuration

### Docker Configuration

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy script
COPY main.py /app/main.py

# Make script executable
RUN chmod +x /app/main.py

# Set the entrypoint
ENTRYPOINT ["/app/main.py"]
```