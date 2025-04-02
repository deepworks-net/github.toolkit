# Branch Operations Action

This action provides a robust interface for working with Git branches in GitHub Actions workflows.

## Features

- Create new branches
- Delete branches (locally and remotely)
- Checkout branches
- Merge branches
- List branches (with pattern filtering)
- Push branches to remote

## Usage

### Basic Example

```yaml
- name: Create Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@main
  with:
    action: create
    branch_name: feature/my-feature
    base_branch: develop
```

### Input Parameters

| Parameter    | Description                                             | Required | Default |
|-------------|---------------------------------------------------------|----------|---------|
| `action`    | Branch operation (create, delete, list, checkout, merge) | Yes      | N/A     |
| `branch_name` | Name of the branch to operate on                        | No*      | N/A     |
| `base_branch` | Base branch for creating or merging                     | No       | main    |
| `force`     | Force operation (delete, checkout, merge)                | No       | false   |
| `message`   | Commit message for merge operations                      | No       | N/A     |
| `pattern`   | Pattern for listing branches (e.g. "feature/*")          | No       | N/A     |
| `remote`    | Include remote operations                                | No       | false   |

*Required for all actions except 'list'

### Outputs

| Output           | Description                                    |
|------------------|------------------------------------------------|
| `branches`      | Comma-separated list of branches (list action) |
| `result`        | Operation result (success/failure)             |
| `current_branch` | Current branch after operation                |

## Examples

### Create and Push Feature Branch

```yaml
- name: Create Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@main
  with:
    action: create
    branch_name: feature/my-feature
    base_branch: develop
    remote: true
```

### List Feature Branches

```yaml
- name: List Feature Branches
  id: list-branches
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@main
  with:
    action: list
    pattern: 'feature/*'

- name: Show Branches
  run: echo "Found branches: ${{ steps.list-branches.outputs.branches }}"
```

### Merge and Delete Branch

```yaml
- name: Merge Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@main
  with:
    action: merge
    branch_name: feature/completed-feature
    base_branch: main
    message: "Merge feature branch into main"

- name: Delete Feature Branch
  uses: deepworks-net/github.toolkit/actions/core/branch_operations@main
  with:
    action: delete
    branch_name: feature/completed-feature
    remote: true
```

## Development

This action follows the core actions pattern in the GitHub toolkit repository.

### Testing

Run the tests with:

```bash
pytest
```

Or run specific test categories:

```bash
pytest -m unit
pytest -m integration
```