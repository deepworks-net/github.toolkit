# Core Action: Manage Release

## Overview

The Manage Release action handles draft release content management in GitHub repositories. It supports two modes of operation:

1. PR Merge: Adds PR information to draft release notes
2. Prepare Release: Prepares draft content for final release

## Usage

### PR Merge Mode

```yaml
- name: Update Release Notes
  uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    mode: 'pr-merge'
    pr-number: '123'
    pr-title: 'Feature: Add new functionality'

### Prepare Release Mode
- name: Prepare Release Notes
  uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    mode: 'prepare-release'
    version: 'v1.0.0'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | GitHub token for API access | Yes | - |
| `mode` | Operation mode (pr-merge, prepare-release) | Yes | - |
| `pr-number` | PR number for pr-merge mode | No* | - |
| `pr-title` | PR title for pr-merge mode | No* | - |
| `version` | Version for prepare-release mode | No* | - |

*Required based on mode

## Outputs

| Output | Description |
|--------|-------------|
| `content` | The updated release notes content |

## Behavior

### PR Merge Mode

1. Gets current draft release
2. Adds PR information to notes
3. Updates draft release

### Prepare Release Mode

1. Gets current draft release
2. Prepares content for release
3. Updates draft release

## Error Handling

The action handles several error cases:

1. Invalid mode
2. Missing required inputs
3. GitHub API errors
4. Draft release not found

## Implementation

### Core Files

- `main.py`: Release management logic
- `action.yml`: Action metadata
- `Dockerfile`: Container configuration

### Dependencies

- Python 3.9
- Git
- GitHub API access

## Example Use Cases

### Update Release Notes on PR Merge

```yaml
on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  update-notes:
    if: github.event.pull_request.merged == true
    uses: ./.github/workflows/core.action.manage_release.yml
    with:
      mode: 'pr-merge'
      pr-number: ${{ github.event.pull_request.number }}
      pr-title: ${{ github.event.pull_request.title }}
```

### Prepare Release Notes

```yaml
jobs:
  prepare:
    uses: ./.github/workflows/core.action.manage_release.yml
    with:
      mode: 'prepare-release'
      version: 'v1.0.0'
```
