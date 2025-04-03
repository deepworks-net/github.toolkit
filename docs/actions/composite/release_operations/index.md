# Release Operations Action

A composite action that combines tag, branch, and commit operations to streamline the release process.

## Overview

The Release Operations action orchestrates multiple atomic Git operations to provide a comprehensive and flexible release workflow. By combining the Core Tag Operations, Branch Operations, and Commit Operations actions, it simplifies complex release tasks into a single, configurable action.

## Features

- Create release branches
- Create and manage release tags
- Update changelogs
- Create GitHub releases
- Handle release assets
- Push changes to remote repository

## Usage

### Basic Release Creation

```yaml
- name: Create Release
  uses: ./actions/composite/release_operations
  with:
    action: create
    version: v1.0.0
    message: "Release v1.0.0"
```

### Full Release Workflow with Branch

```yaml
- name: Create Release
  id: release
  uses: ./actions/composite/release_operations
  with:
    action: create
    version: v1.0.0
    message: "Release v1.0.0"
    body: |
      ## What's New
      - Feature 1
      - Feature 2
      - Bug fix 1
    target_branch: main
    release_branch: release/1.0
    update_changelog: true
    draft: false
    prerelease: false
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `action` | Release operation (create, publish, update, delete) | Yes | |
| `version` | Version for the release (e.g., v1.0.0) | Yes | |
| `target_branch` | Target branch for the release | No | main |
| `release_branch` | Name of the release branch to create | No | |
| `message` | Release message | No | Release {version} |
| `body` | Release body content | No | |
| `draft` | Create as draft release | No | false |
| `prerelease` | Mark as prerelease | No | false |
| `update_changelog` | Whether to update the changelog | No | true |
| `tag_only` | Only create a tag, not a GitHub release | No | false |
| `files` | Files to include in the release (comma-separated) | No | |

## Outputs

| Name | Description |
|------|-------------|
| `release_id` | ID of the created or updated release |
| `tag_name` | Name of the created tag |
| `release_url` | URL of the created or updated release |
| `release_branch` | Name of the release branch (if created) |
| `result` | Operation result (success/failure) |

## Implementation Details

This composite action combines several atomic actions to provide a comprehensive release workflow:

1. **Actions/Checkout**: Ensures the repository is available with proper history
2. **Branch Operations**: Creates and manages release branches
3. **Tag Operations**: Creates and manages release tags
4. **Update Changelog**: Updates the changelog for the release
5. **Commit Operations**: Commits any changes to the changelog
6. **GitHub's Create Release**: Creates a GitHub release using the tag

The action follows a logical flow:

1. First, it creates a release branch if specified
2. Then, it creates a tag for the release
3. Next, it updates the changelog if requested
4. After that, it commits any changelog changes
5. Finally, it creates a GitHub release

## Examples

### Creating a Standard Release

```yaml
name: Create Release

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version number (e.g., v1.0.0)'
        required: true

jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Create Release
        id: release
        uses: ./actions/composite/release_operations
        with:
          action: create
          version: ${{ github.event.inputs.version }}
          message: "Release ${{ github.event.inputs.version }}"
          update_changelog: true
```

### Creating a Pre-release

```yaml
name: Create Pre-release

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version number (e.g., v1.0.0-beta)'
        required: true

jobs:
  create-prerelease:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Create Pre-release
        uses: ./actions/composite/release_operations
        with:
          action: create
          version: ${{ github.event.inputs.version }}
          message: "Pre-release ${{ github.event.inputs.version }}"
          prerelease: true
          update_changelog: false
```

### Tag Only (No GitHub Release)

```yaml
name: Create Release Tag

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version number (e.g., v1.0.0)'
        required: true

jobs:
  create-tag:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
          
      - name: Create Tag
        uses: ./actions/composite/release_operations
        with:
          action: create
          version: ${{ github.event.inputs.version }}
          tag_only: true
```

## Core/Composite Pattern

This action demonstrates the core/composite pattern by:

1. **Leveraging Atomic Operations**: Using core actions for specific Git operations
2. **Orchestrating Complex Workflows**: Combining multiple operations logically
3. **Simplifying Interfaces**: Providing a high-level interface for complex tasks
4. **Maintaining Flexibility**: Allowing configuration of each step in the process

This approach ensures that users can either use this high-level composite action for common release workflows or build their own workflows using the individual core actions as needed.