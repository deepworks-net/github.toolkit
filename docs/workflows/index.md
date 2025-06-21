# Workflows Overview

**📖 For comprehensive documentation:** [Understanding Workflows Guide](../guides/understanding-workflows.md)

## Structure

```markdown
.github/workflows/
├── .flow.*.yml                # Private/internal flows for this repository
├── .core.*.yml                # Private/internal core workflows
├── core.action.*.yml          # Public atomic, reusable workflows
├── flow.*.yml                 # Public higher-level flows combining actions/workflows
└── test.*.yml                # Test workflows for actions/flows
```

## Naming Convention

### Private/Internal Workflows

- Pattern: `.flow.<name>.yml` or `.core.<name>.yml`
- Purpose: Repository-specific workflows not intended for external use
- Visibility: Private to the repository (like private access modifiers)
- Example: `.flow.update_version.yml`

> **Note**: Workflows prefixed with a dot (`.`) are internal to the repository and should not be referenced externally via `uses:` statements. These handle repository-specific operations.

### Core Action Workflows

- Pattern: `core.action.<name>.yml`
- Purpose: Atomic, reusable operations
- Visibility: Public - can be used externally
- Example: `core.action.version_calculator.yml`

### Flow Workflows

- Pattern: `flow.<name>.yml`
- Purpose: Combine core actions into higher-level operations
- Visibility: Public - can be used externally depending on exposed inputs/outputs
- Example: `flow.prepare_release.yml`

### Test Workflows

- Pattern: `test.<type>.<name>.yml`
- Purpose: Validate actions and flows
- Example: `test.core.action.version_calculator.yml`

## Implemented Workflows

### Core Action Workflows

#### [Version Calculator](core/version_calculator.md)

- Calculates next version based on Git tags
- Provides current version, next version, and commit count
- Used for automated version management

#### [Version Updater](core/version_updater.md)

- Updates version numbers across multiple files
- Supports YAML, JSON, and text files
- Maintains file formatting and structure

### Flow Workflows

#### [Prepare Release](flow/prepare_release.md)

- Combines version calculation and updating
- Manages release preparation process
- Creates release branches and PRs

### Test Workflows

#### [Version Calculator Tests](tests/core/version_calculator.md)

- Validates version calculation logic
- Tests with and without existing tags
- Verifies output format and error handling

#### [Version Updater Tests](tests/core/version_updater.md)

- Tests file updates across formats
- Validates prefix handling
- Verifies error conditions

## Usage Patterns

### Using Core Action Workflows

```yaml
jobs:
  calculate:
    uses: deepworks-net/github.toolkit/.github/workflows/core.action.version_calculator.yml@v1
```

### Using Flow Workflows

```yaml
jobs:
  prepare:
    uses: deepworks-net/github.toolkit/.github/workflows/flow.prepare_release.yml@v1
```

## Implementation Guidelines

### Core Action Workflows

1. Single responsibility principle
2. Clear input/output contract
3. Error handling
4. Comprehensive tests

### Flow Workflows

1. Combine core actions
2. Handle workflow state
3. Provide higher-level operations
4. Error recovery

## Best Practices

1. **Workflow Selection**
    - Use core actions for atomic operations
    - Use flows for complex processes
    - Keep responsibilities clear

2. **Version Management**
    - Tag releases appropriately
    - Reference specific versions
    - Document breaking changes

3. **Error Handling**
    - Provide clear error messages
    - Handle failure states
    - Document error conditions

4. **Testing**
    - Test all workflows
    - Include error cases
    - Verify outputs
