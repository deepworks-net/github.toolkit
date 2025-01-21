# Version Calculator Tests

## Overview

The test suite for the Version Calculator core action validates functionality, error handling, and output consistency.

## Test Structure

```yaml
# .github/workflows/test.core.action.version_calculator.yml
on:
  pull_request:
    paths:
      - 'actions/core/version_calculator/**'
      - '.github/workflows/core.action.version_calculator.yml'
      - '.github/workflows/test.core.action.version_calculator.yml'
  workflow_dispatch:
```

## Test Cases

### 1. Default Version (No Tags)

Tests the behavior when no Git tags exist.

```yaml
test-no-tags:
  steps:
    - Clean Environment
      # Remove local tags
    - Run Calculator
      # Input: default_version: 'v0.1.0'
    - Verify Outputs
      # Expect:
      # - next_version: v0.1.0
      # - current_version: v0.1.0
      # - commit_count: 0
```

### 2. Version With Tags

Tests version calculation with existing tags and commits.

```yaml
test-with-tag:
  steps:
    - Clean Environment
    - Create Test State
      # - Create tag v1.0.0
      # - Add 2 commits
    - Run Calculator
    - Verify Outputs
      # Expect:
      # - next_version: v1.0.2
      # - current_version: v1.0.0
      # - commit_count: 2
```

### 3. Custom Version Prefix

Tests handling of non-standard version prefixes.

```yaml
test-custom-prefix:
  steps:
    - Clean Environment
    - Create Test State
      # - Create tag ver1.0.0
      # - Add 1 commit
    - Run Calculator
      # Input:
      # - version_prefix: 'ver'
      # - tag_pattern: 'ver*'
    - Verify Outputs
      # Expect:
      # - next_version: ver1.0.1
      # - current_version: ver1.0.0
      # - commit_count: 1
```

### 4. Output Verification

Tests completeness and format of all outputs.

```yaml
test-all-outputs:
  steps:
    - Clean Environment
    - Create Test State
      # - Create tag v0.1.0
      # - Add 1 commit
    - Run Calculator
    - Verify All Outputs
      # Check existence and values of:
      # - next_version
      # - current_version
      # - commit_count
```

## Environment Setup

Each test follows a standard setup pattern:

1. **Clean Environment**

    ```yaml
    - name: Clean Local Environment
    run: |
        git config --global user.email "test@github.com"
        git config --global user.name "Test User"
        git tag -l | xargs -r git tag -d
    ```

2. **Test State Creation**

    ```yaml
    - name: Create Test State
    run: |
        git tag <tag_name>
        git commit --allow-empty -m "test commit"
    ```

## Output Verification

### Standard Output Check

```yaml
- name: Verify Output Existence
  run: |
    if [[ -z "${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}" ]] || \
       [[ -z "${% raw %}{{ steps.version.outputs.current_version }}{% endraw %}" ]] || \
       [[ -z "${% raw %}{{ steps.version.outputs.commit_count }}{% endraw %}" ]]; then
      echo "Missing required outputs"
      exit 1
    fi
```

### Value Verification

```yaml
- name: Verify Output Values
  run: |
    if [[ "${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}" != "expected_value" ]]; then
      echo "Expected expected_value, got ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}"
      exit 1
    fi
```

## Error Handling

Tests verify that the action:

1. Handles missing tags appropriately
2. Validates version formats
3. Manages commit counting correctly
4. Provides all required outputs

## Local Testing

To run tests locally:

1. Clone repository
2. Navigate to action directory
3. Run test workflow:

```bash
act pull_request -W .github/workflows/test.core.action.version_calculator.yml
```
