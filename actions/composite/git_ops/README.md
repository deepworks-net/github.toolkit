# Git Operations Composite Action

This composite action provides modular, reusable Git operations for GitHub Actions workflows.

## Structure

The action is organized into specialized modules:

- **Branch Operations** - Creating, deleting, checkout, and listing branches
- **Commit Operations** - Creating commits, retrieving info, reverting, and listing commits
- **Tag Operations** - Creating, deleting, pushing, and listing tags

Each module can be used independently or together through the main git_ops.py interface.

## Usage

### As a Composite Action

```yaml
- name: Git Operations
  uses: actions/composite/git_ops@v1
  with:
    # Common parameters
    branch_name: 'feature/my-feature'
    commit_message: 'Update documentation'
    files: 'README.md docs/usage.md'
    create_pr: 'true'
    pr_title: 'Feature: Add new documentation'
    pr_body: 'This PR adds updated documentation.'
```

### Using Individual Modules

#### Branch Operations

```yaml
- name: Git Branch Operations
  uses: actions/composite/git_ops/branch@v1
  with:
    action: 'create'  # create/delete/checkout/list
    branch_name: 'feature/my-feature'
    start_point: 'main'  # Optional
```

#### Commit Operations

```yaml
- name: Git Commit Operations
  uses: actions/composite/git_ops/commit@v1
  with:
    action: 'create'  # create/info/revert/list
    message: 'Update documentation'
    files: 'README.md,docs/usage.md'  # Optional
    all: 'true'  # Optional, commit all changes
```

#### Tag Operations

```yaml
- name: Git Tag Operations
  uses: actions/composite/git_ops/tag@v1
  with:
    action: 'create'  # create/delete/push/list
    tag_name: 'v1.0.0'
    message: 'Release v1.0.0'  # Optional
    remote: 'true'  # Optional
```

## Development

Each module includes its own test suite (unit and integration tests).

Run tests:

```bash
cd actions/composite/git_ops/[module]
pip install -r requirements.txt -r requirements-dev.txt
pytest
```