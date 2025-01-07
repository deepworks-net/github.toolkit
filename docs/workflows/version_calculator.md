# Version Calculator Workflow Documentation

This workflow demonstrates how to calculate the next version of your repository using the `version_calculator` GitHub Action. The workflow supports manual triggering and can be integrated into your repository for version management.

---

## Workflow Overview

The workflow uses the following key features:

- **Manual Triggering**: Can be initiated on demand via the `workflow_dispatch` event.
- **Dynamic Inputs**: Accepts customizable inputs for default version, version prefix, and tag patterns.
- **Semantic Version Calculation**: Automatically calculates the next version based on the latest Git tag and the number of commits since the tag.

---

## Workflow File

```yaml
name: Version Calculator Workflow

on:
  workflow_dispatch:  # Allows manual triggering of the workflow

  workflow_call:  # Supports invocation by other workflows
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
          fetch-depth: 0  # Fetch all history and tags for accurate versioning

      - name: Calculate next version
        id: version
        uses: deepworks-net/github.toolkit/actions/version_calculator@v1
        with:
          default_version: ${% raw %}{{ inputs.default_version }}{% endraw %}
          version_prefix: ${% raw %}{{ inputs.version_prefix }}{% endraw %}
          tag_pattern: ${% raw %}{{ inputs.tag_pattern }}{% endraw %}
```

---

## Inputs

| Input            | Description                                         | Required | Default  |
|-------------------|-----------------------------------------------------|----------|----------|
| `default_version` | Default version to use when no tags exist           | No       | `v0.1.0` |
| `version_prefix`  | Prefix for version tags (e.g., `v` in `v1.0.0`)     | No       | `v`      |
| `tag_pattern`     | Pattern to match version tags                      | No       | `v*`     |

---

## Outputs

| Output            | Description                                      |
|--------------------|--------------------------------------------------|
| `next_version`     | The calculated next version                     |
| `current_version`  | Current version (latest tag or default)         |
| `commit_count`     | Number of commits since the last version tag    |

---

## Workflow Details

1. **Triggering**:
    - This workflow can be triggered manually or called by other workflows using the `workflow_call` event.

2. **Checkout Code**:
    - Ensures the repository is fully checked out, including all commit history and tags (`fetch-depth: 0`).

3. **Version Calculation**:
    - The `version_calculator` action calculates the next version based on the latest Git tag and commit history.

4. **Outputs**:
    - Provides calculated `next_version`, `current_version`, and `commit_count` as workflow outputs for further use.

---

## Notes

- **Ensure Tag Availability**: This workflow assumes that version tags are present in the repository. If no tags exist, the `default_version` input is used.
- **Semantic Versioning**: Tags should follow a semantic versioning format (e.g., `v1.2.3`).
- **Custom Prefixes**: Use the `version_prefix` input to support custom tag prefixes.
