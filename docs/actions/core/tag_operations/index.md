# Tag Operations

The Tag Operations action provides atomic git tag operations, allowing you to create, delete, push, list, and check git tags as part of your workflows.

## Overview

This action is a self-contained, Docker-based action that performs Git tag operations. It is designed to be used as part of GitHub Actions workflows to manage releases and version tagging.

Key features include:

- Creating tags (both lightweight and annotated)
- Deleting tags (locally and remotely)
- Pushing tags to remote repositories
- Listing tags with pattern filtering
- Checking if tags exist
- Tag name validation
- Comprehensive error handling

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

## Examples

### Creating a Tag

```yaml
- name: Create Release Tag
  id: create-tag
  uses: ./actions/core/tag_operations
  with:
    action: create
    tag_name: v1.0.0
    message: "Release v1.0.0"
    remote: true  # Push to remote
```

### Checking if a Tag Exists

```yaml
- name: Check Tag
  id: check-tag
  uses: ./actions/core/tag_operations
  with:
    action: check
    tag_name: v1.0.0

- name: Use Tag Check Result
  run: |
    if [[ "{% raw %}${{ steps.check-tag.outputs.tag_exists }}{% endraw %}" == "true" ]]; then
      echo "Tag v1.0.0 exists with message: {% raw %}${{ steps.check-tag.outputs.tag_message }}{% endraw %}"
    else
      echo "Tag v1.0.0 does not exist"
    fi
```

### Listing Tags

```yaml
- name: List Tags
  id: list-tags
  uses: ./actions/core/tag_operations
  with:
    action: list
    pattern: "v1.*"
    sort: version  # Sort by semantic versioning

- name: Display Tags
  run: |
    echo "Found tags: {% raw %}${{ steps.list-tags.outputs.tags }}{% endraw %}"
```

### Deleting a Tag

```yaml
- name: Delete Tag
  uses: ./actions/core/tag_operations
  with:
    action: delete
    tag_name: v1.0.0
    remote: true  # Delete from remote
```

### Force-Pushing a Tag

```yaml
- name: Push Tag
  uses: ./actions/core/tag_operations
  with:
    action: push
    tag_name: v1.0.0
    force: true  # Force push
```

## Error Handling

The action handles various error conditions:

- Invalid tag names are rejected
- Attempting to create an existing tag without force flag
- Attempting to delete a non-existent tag
- Git command execution failures

The action returns the `result` output as "success" or "failure", and sets the action's exit code accordingly.

## Implementation Notes

The tag operations action follows the single-responsibility principle, focusing solely on tag operations. It works well in conjunction with other actions like branch operations.

Tag name validation follows Git's rules, rejecting names with spaces, control characters, and certain special characters like `~^:?*[]\`.

For tag listing with sorting by version, the action implements semantic versioning-aware sorting that can handle tags like `v1.10.0` correctly (sorted after `v1.9.0`).