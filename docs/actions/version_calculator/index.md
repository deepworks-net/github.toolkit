# Version Calculator Action Documentation

## Overview

The **Version Calculator** GitHub Action dynamically calculates the next version for your repository based on the latest Git tag and commit history. It is designed for seamless integration into CI/CD workflows, especially for projects adhering to semantic versioning.

### Key Features

- Calculates the next version based on the latest Git tag.
- Outputs the current version, next version, and commit count since the last tag.
- Supports customizable version prefixes and tag patterns.
- Fully Dockerized for consistent behavior across environments.

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

## How It Works

### 1. **Git Setup**

The action configures Git to trust the workspace and fetches the repository history to ensure accurate tag and commit detection.

### 2. **Tag Detection**

It retrieves the latest version tag based on a specified pattern and calculates the number of commits since that tag.

### 3. **Version Calculation**

The action increments the patch version number based on the commit count since the latest tag. If no tags exist, it defaults to `default_version`.

---

## Expected Behavior

When the **Version Calculator** action is used:

1. **Initial Run with No Tags**:
    - If no tags exist in the repository, the action will use the `default_version` input (defaulting to `v0.1.0`).
    - Outputs:
        - `current_version`: `v0.1.0`
        - `next_version`: `v0.1.0`
        - `commit_count`: Total commits in the repository.

2. **Run with Existing Tags**:
    - The action identifies the latest tag matching the `tag_pattern`.
    - It calculates the number of commits since the latest tag and increments the patch version accordingly.
    - Outputs:
        - `current_version`: Latest tag.
        - `next_version`: Incremented patch version.
        - `commit_count`: Commits since the latest tag.

3. **Edge Cases**:
    - If the latest tag does not match the `tag_pattern`, the action defaults to `default_version` behavior.
    - If there are no new commits since the latest tag, the `next_version` will match the `current_version`.

---

## Workflow Integration

### Example Workflow

```yaml
name: Version Calculation Workflow

on:
  workflow_dispatch:  # Allows manual triggering

jobs:
  calculate-version:
    runs-on: ubuntu-latest

    outputs:
      next_version: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}
      current_version: ${% raw %}{{ steps.version.outputs.current_version }}{% endraw %}
      commit_count: ${% raw %}{{ steps.version.outputs.commit_count }}{% endraw %}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Calculate next version
        id: version
        uses: deepworks-net/github.actions/actions/version_calculator@v1
        with:
          default_version: "v0.1.0"
          version_prefix: "v"
          tag_pattern: "v*"

      - name: Use calculated version
        run: echo "Next version: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}"
```

---

## Customizing the Workflow

### Dynamic Repository Referencing

To ensure the workflow can dynamically reference the repository it resides in, use the following:

```yaml
with:
  repository: ${% raw %}{{ github.repository }}{% endraw %}
```

This ensures compatibility even when the repository is forked or reused elsewhere.

---

## Debugging Tips

1. **Ensure Proper Tags Exist**: Verify that version tags in the repository match the specified `tag_pattern`.
2. **Fetch Entire History**: Set `fetch-depth: 0` when checking out the repository to include all tags and commits.
3. **Validate Inputs**: Double-check that input parameters match the repository's versioning scheme.

---

## File Structure

### 1. `action.yml`

Defines the inputs, outputs, and execution environment for the action.

### 2. `Dockerfile`

Contains the runtime environment for the action.

### 3. `version_calculator.py`

The main script for calculating the version.

---

## References

### Action Metadata

```yaml
name: Version Calculator
runs:
  using: "docker"
  image: "Dockerfile"
branding:
  icon: "tag"
  color: "blue"
```

### Script Highlights

- Retrieves latest tags using `git tag -l --sort=-v:refname`.
- Calculates commits using `git rev-list`.
- Outputs results to GitHub Actions using `::set-output` commands.
