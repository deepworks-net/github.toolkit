# Core Action: Manage Release

## Overview

The Manage Release action provides a standardized interface for working with GitHub draft releases. It supports three main operations:

1. Creating/ensuring a draft release exists
2. Getting current draft release information
3. Updating draft release content

## Usage

### Draft Operation

Creates a new draft release or returns existing one:

```yaml
- name: Create Draft Release
  uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
  with:
    github-token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
    operation: 'draft'
    name: 'Release v1.0.0'
    body: 'Initial release notes'
```

### Get Operation

Retrieves current draft release information:

```yaml
- name: Get Draft Release
  uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
  with:
    github-token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
    operation: 'get'
```

### Update Operation

Updates draft release content with different modes:

```yaml
- name: Update Draft Release
  uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
  with:
    github-token: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
    operation: 'update'
    content: 'New content to add'
    update_mode: 'append'  # or 'replace', 'prepend'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | GitHub token for API access | Yes | - |
| `operation` | Operation to perform (draft, get, update) | No | `get` |
| `name` | Release name for draft operation | No | `Draft Release` |
| `body` | Initial release body for draft operation | No | `''` |
| `content` | Content for update operation | No* | - |
| `update_mode` | How to update content (replace, append, prepend) | No | `replace` |

*Required for update operation

## Outputs

| Output | Description |
|--------|-------------|
| `id` | Release ID |
| `body` | Release content |
| `tag_name` | Release tag name |
| `name` | Release name |
| `exists` | Whether draft release exists (true/false) |

## Behavior

### Draft Operation

1. Checks for existing draft release
2. If none exists, creates new draft
3. Returns release information

### Get Operation

1. Fetches current draft release
2. Returns release information if exists
3. Indicates if no draft exists

### Update Operation

1. Gets current draft release
2. Updates content based on mode:
    - `replace`: Overwrites existing content
    - `append`: Adds to end of content
    - `prepend`: Adds to beginning of content
3. Returns updated release information

## Error Handling

The action handles several error cases:

1. **Invalid Operation**
    - Unsupported operation specified
    - Missing required inputs for operation

2. **GitHub API Errors**
    - Authentication failures
    - Rate limiting
    - Network issues

3. **Content Errors**
    - Missing content for update
    - Invalid update mode
    - Release not found for update

## Example Use Cases

### Release Preparation

```yaml
jobs:
  prepare:
    steps:
      - name: Create Draft
        uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
        with:
          operation: 'draft'
          name: 'Release v1.0.0'
```

### PR Merge Updates

```yaml
on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  update-notes:
    if: github.event.pull_request.merged == true
    steps:
      - name: Update Release Notes
        uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
        with:
          operation: 'update'
          content: |
            - PR #${% raw %}{{ github.event.pull_request.number }}{% endraw %}: ${% raw %}{{ github.event.pull_request.title }}{% endraw %}
          update_mode: 'append'
```

### Release Status Check

```yaml
jobs:
  check:
    steps:
      - name: Check Draft Release
        id: release
        uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
        
      - name: Create if Missing
        if: steps.release.outputs.exists == 'false'
        uses: deepworks-net/github.toolkit/actions/core/manage_release@v1
        with:
          operation: 'draft'
```

## Implementation

### Core Files

- `main.py`: Release management logic
- `action.yml`: Action metadata
- `Dockerfile`: Container configuration

### Dependencies

- Python 3.9
- Git
- curl
- GitHub API access
