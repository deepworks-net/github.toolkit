# GitHub Actions Collection

A collection of reusable GitHub Actions workflows and core actions for standardizing development processes across repositories.

## Available Components

### Core Actions

Atomic operations that can be combined to build custom workflows:

- **Version Calculator**: Calculate version numbers based on git tags
- **Version Updater**: Update version references in code and documentation
- **Branch Operations**: Create, delete, checkout, list, and merge branches
- **Tag Operations**: Create, delete, push, and list git tags
- **Commit Operations**: Create, amend, list, cherry-pick and revert git commits

### Composite Actions

Workflows that combine multiple operations for common tasks:

- **Git Operations**: Handle git operations including branch and tag management
- **Release Notes**: Generate release notes from PRs and commits
- **Update Changelog**: Update changelog based on merged PRs
- **Release Operations**: Combine tag, branch, and commit operations for comprehensive release management

### Workflows

Ready-to-use GitHub workflows for common development processes:

#### 1. Prepare Release Branch (`prep-release.yml`)

Creates a release branch and prepares the changelog for release.

**Trigger:**  
Push the tag `prep`

**Actions:**

- Creates a release branch
- Moves Unreleased changelog items to a new version section
- Removes the Unreleased section for release
- Creates a PR for review

**Usage:**

```bash
git tag prep
git push origin prep
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
2. For core actions, reference them in your workflows using the `uses` syntax
3. No additional configuration needed - workflows use repository context for variables

## Requirements

- GitHub repository with develop branch
- Permissions to push tags and create PRs
- Changelog.md file in repository root (will be created if missing)

## Contributing

1. Create a feature branch off develop
2. Make your changes
3. Create a PR to develop
4. Changelog will be automatically updated upon merge

## Documentation

See the [documentation site](https://deepworks-net.github.io/github.toolkit/) for detailed usage examples and API references for all actions and workflows.

## License

MIT License - See [LICENSE.md](https://github.com/deepworks-net/github.actions/blob/main/LICENSE.md) file for details