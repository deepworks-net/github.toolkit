# Core Action: Version Calculator

## Overview

The Version Calculator is a core (atomic) action that calculates the next version number based on Git tags and commit history. It follows semantic versioning principles while maintaining automatability and predictability.

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
| `default_version` | Default version when no tags exist | No | `v0.1.0` |
| `version_prefix` | Prefix for version tags | No | `v` |
| `tag_pattern` | Pattern to match version tags | No | `v*` |

## Outputs

| Output | Description |
|--------|-------------|
| `next_version` | The calculated next version |
| `current_version` | Current version (latest tag or default) |
| `commit_count` | Number of commits since last tag |

## Implementation

### Core Files

- `main.py`: Primary logic for version calculation
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

## Example Use Cases

### Basic Version Calculation

```yaml
steps:
  - name: Calculate Version
    id: version
    uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1

  - name: Use Version
    run: echo "Next version will be ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}"
```

### Custom Version Prefix

```yaml
steps:
  - name: Calculate Version
    uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1
    with:
      version_prefix: 'ver'
      tag_pattern: 'ver*'
```

## Testing

The action includes comprehensive tests in the `test.core.action.version_calculator.yml` workflow, which validates:

- Default version behavior (no tags)
- Version calculation with existing tags
- Custom version prefix handling
- Output completeness

## Error Handling

The action provides clear error messages for common issues:

- Invalid version formats
- Git configuration errors
- Missing repository access
- Tag pattern mismatches
