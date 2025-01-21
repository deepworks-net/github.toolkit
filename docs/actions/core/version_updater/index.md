# Core Action: Version Updater

## Overview

The Version Updater is a core (atomic) action that updates version numbers across multiple file types. It handles YAML, JSON, and text files while preserving file structure and formatting.

## Usage

```yaml
- name: Update Versions
  uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
  with:
    version: 'v2.0.0'       # Required
    files: |               # Required
      "package.json"
      "version.yml"
    strip_v_prefix: true   # Optional
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `version` | Version number to set (format: v1.2.3 or 1.2.3) | Yes | - |
| `files` | Files to update (one per line) | Yes | - |
| `strip_v_prefix` | Remove 'v' prefix when updating files | No | `true` |

## Outputs

| Output | Description |
|--------|-------------|
| `files` | JSON array of successfully updated files |

## File Type Support

### YAML Files (.yml, .yaml)

```yaml
# Input
version: 1.0.0

# Output (with strip_v_prefix: true)
version: 2.0.0

# Output (with strip_v_prefix: false)
version: v2.0.0
```

### JSON Files (.json)

```json
// Input
{
  "version": "1.0.0"
}

// Output (with strip_v_prefix: true)
{
  "version": "2.0.0"
}
```

### Text Files (any extension)

Uses regex pattern matching to find and update version numbers. Matches patterns like:

- `version = 1.0.0`
- `version: "1.0.0"`
- `"version": "1.0.0"`

## Error Handling

The action provides clear error messages and appropriate exit codes:

1. **Version Format**
    - Invalid format provided
    - Missing version input

2. **File Operations**
    - File not found
    - Permission denied
    - Invalid file format (JSON)

3. **Version Fields**
    - No version field found in file
    - Multiple version fields in file

Exit Codes:

- 0: All files successfully updated
- 1: One or more files failed to update

## Implementation

### Core Files

- `main.py`: Version update logic
- `action.yml`: Action metadata and interface
- `Dockerfile`: Standardized container configuration
- `requirements.txt`: Python dependencies

### Dependencies

- Python 3.9
- PyYAML 6.0.1
- Git (for workspace configuration)

## Example Use Cases

### Basic Single File Update

```yaml
- name: Update Package Version
  uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
  with:
    version: 'v2.0.0'
    files: |
      "package.json"
```

### Multiple Files with Different Formats

```yaml
- name: Update All Versions
  uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
  with:
    version: 'v2.0.0'
    files: |
      "package.json"
      "version.yml"
      "VERSION"
```

### Keep Version Prefix

```yaml
- name: Update with Prefix
  uses: deepworks-net/github.toolkit/actions/core/version_updater@v1
  with:
    version: 'v2.0.0'
    files: |
      "config.yml"
    strip_v_prefix: false
```

## Testing

Each feature is verified through automated tests:

1. File Type Support:
    - YAML updates
    - JSON updates
    - Text file updates

2. Version Handling:
    - With/without v prefix
    - Multiple formats
    - Invalid formats

3. Error Cases:
    - Missing files
    - Invalid formats
    - Permission issues