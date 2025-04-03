# Release Operations Action

A composite action that combines tag, branch, and commit operations to streamline the release process.

## Overview

This action wraps multiple atomic Git operations to provide a comprehensive release workflow, including:

- Creating release branches
- Creating and managing release tags
- Updating changelogs
- Creating GitHub releases
- Handling release assets

## Features

- Create complete releases with a single action
- Flexible configuration options for different release workflows
- Automatic changelog updates
- Support for drafts and prereleases
- Integration with GitHub Releases

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

- name: Display Release URL
  run: echo "Release URL ${{ steps.release.outputs.release_url }}"
```

### Tag Only (No GitHub Release)

```yaml
- name: Create Tag Only
  uses: ./actions/composite/release_operations
  with:
    action: create
    version: v1.0.0
    tag_only: true
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

## Behavior Matrix

| Action | Inputs | Behavior |
|--------|--------|----------|
| create | version, message | Creates a tag and GitHub release |
| create | version, message, release_branch | Creates release branch, tag, and GitHub release |
| create | version, message, update_changelog=true | Updates changelog, creates tag and GitHub release |
| create | version, tag_only=true | Creates a tag only (no GitHub release) |
| publish | version, draft=false | Publishes an existing draft release |
| update | version, body | Updates the body of an existing release |
| delete | version | Deletes a release and its associated tag |

## Implementation

This action is a composite action that implements a resonance-based modular architecture, combining the following actions through lateral relationships:

- **Core Actions** (Atomic operations):
  - `actions/core/branch_operations` - Manages Git branch creation and manipulation
  - `actions/core/tag_operations` - Handles Git tag creation and management
  - `actions/core/commit_operations` - Manages Git commit operations

- **Composite Actions** (Combined operations):
  - `actions/composite/update_changelog` - Updates the CHANGELOG.md file

All components maintain peer-to-peer relationships rather than hierarchical dependencies, promoting a more flexible and maintainable codebase.

## Examples

### Creating a Release with Changelog Update

```yaml
name: Create Release

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version number (e.g., v1.0.0)'
        required: true
      release_type:
        description: 'Release type'
        required: true
        default: 'full'
        type: choice
        options:
          - full
          - draft
          - prerelease
          - tag-only

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
          draft: ${{ github.event.inputs.release_type == 'draft' }}
          prerelease: ${{ github.event.inputs.release_type == 'prerelease' }}
          tag_only: ${{ github.event.inputs.release_type == 'tag-only' }}
          
      - name: Display Release URL
        if: ${{ github.event.inputs.release_type != 'tag-only' }}
        run: echo "Release created at ${{ steps.release.outputs.release_url }}"
```

### Creating a Hotfix Release

```yaml
name: Create Hotfix Release

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Hotfix version (e.g., v1.0.1)'
        required: true
      base_version:
        description: 'Base version to branch from (e.g., v1.0.0)'
        required: true

jobs:
  create-hotfix:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Create Hotfix Release
        uses: ./actions/composite/release_operations
        with:
          action: create
          version: ${{ github.event.inputs.version }}
          message: "Hotfix ${{ github.event.inputs.version }}"
          target_branch: ${{ github.event.inputs.base_version }}
          release_branch: hotfix/${{ github.event.inputs.version }}
          update_changelog: true
```