# GitHub Actions Collection

A collection of reusable GitHub Actions workflows for standardizing development processes across repositories.

## Available Workflows

### Release Management

Two workflows that work together to manage the release process:

#### 1. Prepare Release Branch (`prep-release.yml`)
Creates a release branch and prepares the changelog for release.

**Trigger:**  
Push a tag with prefix `prep-v` (e.g., `prep-v1.0.0`)

**Actions:**
- Creates a release branch
- Moves Unreleased changelog items to a new version section
- Removes the Unreleased section for release
- Creates a PR for review

**Usage:**
```bash
git tag prep-v1.0.0
git push origin prep-v1.0.0
```

#### 2. Update Changelog (`update-changelog.yml`)
Automatically updates the changelog when PRs are merged to develop.

**Trigger:**  
PR merged to develop branch

**Actions:**
- Adds PR to Unreleased section of changelog
- Creates Unreleased section if it doesn't exist
- Maintains changelog formatting

**Usage:**
Automatic - no manual steps required. PR merges to develop trigger the workflow.

## Changelog Format

The workflows maintain the following changelog format:

```markdown
# Repository Changelog
*Note: the changes in this log are automatically generated and commited via github actions, modify only if you know what you are doing!*

## **MM/DD/YYYY - Unreleased**
- PR #{number}: {title}

## **[(MM/DD/YYYY) - {version}](https://github.com/{org}/{repo}/releases/tag/{version})**
- PR #{number}: {title}
```

## Setup Instructions

1. Copy the desired workflow files to your repository's `.github/workflows/` directory
2. No additional configuration needed - workflows use repository context for variables

## Requirements

- GitHub repository with develop branch
- Permissions to push tags and create PRs
- Changelog.md file in repository root (will be created if missing)

## Contributing

1. Create a feature branch off develop
2. Make your changes
3. Create a PR to develop
4. Changelog will be automatically updated upon merge

## Support

For issues, questions, or contributions:
1. Open an issue in this repository
2. Include workflow name and description of need

## License

MIT License - See [LICENSE.md](LICENSE.md) file for details