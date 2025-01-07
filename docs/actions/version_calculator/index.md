# Version Calculator GitHub Action

This GitHub Action calculates the next version of your repository based on the latest Git tag. It is ideal for managing semantic versioning in repositories, ensuring consistent version updates based on commit activity.

## Features

- **Semantic Versioning**: Automatically calculates the next patch version based on commits since the latest tag.
- **Customizable Tagging**: Supports custom version prefixes and tag patterns.
- **Commit Tracking**: Outputs the number of commits since the last version tag.

---

## Inputs

| Input            | Description                                         | Required | Default  |
|-------------------|-----------------------------------------------------|----------|----------|
| `default_version` | Default version used when no tags exist            | No       | `v0.1.0` |
| `version_prefix`  | Prefix for version tags (e.g., `v` in `v1.0.0`)    | No       | `v`      |
| `tag_pattern`     | Pattern to match version tags                      | No       | `v*`     |

---

## Outputs

| Output            | Description                                      |
|--------------------|--------------------------------------------------|
| `next_version`     | The calculated next version                     |
| `current_version`  | Current version (latest tag or default)         |
| `commit_count`     | Number of commits since the last version tag    |

---

## Usage

Below is an example workflow that demonstrates how to use the `version_calculator` Action:

### Example Workflow

```yaml
name: Version Calculator Workflow

on:
  workflow_dispatch: # Allows manual triggering of the workflow

jobs:
  calculate-version:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history and tags for accurate versioning

      - name: Calculate next version
        id: version
        uses: deepworks-net/github.toolkit/actions/version_calculator@v1
        with:
          default_version: v0.1.0
          version_prefix: v
          tag_pattern: v*

      - name: Output version details
        run: |
          echo "Next version: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}"
          echo "Current version: ${% raw %}{{ steps.version.outputs.current_version }}{% endraw %}"
          echo "Commits since last tag: ${% raw %}{{ steps.version.outputs.commit_count }}{% endraw %}"
```

---

## How It Works

1. **Fetch Git History**:
    - Ensures all tags and commit history are fetched for accurate calculations.

2. **Retrieve Latest Tag**:
    - Finds the latest Git tag using the specified tag pattern.

3. **Calculate Next Version**:
    - Parses the latest tag and calculates the next patch version by incrementing the patch number based on the number of commits since the tag.

4. **Set Outputs**:
    - Outputs the next version, current version, and commit count for use in subsequent workflow steps.

---

## Implementation Details

### Script Details (`version_calculator.py`)

The core logic is implemented in a Python script. Key functions include:

- **`setup_git()`**: Configures Git to trust the workspace.
- **`get_latest_tag()`**: Retrieves the latest Git tag matching the specified pattern.
- **`calculate_next_version(latest_tag, version_prefix)`**:
    - Parses the tag to extract major, minor, and patch components.
    - Increments the patch number based on the commit count since the tag.
- **`get_commit_count_since_tag(tag)`**:
    - Counts commits made since the last tag.

### Action Metadata (`action.yml`)

The action is designed to run as a Docker container and provides customizable inputs for tag matching and version defaults.

---

## Notes

- Ensure the `fetch-depth` in the `actions/checkout` step is set to `0` to include all tags and commit history.
- The action relies on semantic versioning. Ensure your tags follow the expected pattern (e.g., `v1.2.3`).
- Outputs are set using the `::set-output` command for compatibility with GitHub Actions.
