# Release Drafter Workflow

This workflow automates the creation and management of GitHub Releases. It maintains a draft release that updates automatically with new changes and publishes final releases when version tags are pushed.

## Workflow File

`.github/workflows/release-drafter.yml`

## Triggers

The workflow responds to three types of events:

1. **Push to develop branch**:
   - Updates the draft release
   - Calculates next version based on commit count
   - Updates release notes

2. **Push of version tags** (`v*`):
   - Publishes the final release
   - Uses the tag's version number
   - Finalizes release notes

3. **Workflow call**:
   - Allows other workflows to trigger release operations
   - Supports custom tag names and options

## Version Calculation

The workflow automatically calculates the next version number based on:

- Latest version tag (vX.Y.Z format)
- Number of commits since that tag
- Semantic versioning principles

Example:

- Current version: v1.0.16
- 3 new commits
- Next calculated version: v1.0.19

## Jobs

### 1. Update Release Draft

Runs when changes are pushed to develop:

```yaml
jobs:
  update_release_draft:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
```

Steps:

1. Checkout repository with full history
2. Calculate next version based on commit count
3. Update draft release with new version and changes

### 2. Publish Release

Runs when a version tag is pushed:

```yaml
jobs:
  publish_release:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
```

Steps:

1. Checkout repository
2. Publish final release with tag version
3. Update release notes

## Input Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `tag-name` | Release tag name | No | Current tag |
| `draft` | Create as draft | No | `false` |

## Secrets

| Secret | Description | Required | Default |
|--------|-------------|----------|---------|
| `token` | GitHub token | No | `GITHUB_TOKEN` |

## Release Format

### Draft Release

```markdown
## Draft Release v1.0.X

[Automatically populated release notes]

See the [Changelog](link) for more details.
```

### Final Release

```markdown
## Release v1.0.X

[Release notes from draft]

See the [Changelog](link) for more details.
```

## Integration

This workflow integrates with:

- Changelog updates
- Release preparation
- Version tagging

## Configuration

The workflow uses release-drafter configuration from `.github/release-drafter.yml` for:

- Change categorization
- Note formatting
- Version resolution

## Permissions

Required permissions:

```yaml
permissions:
  contents: write
```

## Usage Examples

### As Part of Release Process

1. Push changes to develop:
   - Updates draft release
   - Increments version number
   - Updates release notes

2. Create version tag:

   ```bash
   git tag v1.0.x
   git push origin v1.0.x
   ```

   - Publishes final release
   - Uses tag version
   - Finalizes release notes

### Called from Another Workflow

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/release-drafter.yml@main
    with:
      tag-name: 'v1.0.0'
```

## Troubleshooting

Common issues and solutions:

1. **Version Calculation Fails**
   - Ensure repository has at least one version tag
   - Check tag format matches `vX.Y.Z`
   - Verify git history is available (fetch-depth: 0)

2. **Draft Not Updating**
   - Check branch name matches 'develop'
   - Verify workflow has write permissions
   - Check release-drafter configuration

3. **Release Not Publishing**
   - Verify tag format matches `v*`
   - Check GitHub token permissions
   - Review release-drafter logs

## Related Documentation

- [release-drafter action](https://github.com/release-drafter/release-drafter)
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)