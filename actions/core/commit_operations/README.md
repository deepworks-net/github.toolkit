# Commit Operations Action

A self-contained action that provides atomic git commit operations.

## Features

- Create new commits
- Amend existing commits
- List commits with filtering
- Get commit information
- Cherry-pick commits from other branches
- Revert commits
- Comprehensive error handling and validation

## Usage

### Creating a commit

```yaml
- name: Commit Changes
  uses: ./actions/core/commit_operations
  with:
    action: create
    message: "Add new feature"
    files: "src/feature.js, src/tests/feature.test.js"
```

### Amending a commit

```yaml
- name: Amend Commit
  uses: ./actions/core/commit_operations
  with:
    action: amend
    message: "Add new feature with test"
    files: "src/feature.js, src/tests/feature.test.js"
```

### Listing recent commits

```yaml
- name: List Recent Commits
  id: list-commits
  uses: ./actions/core/commit_operations
  with:
    action: list
    limit: 5
    format: "short"
```

### Getting commit information

```yaml
- name: Get Commit Info
  id: get-commit
  uses: ./actions/core/commit_operations
  with:
    action: get
    commit_hash: "abc1234"
```

### Cherry-picking a commit

```yaml
- name: Cherry Pick Commit
  uses: ./actions/core/commit_operations
  with:
    action: cherry-pick
    commit_hash: "abc1234"
```

### Reverting a commit

```yaml
- name: Revert Commit
  uses: ./actions/core/commit_operations
  with:
    action: revert
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

## Error Handling

- Missing required inputs are caught with descriptive error messages
- Git errors are handled with appropriate user feedback
- Pre-commit hook failures are reported clearly
- Proper exit codes for workflow control

## Implementation Notes

- Automatically configures a default Git identity (GitHub Actions) when running in environments where user.name and user.email are not set
- Safe directory is configured automatically for GitHub workspace
- Uses proper error handling and exit codes to ensure workflow continuity
- Leverages shared git utilities for common operations