# Publish GitHub Release Workflow

This reusable workflow automatically creates and publishes GitHub Releases when version tags are pushed to the repository. It's designed to work in conjunction with the prepare-release and update-changelog workflows.

## Workflow File

`.github/workflows/release-drafter.yml`

## Trigger

The workflow can be triggered in two ways:

### 1. Tag Push

Automatically triggers when a tag matching the pattern `v*` is pushed to the repository. For example:

- v1.0.0
- v2.1.3
- v0.1.0

```yaml
on:
  push:
    tags:
      - 'v*'
```

### 2. Workflow Call

Can be called from another workflow using the `workflow_call` trigger.

## Input Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `tag-name` | Tag name for the release (e.g., v1.0.0) | No | Current tag |
| `draft` | Create as draft release | No | `false` |

## Secrets

| Secret | Description | Required | Default |
|--------|-------------|----------|---------|
| `token` | GitHub token for release creation | No | `GITHUB_TOKEN` |

## Usage

### As a Standalone Workflow

When a version tag is pushed, the workflow automatically:

1. Creates a new GitHub Release
2. Sets the release title and description
3. Publishes the release

### As a Reusable Workflow

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/release-drafter.yml@main
    with:
      tag-name: 'v1.0.0'
      draft: false
    secrets:
      token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
```

## Release Format

The workflow creates releases with:

1. Title based on the tag name
2. Standard header section
3. Link to changelog in footer
4. Content from the release draft

## Permissions

The workflow requires:

- `contents: write` permission to create releases
- GitHub token with appropriate permissions

## Integration with Other Workflows

This workflow is part of the release process that includes:

1. **Prepare Release Workflow**
   - Creates release branch
   - Updates changelog
   - Prepares release PR

2. **Update Changelog Workflow**
   - Maintains changelog during development
   - Tracks unreleased changes

3. **Release Drafter (This Workflow)**
   - Creates final release
   - Publishes to GitHub

## Release Process

1. Release preparation initiated (`prep-v*` tag)
2. Release branch created
3. Changelog updated
4. Release PR merged
5. Version tag pushed
6. Release published

## Troubleshooting

Common issues and solutions:

1. **Release Not Publishing**
   - Check tag format matches `v*` pattern
   - Verify workflow has write permissions
   - Check GitHub token permissions

2. **Missing Content**
   - Ensure changelog is properly formatted
   - Verify release draft exists
   - Check release-drafter configuration

3. **Permission Errors**
   - Check repository settings
   - Verify token permissions
   - Ensure workflow permissions are set

## Contributing

To modify this workflow:

1. Fork the repository
2. Edit `.github/workflows/release-drafter.yml`
3. Test changes by creating a release
4. Submit a pull request

## Configuration

release-drafter configuration options:

```yaml
publish: true
tag: ${tag name}
draft: false
header: |
  ## Release ${version}
footer: |
  See the [Changelog](link) for more details.
```

## Related Documentation

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [release-drafter action](https://github.com/release-drafter/release-drafter)
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)