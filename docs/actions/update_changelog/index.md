# Changelog Update Action

Synchronizes the repository's `CHANGELOG.md` with content from the draft release, ensuring an "Unreleased" section reflects all recent changes and maintains consistent formatting.

---

## Usage

```yaml
steps:
  - name: Update Changelog
    uses: ./actions/changelog_update
    with:
      github-token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
      version: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}
```

---

## Inputs

| Input           | Description                                 | Required | Default |
|------------------|---------------------------------------------|----------|---------|
| `github-token`  | GitHub token for API access                 | Yes      | N/A     |
| `version`       | Version number to use in the unreleased section | Yes      | N/A     |

---

## Functionality

### Draft Release Content

This action retrieves draft release details via the GitHub API:

1. Identifies the draft release.
2. Extracts PR entries.
3. Strips footer content.

### Changelog Format

Follows a consistent structure:

```markdown
# Repository Changelog

## **MM/DD/YYYY - vX.Y.Z Unreleased**
- PR #123: Feature description
- PR #124: Another change

## **[(MM/DD/YYYY) - vX.Y.Z](link-to-release)**
- Previous release content
```

### Processing Steps

1. Fetches draft release content.
2. Updates or creates the "Unreleased" section with:
   - Current date
   - Provided version number
   - Draft release content.
3. Preserves all previous releases.
4. Maintains formatting consistency.

---

## Implementation Details

### Environment Setup

- Configures Git in container environments.
- Installs required tools (e.g., GitHub CLI).
- Prepares workspace access.

### Git Operations

Handles:

- Git configuration.
- Committing changes.
- Pushing to a staging branch.

### Error Handling

Provides clear feedback for:

1. Missing GitHub token.
2. API request failures.
3. File operation issues.
4. Git command failures.

---

## Example Workflows

### Basic Usage with Version Calculation

```yaml
jobs:
  update-changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: staging
          fetch-depth: 0

      - name: Calculate Version
        uses: ./actions/version_calculation
        id: version

      - name: Update Changelog
        uses: ./actions/changelog_update
        with:
          github-token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
          version: ${% raw %}{{ steps.version.outputs.next_version }}{% endraw %}
```

### Manual Version Specification

```yaml
steps:
  - name: Update Changelog
    uses: ./actions/changelog_update
    with:
      github-token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
      version: 'v1.0.0'
```

---

## Requirements

1. Repository must include:
    - `CHANGELOG.md` in the root directory.
    - Draft release for content sourcing.
    - Proper GitHub token permissions.

2. Environment must have:
    - Git.
    - GitHub CLI.
    - Python 3.9+.

---

## Files

### `action.yml`

Defines the action interface:

- Input parameters.
- Environment configuration.
- Docker container setup.

### `Dockerfile`

Configures the container with:

- Python runtime.
- Git installation.
- GitHub CLI.
- Necessary environment setups.

### `update_changelog.py`

Implements core logic:

- Fetches draft release content.
- Parses and updates the changelog.
- Manages Git operations.
- Handles errors.

---

## Error Cases

The action accounts for several potential issues:

1. **Missing Draft Release**
    - Outputs a clear error message.
    - Returns a non-zero exit code.

2. **GitHub API Issues**
    - Validates tokens.
    - Handles request failures or permission errors.

3. **File Operations**
    - Detects missing changelog.
    - Handles write permissions or format inconsistencies.

4. **Git Operations**
    - Resolves configuration or push errors.
    - Handles permission issues.

---

## Future Improvements

Possible enhancements:

1. Support custom changelog formats.
2. Handle multiple changelog files.
3. Categorize release notes.
4. Automate version bumping.
5. Customize commit messages.

---

## Integration Points

Designed to integrate with:

- Version calculation actions.
- Release preparation workflows.
- GitHub release drafts.
- Branch protection rules.

---

## Contributing

To contribute:

1. Update the Python script for logic changes.
2. Test with various changelog states.
3. Verify formatting consistency.
4. Submit a PR for review.
