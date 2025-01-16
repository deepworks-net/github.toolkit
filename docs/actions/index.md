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
│   ├── version_calculator/
│   └── version_updater/
└── composite/            # Combined operations
    └── update_changelog/
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

### Testing

- Comprehensive test workflows
- Standard test structure
- Clear naming conventions

### Documentation

- Complete API documentation
- Usage examples
- Error handling guidance

## Contributing

See our guides for creating:

- [New Core Actions](contributing/core-actions.md)
- [New Composite Actions](contributing/composite-actions.md)
- [Action Tests](contributing/testing.md)

## Available Actions

### Core

- [Version Calculator](core/version_calculator/index.md)
- [Version Updater](core/version_updater/index.md)

### Composite

- [Update Changelog](composite/update_changelog/index.md)
