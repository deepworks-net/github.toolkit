# Core Action: Version Updater

## Overview

The Version Updater is a core (atomic) action that updates version numbers across multiple file types (YAML, JSON, and text files). It provides consistent version management while maintaining file-specific formatting.

## Usage

```yaml
- name: Update Versions
  uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
  with:
    version: 'v1.0.0'             # Required: Version to set
    files: |  # Required: Files to update (one per line)
          "README.md"
          "CHANGELOG.md"
          "mkdocs.yml"
    strip_v_prefix: true          # Optional: Remove 'v' prefix when updating
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `version` | Version number to set | Yes | - |
| `files` | JSON array of file paths to update | Yes | - |
| `strip_v_prefix` | Remove 'v' prefix when updating files | No | `true` |

## Outputs

| Output | Description |
|--------|-------------|
| `files` | JSON array of successfully updated files |

## Implementation

### Core Files

- `main.py`: Primary logic for version updating
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

# Install Python dependencies
RUN pip install PyYAML

# Copy action files
COPY *.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/main.py"]
```

## File Type Support

### YAML Files

- Updates `version:` fields
- Preserves file formatting
- Handles different indentation levels

### JSON Files

- Updates `version` key in JSON objects
- Maintains JSON structure
- Preserves formatting and indentation

### Text Files

- Uses regex to find version patterns
- Updates versions while preserving surrounding text
- Handles common version formats

## Example Use Cases

### Update Single File

```yaml
steps:
  - name: Update Version
    uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
    with:
      version: 'v2.0.0'
      files: |
            "package.json"
```

### Update Multiple Files

```yaml
steps:
  - name: Update Versions
    uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
    with:
      version: 'v2.0.0'
      files: |
            "version.yml"
            "package.json"
            "VERSION"
      strip_v_prefix: false
```

## Testing

The action includes comprehensive tests in the `test.core.action.version_updater.yml` workflow, which validates:

- YAML file updates
- JSON file updates
- Multiple file updates
- Version prefix handling
- Error conditions

## Error Handling

The action provides clear error messages for common issues:

- File not found
- Invalid file formats
- Permission issues
- Version pattern mismatches
