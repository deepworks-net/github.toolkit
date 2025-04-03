# Commit Operations Action

A self-contained action that provides atomic git commit operations.

## Overview

The Commit Operations action handles Git commit-related operations in a standardized way, ensuring proper error handling and consistent output. It uses the shared Git utilities for common Git operations, providing a reliable interface for working with commits in GitHub Actions workflows.

## Features

- Create new commits with various options
- Amend existing commits with new changes or messages
- List commits with flexible filtering and formatting
- Get detailed information about specific commits
- Cherry-pick commits from one branch to another
- Revert commits with proper error handling

## Usage

### Creating a Commit

```yaml
- name: Create Commit
  uses: ./actions/core/commit_operations
  with:
    action: create
    message: "Add new feature"
    files: "src/feature.js, src/tests/feature.test.js"
```

### Amending a Commit

```yaml
- name: Amend Commit
  uses: ./actions/core/commit_operations
  with:
    action: amend
    message: "Add new feature with test"
```

### Listing Recent Commits

```yaml
- name: List Recent Commits
  id: list-commits
  uses: ./actions/core/commit_operations
  with:
    action: list
    limit: 5
    format: "short"
```

### Getting Commit Information

```yaml
- name: Get Commit Info
  id: get-commit
  uses: ./actions/core/commit_operations
  with:
    action: get
    commit_hash: "abc1234"
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `action` | Commit operation to perform (create, amend, list, get, cherry-pick, revert) | Yes | |
| `message` | Commit message | Yes for create, amend | |
| `files` | Comma-separated list of files to include in the commit | No | . (all staged files) |
| `commit_hash` | Hash of the commit for get, cherry-pick, and revert operations | Yes for get, cherry-pick, revert | |
| `limit` | Number of commits to list | No | 10 |
| `author` | Filter commits by author | No | |
| `since` | List commits since date (ISO format) | No | |
| `until` | List commits until date (ISO format) | No | |
| `path` | Filter commits affecting a specific path | No | |
| `format` | Output format for list/get (oneline, short, medium, full) | No | medium |
| `no_verify` | Skip pre-commit hooks | No | false |

## Outputs

| Name | Description |
|------|-------------|
| `commits` | Commit information in requested format (for list/get actions) |
| `commit_hash` | Hash of the created or amended commit (for create/amend actions) |
| `result` | Operation result (success/failure) |
| `author` | Author of the commit (for get action) |
| `date` | Date of the commit (for get action) |
| `message` | Message of the commit (for get action) |

## Behavior Matrix

| Action | Inputs | Behavior | Outputs |
|--------|--------|----------|---------|
| create | message | Creates a commit with the specified message | result, commit_hash |
| create | message, files | Creates a commit with specific files | result, commit_hash |
| amend | | Amends the last commit keeping the message | result, commit_hash |
| amend | message | Amends the last commit with a new message | result, commit_hash |
| amend | files | Amends the last commit with additional files | result, commit_hash |
| list | | Lists the last 10 commits | commits, result |
| list | limit | Lists the specified number of commits | commits, result |
| list | author | Lists commits by a specific author | commits, result |
| list | since, until | Lists commits in the date range | commits, result |
| get | commit_hash | Gets information about a specific commit | result, author, date, message |
| cherry-pick | commit_hash | Cherry-picks the specified commit | result |
| revert | commit_hash | Reverts the specified commit | result, commit_hash |

## Implementation Details

The commit operations action is part of the atomic git operations suite, focusing specifically on commit-related operations. It uses the shared git utilities for common operations like Git configuration, validation, and error handling.

### Core Functions

- **create_commit**: Create a new commit with the specified message and files
- **amend_commit**: Amend the last commit with an optional new message or files
- **list_commits**: List commits with filtering options
- **get_commit_info**: Get detailed information about a specific commit
- **cherry_pick_commit**: Cherry-pick a commit from one branch to another
- **revert_commit**: Create a new commit that reverts a specified commit

### Error Handling

The action provides detailed error messages and appropriate exit codes for all operations. It handles common Git errors like:

- Conflicts during cherry-pick or revert operations
- Invalid commit references
- Permission issues
- Pre-commit hook failures

## Examples

### Committing Multiple Files

```yaml
- name: Commit Changes
  uses: ./actions/core/commit_operations
  with:
    action: create
    message: "Update documentation and add tests"
    files: "README.md, docs/usage.md, tests/new_test.js"
```

### Creating Commits with No-Verify

```yaml
- name: Quick Commit
  uses: ./actions/core/commit_operations
  with:
    action: create
    message: "WIP: Add feature"
    no_verify: true
```

### Getting Commit Information and Using It

```yaml
- name: Get Latest Commit Info
  id: commit-info
  uses: ./actions/core/commit_operations
  with:
    action: get
    commit_hash: HEAD
    format: full

- name: Use Commit Info
  run: echo "Latest commit by ${{ steps.commit-info.outputs.author }} on ${{ steps.commit-info.outputs.date }}"
```

### Listing Commits by Author

```yaml
- name: List User Commits
  id: user-commits
  uses: ./actions/core/commit_operations
  with:
    action: list
    author: "John Doe"
    since: "2023-01-01"
    limit: 20
    format: oneline

- name: Display Commits
  run: echo "${{ steps.user-commits.outputs.commits }}"
```