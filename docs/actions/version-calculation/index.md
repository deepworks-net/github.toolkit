
# Version Calculation Action

This action calculates the next version number based on Git tags and commit history, adhering to semantic versioning. The patch number reflects the count of commits since the last release.

## Usage

```yaml
steps:
  - name: Calculate Version
    uses: ./actions/version_calculation
    id: version
```

---

## Outputs

| Output         | Description                           |
|----------------|---------------------------------------|
| `next_version` | Calculated next version (e.g., v1.0.34) |

---

## How It Works

1. **Finds Latest Tag**: Locates the latest Git tag (`vMAJOR.MINOR.PATCH`).
2. **Counts Commits**: Determines the number of commits since the tag.
3. **Increments Patch**: Updates the patch number by the commit count.
4. **Outputs Version**: Returns the calculated version.

**Example**:

- Latest tag: `v1.0.16`
- Commits since tag: `3`
- Calculated version: `v1.0.19`

---

## Details

### Version Format

- Semantic versioning (`vMAJOR.MINOR.PATCH`)
- **Major** and **Minor** remain unchanged.
- **Patch** = Previous patch + Commit count.

### Git Configuration

- Configures Git safe directory settings.
- Ensures repository access in container environments.

### Error Handling

- Validates tag format.
- Handles cases with no existing tags.
- Provides clear error messages for failures.

---

## Example Workflows

### Prepare Release Workflow

```yaml
jobs:
  create-release-branch:
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Calculate Version
        uses: ./actions/version_calculation
        id: version

      - name: Use Version
        run: echo "Next version will be ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}"
```

### Release Drafter

```yaml
jobs:
  update_release_draft:
    steps:
      - name: Calculate Version
        uses: ./actions/version_calculation
        id: version

      - uses: release-drafter/release-drafter@v6
        with:
          version: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}
```

---

## Files

### action.yml

```yaml
name: "Version Calculation"
description: "Calculate the next version based on the latest Git tag."
outputs:
  next_version:
    description: "The calculated next version."
runs:
  using: "docker"
  image: "Dockerfile"
```

### version_calculation.py

- Configures Git environment.
- Retrieves the latest tag.
- Calculates the next version.
- Sets output for GitHub Actions.

---

## Requirements

1. Repository must use semantic versioning tags (`v*.*.*`).
2. Full Git history must be available (`fetch-depth: 0`).
3. Git must be installed in the environment.

---

## Error Cases

The action fails with clear error messages if:

1. No version tags exist.
2. Invalid tag format is found.
3. Git commands fail.
4. Repository access issues occur.

---

## Contributing

To modify this action:

1. Update the Python script for logic changes.
2. Test with various repository states.
3. Update documentation for any changes.
4. Submit a PR for review.

---

## Future Improvements

Potential enhancements:

1. Support custom version formats.
2. Allow configuration for version calculation rules.
3. Support alternative versioning schemes.
4. Output additional version metadata.
