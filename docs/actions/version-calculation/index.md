# Version Calculation Action

This reusable action calculates the next version number based on Git tags and commit history. It follows semantic versioning principles where the patch number represents the number of commits since the last release.

## Usage

```yaml
steps:
  - name: Calculate Version
    uses: ./actions/version_calculation
    id: version
```

## Outputs

| Output | Description |
|--------|-------------|
| `next_version` | The calculated next version (e.g., v1.0.34) |

## How It Works

1. Finds the latest version tag (format: v*.*.*) in the repository
2. Counts commits since that tag
3. Increments the patch number by the commit count
4. Outputs the new version number

For example:

- Latest tag: v1.0.16
- 3 commits since tag
- Calculated version: v1.0.19

## Implementation Details

### Version Format

- Follows semantic versioning (vMAJOR.MINOR.PATCH)
- Major and Minor versions stay the same
- Patch version = previous patch + commit count

### Git Configuration

- Automatically configures Git safe directory settings
- Handles repository access in container environments

### Error Handling

- Validates tag format
- Handles cases with no existing tags
- Reports clear error messages

## Example Workflows

### In Prepare Release Workflow

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

### In Release Drafter

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

Core script that:

- Configures Git environment
- Retrieves latest tag
- Calculates next version
- Sets output for GitHub Actions

## Requirements

1. Repository must use semantic versioning tags (v*.*.*)
2. Full Git history must be available (use `fetch-depth: 0` with checkout)
3. Git must be installed in the environment

## Error Cases

The action will fail with clear error messages if:

1. No version tags exist
2. Invalid tag format found
3. Git commands fail
4. Repository access issues occur

## Contributing

To modify this action:

1. Update Python script for logic changes
2. Test with various repository states
3. Update documentation for any changes
4. Submit PR for review

## Future Improvements

Potential enhancements:

1. Support for custom version formats
2. Configuration for version calculation rules
3. Support for other versioning schemes
4. Additional version metadata output