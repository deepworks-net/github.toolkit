# Actions Overview

## Architecture

Our GitHub Actions toolkit follows a layered architecture that promotes reusability, maintainability, and clear separation of concerns.

### Core Actions

- Atomic, self-contained operations
- Single responsibility principle
- Highly reusable
- [Learn more about Core Actions](core/index.md)

### Composite Actions

- Combine core actions
- Add workflow-specific logic
- Higher-level operations
- [Learn more about Composite Actions](composite/index.md)

## Directory Structure

```FILEDIR
actions/
├── core/                  # Atomic operations
│   ├── branch_operations/
│   ├── commit_operations/
│   ├── tag_operations/
│   ├── version_calculator/
│   └── version_updater/
├── composite/            # Combined operations
│   ├── release_operations/
│   └── update_changelog/
└── shared/               # Shared utilities
    └── git_utils/        # Common Git functions
```

## Usage Patterns

### Using Core Actions

```yaml
steps:
  - name: Calculate Version
    uses: deepworks-net/github.toolkit/actions/core/version_calculator@v1
    with:
      default_version: 'v0.1.0'
```

### Using Composite Actions

```yaml
steps:
  - name: Update Changelog
    uses: deepworks-net/github.toolkit/actions/composite/update_changelog@v1
    with:
      content: ${% raw %}{{ steps.notes.outputs.content }}{% endraw %}
```

## Standards

### Docker Configuration

- Standard base image (python:3.9-slim)
- Consistent dependency management
- Clear entrypoint configuration

### Core/Composite Pattern

- Atomic core actions with single responsibilities
- Shared utilities for common functions
- Composite actions that combine core actions
- Clear separation of concerns

### Testing

- Comprehensive test workflows
- Standard test structure
- Clear naming conventions
- Unit tests for atomic functions
- Integration tests for real-world scenarios

### Documentation

- Complete API documentation
- Usage examples
- Error handling guidance
- Migration guides for new patterns

## Available Actions

### Core

- [Core Actions](core/index.md)
    - [Branch Operations](core/branch_operations/index.md)
    - [Commit Operations](core/commit_operations/index.md)
    - [Manage Release](core/manage_release/index.md)
    - [Tag Operations](core/tag_operations/index.md)
    - [Version Calculator](core/version_calculator/index.md)
    - [Version Updater](core/version_updater/index.md)

### Composite

- [Composite Actions](composite/index.md)
    - [Release Operations](composite/release_operations/index.md)
    - [Update Changelog](composite/update_changelog/index.md)

### Shared Utilities

- [Git Utilities](../guides/git-utilities.md) - Common git operation utilities
