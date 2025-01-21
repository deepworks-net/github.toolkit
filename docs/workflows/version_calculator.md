# Version Calculator Workflow

## Overview

The Version Calculator workflow provides a reusable workflow for calculating version numbers based on Git tags and commit history. It wraps the Version Calculator core action for easy integration into external repositories.

## Usage

```yaml
name: Calculate Version

on:
  workflow_dispatch:  # Manual trigger
  push:              # Auto trigger

jobs:
  get-version:
    uses: deepworks-net/github.toolkit/.github/workflows/core.action.version_calculator.yml@v1
    with:
      default_version: "v0.1.0"  # Optional
      version_prefix: "v"        # Optional
      tag_pattern: "v*"         # Optional
```

## Inputs

### `default_version` (Optional)

- **Description**: Default version to use when no tags exist
- **Type**: String
- **Default**: `v0.1.0`
- **Note**: Must match format `{prefix}\d+\.\d+\.\d+`

### `version_prefix` (Optional)

- **Description**: Prefix for version tags
- **Type**: String
- **Default**: `v`
- **Example**: `'v'` for v1.0.0 or `'ver'` for ver1.0.0

### `tag_pattern` (Optional)

- **Description**: Pattern to match version tags
- **Type**: String
- **Default**: `v*`
- **Note**: Should align with version_prefix

## Outputs

### `next_version`

- **Description**: The calculated next version
- **Type**: String
- **Format**: `{prefix}\d+\.\d+\.\d+`

### `current_version`

- **Description**: Current version (latest tag or default)
- **Type**: String
- **Format**: `{prefix}\d+\.\d+\.\d+`

### `commit_count`

- **Description**: Number of commits since current version
- **Type**: Number
- **Note**: Returns 0 when using default_version

## Behavior

### Initial Run (No Tags)

```yaml
Inputs:
  default_version: "v0.1.0"
  version_prefix: "v"
  tag_pattern: "v*"

Outputs:
  current_version: "v0.1.0"
  next_version: "v0.1.0"
  commit_count: 0
```

### With Existing Tag

```yaml
# Repository state:
# - Latest tag: v1.0.0
# - 2 new commits

Outputs:
  current_version: "v1.0.0"
  next_version: "v1.0.2"
  commit_count: 2
```

### Custom Prefix

```yaml
Inputs:
  default_version: "ver0.1.0"
  version_prefix: "ver"
  tag_pattern: "ver*"

# Repository state:
# - Latest tag: ver1.0.0
# - 1 new commit

Outputs:
  current_version: "ver1.0.0"
  next_version: "ver1.0.1"
  commit_count: 1
```

## Example Implementations

### Basic Usage

```yaml
jobs:
  version:
    uses: deepworks-net/github.toolkit/.github/workflows/core.action.version_calculator.yml@v1

  build:
    needs: version
    steps:
      - name: Use Version
        run: |
          echo "Next version: ${% raw %}{{ needs.version.outputs.next_version }}{% endraw %}"
          echo "Current version: ${% raw %}{{ needs.version.outputs.current_version }}{% endraw %}"
          echo "Commit count: ${% raw %}{{ needs.version.outputs.commit_count }}{% endraw %}"
```

### Custom Versioning

```yaml
jobs:
  version:
    uses: deepworks-net/github.toolkit/.github/workflows/core.action.version_calculator.yml@v1
    with:
      default_version: "ver0.1.0"
      version_prefix: "ver"
      tag_pattern: "ver*"
```

## Error Handling

The workflow handles errors from the core action:

1. **Input Validation**
    - Invalid version format
    - Mismatched prefix/default_version
    - Invalid patterns

2. **Git Operations**
    - Repository access issues
    - Tag retrieval failures
    - Configuration problems

3. **Version Calculation**
    - Invalid tag formats
    - Counting errors
    - Pattern matching failures
