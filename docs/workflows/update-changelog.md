# Update Changelog Workflow

This workflow automatically updates the repository's CHANGELOG.md file when pull requests are merged into the develop branch.

## Workflow File

`.github/workflows/update-changelog.yml`

## Trigger

The workflow is triggered when a pull request targeting the `develop` branch is closed:

```yaml
on:
  pull_request:
    branches:
      - develop
    types: [closed]
```

The workflow will only run if the pull request was actually merged, not just closed:

```yaml
jobs:
  update-changelog:
    if: github.event.pull_request.merged == true
```

## Changelog Format

The workflow expects and maintains a changelog in the following format:

```markdown
## **MM/DD/YYYY - Unreleased**
- PR #123: Description of change
- PR #124: Another change

## **MM/DD/YYYY - v1.0.0**
- Previous release changes...
```

## Process

The workflow performs the following steps:

1. Checks out the repository's develop branch
2. Processes the CHANGELOG.md file:
    - If an "Unreleased" section exists, adds the new PR entry to it
    - If no "Unreleased" section exists, creates one with today's date
3. Commits and pushes the updated changelog

### Entry Format

Each changelog entry follows the format:

```markdown
- PR #{number}: {pull request title}
```

## Usage

The workflow runs automatically when PRs are merged. No manual intervention is required.

### Prerequisites

1. Repository must have a `CHANGELOG.md` file in the root directory
2. The file should follow the expected format
3. PRs should be merged into the `develop` branch

### Pull Request Requirements

- PRs must target the `develop` branch
- PR title should be descriptive as it will be used in the changelog
- PR must be merged (not just closed)

## Examples

### PR Title Examples

Good PR titles that make meaningful changelog entries:
```
Add user authentication system
Fix memory leak in data processing
Update dependencies to latest versions
```

Poor PR titles to avoid:
```
Fix bug
Update code
WIP: Changes
```

### Changelog Entry Examples

The workflow will create entries like:
```markdown
## **01/02/2025 - Unreleased**
- PR #123: Add user authentication system
- PR #124: Fix memory leak in data processing
- PR #125: Update dependencies to latest versions
```

## Permissions

The workflow requires:
- Read access to pull request metadata
- Write access to the repository (for pushing changes)

It uses the `GITHUB_TOKEN` secret which is automatically provided by GitHub Actions.

## Error Handling

The workflow includes several safeguards:

1. Only runs on merged PRs
2. Creates "Unreleased" section if missing
3. Checks for changes before committing
4. Uses [skip ci] in commit message to prevent CI loops

## Troubleshooting

Common issues and solutions:

1. **Changelog Not Updated**
    - Verify PR was actually merged
    - Check if PR targeted develop branch
    - Verify CHANGELOG.md exists in root directory

2. **Push Failed**
    - Check if workflow has write permissions
    - Verify branch protections allow GitHub Actions to push

3. **Format Issues**
    - Ensure CHANGELOG.md follows expected format
    - Check for manual modifications that might break format

## Contributing

To modify this workflow:

1. Fork the repository
2. Edit `.github/workflows/update-changelog.yml`
3. Test changes by merging PRs to your fork
4. Submit a pull request

## Related Documentation

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git documentation](https://git-scm.com/doc)