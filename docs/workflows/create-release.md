# Create GitHub Release Workflow

This reusable workflow automatically creates a GitHub Release. It can be triggered either by pushing a version tag or by being called from another workflow.

## Workflow File

`.github/workflows/create-release.yml`

## Triggers

The workflow can be triggered in two ways:

### 1. Tag Push

Automatically triggers when a tag matching the pattern `v*` is pushed to the repository. This includes tags like:

- v1.0.0
- v2.1.3
- v0.1.0-beta

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
| `prerelease` | Whether this is a prerelease | No | `false` |
| `release-title` | Custom release title | No | Tag name |
| `draft` | Whether this is a draft release | No | `false` |

## Secrets

| Secret | Description | Required | Default |
|--------|-------------|----------|---------|
| `token` | GitHub token for release creation | No | `GITHUB_TOKEN` |

## Usage

### As a Standalone Workflow

1. Tag your commit:

   ```bash
   git tag v1.0.0
   ```

2. Push the tag:

   ```bash
   git push origin v1.0.0
   ```

### As a Reusable Workflow

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/create-release.yml@main
    with:
      prerelease: false
      release-title: "My Custom Release"
      draft: false
    secrets:
      token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
```

## Configuration Examples

### Standard Release

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/create-release.yml@main
```

### Draft Release

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/create-release.yml@main
    with:
      draft: true
      release-title: "Release Candidate v1.0.0"
```

### Prerelease

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/create-release.yml@main
    with:
      prerelease: true
      release-title: "Beta Release v0.9.0"
```

## Versioning

Follow semantic versioning for tags:

- Major releases: v1.0.0, v2.0.0
- Minor releases: v1.1.0, v1.2.0
- Patch releases: v1.0.1, v1.0.2

## Permissions

The workflow uses either:

- A provided GitHub token through secrets.token
- The default `GITHUB_TOKEN` secret automatically provided by GitHub Actions

Both tokens must have permissions to create releases in the repository.

## Troubleshooting

Common issues and solutions:

1. **Workflow not triggering on tag push**
   - Ensure tag matches the `v*` pattern
   - Verify tag was pushed to the repository

2. **Workflow call failures**
   - Check input parameter types match expected values
   - Verify secret availability and permissions

3. **Permission errors**
   - Check repository settings allow GitHub Actions
   - Verify workflow has access to required token
   - Ensure token has release creation permissions

## Contributing

To modify this workflow:

1. Fork the repository
2. Edit `.github/workflows/create-release.yml`
3. Submit a pull request

## Related Documentation

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [automatic-releases action](https://github.com/marvinpinto/action-automatic-releases)
- [Semantic Versioning](https://semver.org/)