# Version Calculator Workflow Documentation

## Overview

The **Version Calculator Workflow** is a reusable GitHub workflow designed to calculate the next version of a repository based on the latest Git tag and commit history. It integrates seamlessly into external repositories for dynamic versioning.

### Key Features

- Dynamically calculates the next version.
- Provides the current version and commit count since the last tag.
- Designed for external repositories to reuse without modifying internal workflows.

---

## Inputs

### 1. `default_version` (Optional)

- **Description**: Default version to use when no tags exist.
- **Type**: String
- **Default**: `v0.1.0`

### 2. `version_prefix` (Optional)

- **Description**: Prefix for version tags (e.g., `v` in `v1.0.0`).
- **Type**: String
- **Default**: `v`

### 3. `tag_pattern` (Optional)

- **Description**: Pattern to match version tags.
- **Type**: String
- **Default**: `v*`

---

## Outputs

### 1. `next_version`

- **Description**: The calculated next version.

### 2. `current_version`

- **Description**: The current version (latest tag or default).

### 3. `commit_count`

- **Description**: The number of commits since the last tag.

---

## Expected Behavior

When the **Version Calculator Workflow** is used:

1. **Initial Run with No Tags**:
    - If no tags exist in the repository, the workflow uses the `default_version` input (defaulting to `v0.1.0`).
    - Outputs:
        - `current_version`: `v0.1.0`
        - `next_version`: `v0.1.0`
        - `commit_count`: Total commits in the repository.

2. **Run with Existing Tags**:
    - The workflow identifies the latest tag matching the `tag_pattern`.
    - It calculates the number of commits since the latest tag and increments the patch version accordingly.
    - Outputs:
        - `current_version`: Latest tag.
        - `next_version`: Incremented patch version.
        - `commit_count`: Commits since the latest tag.

3. **Edge Cases**:
    - If the latest tag does not match the `tag_pattern`, the workflow defaults to `default_version` behavior.
    - If there are no new commits since the latest tag, the `next_version` will match the `current_version`.

---

## Example Usage

### Workflow Call

To use the Version Calculator Workflow in an external repository:

```yaml
name: Calculate Version

on:
  workflow_dispatch:  # Allows manual triggering

jobs:
  calculate-version:
    uses: your-username/github.actions/.github/workflows/version_calculator.yml@v1
    with:
      default_version: "v0.1.0"
      version_prefix: "v"
      tag_pattern: "v*"

    outputs:
      next_version: ${% raw %}{{ jobs.calculate-version.outputs.next_version }}{% endraw %}
      current_version: ${% raw %}{{ jobs.calculate-version.outputs.current_version }}{% endraw %}
      commit_count: ${% raw %}{{ jobs.calculate-version.outputs.commit_count }}{% endraw %}
```

### Using Outputs in Subsequent Steps

Once the workflow is invoked, its outputs can be used in downstream jobs or steps:

```yaml
      - name: Use Calculated Version
        run: |
          echo "Next version: ${% raw %}{{ jobs.calculate-version.outputs.next_version }}{% endraw %}"
          echo "Current version: ${% raw %}{{ jobs.calculate-version.outputs.current_version }}{% endraw %}"
          echo "Commits since last tag: ${% raw %}{{ jobs.calculate-version.outputs.commit_count }}{% endraw %}"
```

---

## Debugging Tips

1. **Ensure Proper Tags Exist**: Verify that version tags in the repository match the specified `tag_pattern`.
2. **Fetch Entire History**: Set `fetch-depth: 0` in the `actions/checkout` step to include all tags and commits.
3. **Validate Inputs**: Double-check that input parameters match the repository's versioning scheme.

---

## File Structure

### 1. `version_calculator.yml`

Defines the reusable workflow with input and output specifications.

### 2. `version_calculator.py`

The Python script used for version calculation (referenced within the action).

---

## References

### Workflow Highlights

```yaml
on:
  workflow_dispatch:  # Allows manual triggering
  workflow_call:
    inputs:
      default_version:
        type: string
        required: false
        default: 'v0.1.0'
      version_prefix:
        type: string
        required: false
        default: 'v'
      tag_pattern:
        type: string
        required: false
        default: 'v*'
    outputs:
      next_version:
        description: "Calculated next version"
        value: ${% raw %}{{ jobs.calculate-version.outputs.next_version }}{% endraw %}
      current_version:
        description: "Current version"
        value: ${% raw %}{{ jobs.calculate-version.outputs.current_version }}{% endraw %}
      commit_count:
        description: "Commit count since last tag"
        value: ${% raw %}{{ jobs.calculate-version.outputs.commit_count }}{% endraw %}
```

### Workflow Outputs

- `next_version`: Computed based on commits since the last tag.
- `current_version`: The latest tag or default version.
- `commit_count`: Number of commits since the last tag.
