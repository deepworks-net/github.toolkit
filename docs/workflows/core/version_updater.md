# Version Updater Workflow

## Overview

The Version Updater workflow provides a reusable workflow for updating version numbers across multiple files in a repository. It wraps the Version Updater core action, ensuring consistent version updates across different file types.

## Usage

```yaml
jobs:
  update:
    uses: deepworks-net/github.toolkit/.github/workflows/core.action.version_updater.yml@v1
    with:
      version: 'v2.0.0'
      files: |
        "README.md"
        "package.json"
      strip_v_prefix: true
```

## Inputs

### `version`

- **Description**: Version number to set
- **Required**: Yes
- **Format**: `v1.2.3` or `1.2.3`
- **Example**: `'v2.0.0'`

### `files`

- **Description**: Files to update
- **Required**: Yes
- **Format**: Multi-line string, one file per line
- **Example**:

  ```yaml
  files: |
    "package.json"
    "version.yml"
  ```

### `strip_v_prefix`

- **Description**: Remove 'v' prefix when updating files
- **Required**: No
- **Default**: `true`
- **Type**: boolean

## Outputs

### `files`

- **Description**: JSON array of successfully updated files
- **Type**: String (JSON array)
- **Example**: `'["package.json", "version.yml"]'`

## Examples

### Basic Usage

```yaml
name: Update Version

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'New version'
        required: true
        type: string

jobs:
  update:
    uses: deepworks-net/github.toolkit/.github/workflows/core.action.version_updater.yml@v1
    with:
      version: ${% raw %}{{ inputs.version }}{% endraw %}
      files: |
        "package.json"
        "version.yml"
```

### Integration with Version Calculator

```yaml
name: Release Version Update

jobs:
  calculate:
    uses: ./.github/workflows/core.action.version_calculator.yml@v1
    
  update:
    needs: calculate
    uses: ./.github/workflows/core.action.version_updater.yml@v1
    with:
      version: ${% raw %}{{ needs.calculate.outputs.next_version }}{% endraw %}
      files: |
        "package.json"
        "version.yml"
```

### Keep Version Prefix

```yaml
jobs:
  update:
    uses: ./.github/workflows/core.action.version_updater.yml@v1
    with:
      version: 'v2.0.0'
      files: |
        "config.yml"
      strip_v_prefix: false
```

## Error Handling

The workflow handles several error cases:

1. **Input Validation**
    - Invalid version format
    - Empty files list
    - Invalid file paths

2. **File Operations**
    - Missing files
    - Permission issues
    - Invalid file formats

3. **Version Updates**
    - No version fields found
    - Update failures

### Error Outputs

- Failed updates result in empty file array
- Exit code 1 indicates failures
- Detailed error messages in logs

## Behavior Matrix

### All Files Updated

```yaml
# Input
version: 'v2.0.0'
files: |
  "file1.yml"
  "file2.json"

# Output
files: '["file1.yml", "file2.json"]'
exit_code: 0
```

### Partial Update

```yaml
# Input
version: 'v2.0.0'
files: |
  "exists.json"
  "missing.yml"

# Output
files: '["exists.json"]'
exit_code: 1
```

### No Files Updated

```yaml
# Input
version: 'v2.0.0'
files: |
  "missing.json"

# Output
files: '[]'
exit_code: 1
```

## Implementation Details

1. **Checkout**
    - Fetches repository content
    - No depth limitation
    - Main branch checkout

2. **Version Update**
    - Preserves file formatting
    - Maintains file structure
    - Handles multiple file types

3. **Output Handling**
    - JSON array format
    - Consistent error reporting
    - Clear success/failure indication
