# Deepworks Core GitHub Repository

This repository contains a collection of reusable GitHub Actions workflows. These workflows are designed to standardize common CI/CD tasks across Deepworks repositories.

## Available Workflows

### MkDocs GitHub Pages Workflow
**[View Documentation](workflows/mkdocs-gh-pages.md)**

Automates the deployment of MkDocs documentation to GitHub Pages. This workflow:
- Copies repository files (README, CHANGELOG, LICENSE) to documentation
- Updates MkDocs navigation configuration
- Deploys to GitHub Pages
- Supports custom Python versions and file locations

### Create GitHub Release
**[View Documentation](workflows/create-release.md)**

Automates the creation of GitHub releases. This workflow:
- Creates releases from version tags
- Supports prereleases and draft releases
- Allows custom release titles
- Can be triggered manually or by tags

### Update Changelog
**[View Documentation](workflows/update-changelog.md)**

Automatically updates CHANGELOG.md when pull requests are merged. This workflow:

- Adds PR information to changelog
- Manages unreleased section
- Maintains consistent changelog format
- Runs on PR merge to develop branch

## Using These Workflows

To use these workflows in your repository:

1. Reference them in your workflow files:

    ```yaml
    jobs:
    docs:
        uses: deepworks-net/github.actions/.github/workflows/mkdocs-gh-pages.yml@main
    ```

2. Configure with input parameters:

    ```yaml
    with:
    parameter: value
    ```

3. Provide any required secrets:

    ```yaml
    secrets:
    token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
    ```

## Best Practices

When using these workflows:

1. Always reference a specific tag/SHA instead of `main` for production use
2. Test workflow changes in a feature branch first
3. Monitor workflow runs for any issues
4. Keep repository settings up to date with required permissions

## Need Help?

- Check individual workflow documentation for detailed configuration options
- Review workflow run logs for troubleshooting
- Open an issue if you encounter any problems
- Submit pull requests for improvements

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See our [Contributing Guidelines](../CONTRIBUTING.md) for more information.