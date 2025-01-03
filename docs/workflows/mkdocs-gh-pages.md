# MkDocs GitHub Pages Workflow

This reusable workflow automates the process of building and deploying MkDocs documentation to GitHub Pages. It can be used in any repository that uses MkDocs for documentation.

## Workflow File

`.github/workflows/mkdocs-gh-pages.yml`

## Usage

### Basic Usage

To use this workflow in your repository, create a workflow file with the following content:

```yaml
name: Deploy Documentation
on:
  push:
    branches:
      - main

jobs:
  deploy-docs:
    uses: deepworks-net/github.actions/.github/workflows/mkdocs-gh-pages.yml@main
```

### Advanced Usage

You can customize the workflow behavior using input parameters:

```yaml
name: Deploy Documentation
on:
  push:
    branches:
      - main

jobs:
  deploy-docs:
    uses: deepworks-net/github.actions/.github/workflows/mkdocs-gh-pages.yml@main
    with:
      python-version: '3.11'
      requirements-file: 'docs/requirements.txt'
      readme-source: 'docs/README'
      readme-destination: 'docs/repo/inc/README.md'
      changelog-source: 'CHANGELOG'
      changelog-destination: 'docs/repo/inc/CHANGELOG.md'
      license-source: 'LICENSE'
      license-destination: 'docs/repo/inc/LICENSE.md'
```

## Input Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `python-version` | Python version to use for the build | No | `3.x` |
| `requirements-file` | Path to the requirements.txt file | No | `requirements.txt` |
| `readme-source` | Source path for README | No | `README` |
| `readme-destination` | Destination path for README | No | `docs/repo/inc/README.md` |
| `changelog-source` | Source path for CHANGELOG | No | `CHANGELOG` |
| `changelog-destination` | Destination path for CHANGELOG | No | `docs/repo/inc/CHANGELOG.md` |
| `license-source` | Source path for LICENSE | No | `LICENSE` |
| `license-destination` | Destination path for LICENSE | No | `docs/repo/inc/LICENSE.md` |

## Workflow Details

The workflow performs the following steps:

1. Checks out the repository with submodules
2. Sets up Python environment
3. Installs dependencies from requirements.txt
4. Copies README to docs directory
5. Builds and deploys MkDocs to GitHub Pages

## Requirements

To use this workflow, your repository needs:

1. MkDocs configuration file (`mkdocs.yml`)
2. Python dependencies file (`requirements.txt`) including MkDocs and any required theme/plugins
3. GitHub Pages enabled in repository settings
4. Proper permissions for GitHub Actions

## Example requirements.txt

```txt
mkdocs>=1.6.1
mkdocs-material>=9.5.49
```

## Troubleshooting

### Common Issues

1. **Build Fails**: Ensure all required dependencies are listed in requirements.txt
2. **Deploy Fails**: Check GitHub Pages settings in repository
3. **Missing README**: Verify README.md exists at specified source path

### Workflow Logs

To check workflow execution logs:

1. Go to Actions tab in your repository
2. Click on the workflow run
3. Expand the deploy job to see detailed logs

## Security Considerations

- The workflow runs with repository contents and GitHub token permissions
- No additional secrets are required for basic usage
- Ensure sensitive information is not exposed in documentation

## Contributing

Found a bug or have a suggestion? Please open an issue in the [deepworks-net/github.actions](https://github.com/deepworks-net/github.actions) repository.