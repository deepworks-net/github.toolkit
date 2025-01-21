# Core Action: Version Calculator

## Overview

The Version Calculator is a core (atomic) action that calculates the next version number based on Git tags and commit history. It follows semantic versioning principles while providing predictable, automated version calculation.

## Usage

```yaml
- name: Calculate Version
  uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1
  with:
    default_version: 'v0.1.0'      # Optional: Default if no tags exist
    version_prefix: 'v'            # Optional: Prefix for version tags
    tag_pattern: 'v*'             # Optional: Pattern to match version tags
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `default_version` | Default version when no tags exist. Must match prefix format (e.g., 'v0.1.0' or 'ver0.1.0') | No | `v0.1.0` |
| `version_prefix` | Prefix for version tags (e.g., 'v' in v1.0.0) | No | `v` |
| `tag_pattern` | Pattern to match version tags | No | `v*` |

## Outputs

| Output | Description |
|--------|-------------|
| `next_version` | The calculated next version, based on commit count since current version |
| `current_version` | Current version (latest matching tag or default_version if no tags) |
| `commit_count` | Number of commits since the current version (0 if using default version) |

## Behavior Matrix

### No Tags Exist

- `current_version` = default_version
- `next_version` = default_version
- `commit_count` = 0

### Tags Exist, No New Commits

- `current_version` = latest matching tag
- `next_version` = latest matching tag
- `commit_count` = 0

### Tags Exist, New Commits

- `current_version` = latest matching tag
- `next_version` = increment patch version by commit count
- `commit_count` = number of commits since tag

### Custom Prefix

Note: When using a custom prefix, default_version must match the prefix

```yaml
- uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1
  with:
    default_version: 'ver0.1.0'  # Must match prefix
    version_prefix: 'ver'
    tag_pattern: 'ver*'
```

## Example Use Cases

### Basic Version Calculation

```yaml
steps:
  - name: Calculate Version
    id: version
    uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1

  - name: Use Outputs
    run: |
      echo "Current: ${% raw %}{{ steps.version.outputs.current_version }}{% endraw %}"
      echo "Next: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}"
      echo "Commits: ${% raw %}{{ steps.version.outputs.commit_count }}{% endraw %}"
```

### Custom Version Prefix

```yaml
steps:
  - name: Calculate Version
    uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1
    with:
      default_version: 'ver0.1.0'
      version_prefix: 'ver'
      tag_pattern: 'ver*'
```

## Error Cases

The action will fail with clear error messages in these cases:

1. **Invalid Version Format**
    - Version doesn't match pattern: `{prefix}\d+\.\d+\.\d+`
    - Default version doesn't match specified prefix
    - Tag found with invalid format

2. **Git Errors**
    - Unable to access repository
    - Git configuration issues
    - Tag retrieval fails

3. **Input Validation**
    - Mismatched prefix and default_version
    - Invalid version pattern
    - Invalid tag pattern

## Implementation

### Core Files

- `main.py`: Version calculation logic
- `action.yml`: Action metadata and input/output definitions
- `Dockerfile`: Standardized container configuration

### Docker Configuration

```dockerfile
FROM python:3.9-slim

WORKDIR /action

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Configure git for workspace
RUN git config --global --add safe.directory /github/workspace

# Copy action files
COPY *.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/main.py"]
```
