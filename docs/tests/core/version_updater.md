# Version Updater Tests

## Overview

The test suite for the Version Updater core action validates file updates, error handling, and output consistency across different file types.

## Test Structure

```yaml
# .github/workflows/test.core.action.version_updater.yml
on:
  pull_request:
    paths:
      - 'actions/core/version_updater/**'
      - '.github/workflows/core.action.version_updater.yml'
      - '.github/workflows/test.core.action.version_updater.yml'
  workflow_dispatch:
```

## Test Cases

### 1. YAML File Update

Tests version updates in YAML files.

```yaml
test-yaml-update:
  steps:
    - Create Test File
      # Create YAML with version field
    - Run Updater
      # Input:
      # - version: 'v2.0.0'
      # - files: ["test.yml"]
    - Verify Output
      # Check file content and format
```

### 2. JSON File Update

Tests version updates in JSON files.

```yaml
test-json-update:
  steps:
    - Create Test File
      # Create JSON with version field
    - Run Updater
    - Verify Output
      # Check JSON structure and format
      # Use jq for comparison
```

### 3. Multiple Files Update

Tests updating multiple files simultaneously.

```yaml
test-multiple-files:
  steps:
    - Create Test Files
      # Create YAML and JSON files
    - Run Updater
      # Input: multiple files
    - Verify Outputs
      # Check all files updated correctly
```

### 4. Version Prefix Handling

Tests prefix stripping and preservation.

```yaml
test-keep-v-prefix:
  steps:
    - Create Test File
    - Run Updater
      # Input: strip_v_prefix: false
    - Verify Output
      # Check prefix maintained
```

### 5. Invalid Scenarios

Tests error handling for various failure cases.

```yaml
test-invalid-version:
  steps:
    - Run Updater with invalid version
    - Verify failure

test-missing-file:
  steps:
    - Run Updater with nonexistent file
    - Verify empty output array

test-no-version-field:
  steps:
    - Create file without version
    - Run Updater
    - Verify handling
```

## File Creation Templates

### YAML Test File

```yaml
- name: Create Test YAML
  run: |
    echo "version: 1.0.0" > test.yml
```

### JSON Test File

```yaml
- name: Create Test JSON
  run: |
    echo '{"version": "1.0.0"}' > test.json
```

## Output Verification

### File Content Check

```yaml
- name: Verify Output
  run: |
    content=$(cat test.yml)
    if [[ "$content" != "version: 2.0.0" ]]; then
      echo "Expected 'version: 2.0.0', got '$content'"
      exit 1
    fi
```

### JSON Content Check

```yaml
- name: Verify JSON Output
  run: |
    content=$(cat test.json | jq -c '.')
    expected='{"version":"2.0.0"}'
    if [[ "$content" != "$expected" ]]; then
      echo "Expected '$expected', got '$content'"
      exit 1
    fi
```

### Output Format Check

```yaml
- name: Verify Output Format
  run: |
    output='${% raw %}{{ steps.updater.outputs.files }}{% endraw %}'
    if ! echo "$output" | jq -e . >/dev/null 2>&1; then
      echo "Invalid JSON array output: $output"
      exit 1
    fi
```

## Error Handling Verification

Tests verify the action:

1. Validates input version format
2. Handles missing/invalid files
3. Reports file update status correctly
4. Maintains consistent output format

## Common Patterns

### Test Setup

```yaml
steps:
  - uses: actions/checkout@v4
  - name: Create Test File
    run: |
      # Create test files
  - name: Run Version Updater
    id: updater
    uses: ./actions/core/version_updater
    with:
      # Test inputs
```

### Output Verification

```yaml
- name: Verify Outputs
  run: |
    # Check file contents
    # Verify output format
    # Validate results
```

## Local Testing

To run tests locally:

1. Clone repository
2. Navigate to action directory
3. Run test workflow:

```bash
act pull_request -W .github/workflows/test.core.action.version_updater.yml
```

## Adding New Tests

When adding tests:

1. Follow existing patterns for setup/verification
2. Include positive and negative test cases
3. Verify all outputs and file states
4. Document expected behaviors
5. Include clean up steps if needed
