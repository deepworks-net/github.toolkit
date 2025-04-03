# Tag Operations Action

A self-contained action that provides atomic git tag operations.

## Features

- Create new tags (annotated or lightweight)
- Delete tags (locally or remotely)
- Push tags to remote
- List tags with pattern filtering
- Check if tags exist
- Sort tags by alphabetic order, semantic versioning, or creation date
- Tag name validation
- Comprehensive error handling

## Usage

### Creating a tag

```yaml
- name: Create Release Tag
  uses: ./actions/core/tag_operations
  with:
    action: create
    tag_name: v1.0.0
    message: "Release v1.0.0"
    remote: true  # Push to remote
```

### Deleting a tag

```yaml
- name: Delete Tag
  uses: ./actions/core/tag_operations
  with:
    action: delete
    tag_name: v1.0.0
    remote: true  # Delete from remote
```

### Listing tags

```yaml
- name: List Tags
  id: list-tags
  uses: ./actions/core/tag_operations
  with:
    action: list
    pattern: "v1.*"
    sort: version  # Sort by semantic versioning
```

### Checking if a tag exists

```yaml
- name: Check Tag
  id: check-tag
  uses: ./actions/core/tag_operations
  with:
    action: check
    tag_name: v1.0.0
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `action` | Tag operation to perform (create, delete, list, push, check) | Yes | |
| `tag_name` | Name of the tag to operate on | Yes for create, delete, push, check | |
| `message` | Message for annotated tag creation | No | |
| `ref` | Reference (commit SHA, branch) to place the tag on | No | |
| `pattern` | Pattern for listing tags (e.g. "v1.*") | No | |
| `remote` | Include remote operations (push/delete remote tag) | No | false |
| `force` | Force operation (used with create or push) | No | false |
| `sort` | Sorting method for listing tags (alphabetic, version, date) | No | alphabetic |

## Outputs

| Name | Description |
|------|-------------|
| `tags` | Comma-separated list of tags (when using list action) |
| `result` | Operation result (success/failure) |
| `tag_exists` | Whether the tag exists (true/false) |
| `tag_message` | Message associated with the tag (if exists and is annotated) |

## Behavior Matrix

| Action | Inputs | Behavior | Outputs |
|--------|--------|----------|---------|
| create | tag_name | Creates a lightweight tag | result, tag_exists |
| create | tag_name, message | Creates an annotated tag | result, tag_exists |
| create | tag_name, ref | Creates tag at specified ref | result, tag_exists |
| create | tag_name, force=true | Overwrites existing tag | result, tag_exists |
| create | tag_name, remote=true | Creates tag and pushes to remote | result, tag_exists |
| delete | tag_name | Deletes local tag | result |
| delete | tag_name, remote=true | Deletes local and remote tag | result |
| push | tag_name | Pushes tag to remote | result |
| push | tag_name, force=true | Force pushes tag to remote | result |
| list | | Lists all tags | tags, result |
| list | pattern | Lists tags matching pattern | tags, result |
| list | sort=version | Lists tags sorted by version | tags, result |
| list | sort=date | Lists tags sorted by creation date | tags, result |
| check | tag_name | Checks if tag exists | result, tag_exists, tag_message |

## Error Handling

- Invalid tag names are rejected with appropriate error messages
- Tag operations that fail have descriptive error messages
- Force flag required to overwrite existing tags
- Proper exit codes for workflow control