# Understanding Actions in GitHub Toolkit

This guide explains the two types of actions in the GitHub Toolkit: Core Actions and Composite Actions. Both follow the Loosely Coupled Modular Composition Pattern (LCMCP) for consistent architecture. Understanding these concepts is essential for effectively using and extending the toolkit.

## Core Actions

Core Actions are atomic, self-contained operations that perform a single specific task. They follow the principle of single responsibility and are designed to be reusable building blocks.

### What is a Core Action

Core Actions are:
- **Atomic**: Each action performs one specific operation
- **Self-contained**: All dependencies are packaged within the action
- **Docker-based**: Executed in isolated containers for consistency
- **Generated**: Created from FCM (Formal Conceptual Model) definitions

### Anatomy of a Core Action

Every Core Action follows this standardized structure:

```
actions/core/[action-name]/
├── action.yml          # GitHub Action metadata
├── Dockerfile          # Container definition
├── main.py            # Implementation logic
├── .bridge-sync       # FCM generation metadata (if generated)
└── tests/             # Test suite
    ├── conftest.py
    ├── test_unit.py
    └── test_integration.py
```

### Key Components Explained

#### action.yml Structure

The `action.yml` file defines the action's interface:

```yaml
name: 'Branch Operations'
description: 'Perform Git branch operations'
author: 'Deepworks'
inputs:
  action:
    description: 'Branch operation to perform'
    required: true
  branch_name:
    description: 'Name of the branch to operate on'
    required: false
outputs:
  result:
    description: 'Operation result (success/failure)'
  current_branch:
    description: 'Current branch after operation'
runs:
  using: 'docker'
  image: 'Dockerfile'
```

#### Dockerfile Pattern

Core Actions use a consistent Docker pattern:

```dockerfile
FROM python:3.9-slim

# Install git (required for git operations)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy implementation
COPY main.py .

# Set entrypoint
ENTRYPOINT ["python", "/app/main.py"]
```

#### main.py Implementation Pattern

The main.py follows a standard structure for Core Actions:

```python
#!/usr/bin/env python3

import os
import sys
import subprocess

class GitBranchOperations:
    def __init__(self):
        self._configure_git()
    
    def _configure_git(self):
        """Configure git for safe directory operations."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git: {e}")
            sys.exit(1)

def main():
    """Main entry point for the action."""
    # Get inputs from environment variables
    action = os.environ.get('INPUT_ACTION')
    branch_name = os.environ.get('INPUT_BRANCH_NAME')
    
    # Perform operations
    # ...
    
    # Set outputs
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"result={'success' if result else 'failure'}\n")
        f.write(f"current_branch={current_branch}\n")
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Input/Output Patterns

Core Actions follow GitHub's standard patterns:

- **Input Variables**: Accessed via `os.environ.get('INPUT_[NAME]')`
- **Output Variables**: Written to `$GITHUB_OUTPUT` file
- **Error Handling**: Use appropriate exit codes (0 for success, 1+ for errors)

### Example: Branch Operations Core Action

The `branch_operations` action demonstrates a complete Core Action implementation:

**Location**: `actions/core/branch_operations/`

**Purpose**: Provides comprehensive Git branch management capabilities

**Key Features**:
- Create, delete, checkout, merge, and list branches
- Support for remote operations
- Force operations when needed
- Pattern-based branch filtering

**Usage Example**:
```yaml
- uses: ./actions/core/branch_operations
  with:
    action: create
    branch_name: feature/new-feature
    base_branch: main
    remote: true
```

This action showcases all the patterns and best practices for Core Actions:
- Comprehensive input validation
- Atomic operations with clear success/failure states
- Proper error handling and logging
- Standardized output format
- Complete test coverage

## Composite Actions

Composite Actions in this toolkit follow the **Loosely Coupled Modular Composition Pattern (LCMCP)**, a design philosophy that emphasizes modularity, encapsulation, and composition. While GitHub provides a native composite action format using `using: composite` with steps, this toolkit deliberately uses Docker-based implementations for all actions, including composites.

### Design Philosophy: Why Docker for Composite Actions

The decision to use Docker for Composite Actions rather than GitHub's native composite format is based on the LCMCP principles:

1. **Strict Encapsulation**: Docker containers provide complete encapsulation of dependencies, environment, and implementation details
2. **Atomic Responsibility**: Each action, whether Core or Composite, maintains a single, well-defined responsibility
3. **Consistent Interface**: All actions expose the same interface pattern regardless of complexity
4. **Framework Agnosticism**: Docker-based actions can run in any environment that supports containers
5. **Progressive Complexity**: Complex behavior emerges from composing simpler modules, not from inheritance or steps

### What are Composite Actions

In this toolkit, Composite Actions are:
- **Higher-level orchestrators**: Combine multiple operations into unified workflows
- **Business logic containers**: Encapsulate domain-specific processes
- **Docker-based modules**: Use the same container pattern as Core Actions
- **Loosely coupled**: Interact with other actions through well-defined interfaces

### Architecture Pattern

```yaml
name: "Update Changelog"
description: "Manages CHANGELOG.md file content and formatting"
inputs:
  content:
    description: 'Content to add to changelog'
    required: true
  mode:
    description: 'Operation mode (unreleased, release)'
    required: true
  version:
    description: 'Version number for release mode'
    required: false

runs:
  using: "docker"
  image: "Dockerfile"
```

This pattern provides several advantages:
- **Consistency**: All actions follow the same execution model
- **Isolation**: Each action runs in its own environment
- **Testability**: Docker containers can be tested independently
- **Portability**: Actions work identically across different systems

### Example: Update Changelog Composite Action

The `update_changelog` action demonstrates the LCMCP pattern in practice:

**Location**: `actions/composite/update_changelog/`

**Purpose**: Manages CHANGELOG.md file updates with complex formatting logic

**Key Design Elements**:
- Encapsulates all changelog logic within a single container
- Exposes a simple interface hiding complex implementation
- Maintains no direct dependencies on other actions
- Can be composed with other actions in workflows

**Usage in Workflow**:
```yaml
- uses: deepworks-net/github.toolkit/actions/composite/update_changelog@v1
  with:
    content: ${{ steps.notes.outputs.content }}
    mode: 'unreleased'
    version: ${{ steps.version.outputs.next_version }}
```

### Composition Over Steps

Unlike traditional GitHub composite actions that define steps, LCMCP composite actions achieve complexity through:

1. **Internal Composition**: Complex logic is handled within the container
2. **External Orchestration**: Workflows compose multiple actions
3. **Clear Boundaries**: Each action maintains its own state and logic
4. **Minimal Coupling**: Actions communicate only through inputs/outputs

Example workflow composition:
```yaml
steps:
  # Each action is a self-contained module
  - name: Calculate Version
    id: version
    uses: ./actions/core/version_calculator
    
  - name: Generate Release Notes
    id: notes
    uses: ./actions/composite/release_notes
    with:
      version: ${{ steps.version.outputs.next_version }}
      
  - name: Update Changelog
    uses: ./actions/composite/update_changelog
    with:
      content: ${{ steps.notes.outputs.content }}
      version: ${{ steps.version.outputs.next_version }}
```

### Benefits of This Approach

1. **Uniform Testing**: All actions can be tested the same way
2. **Consistent Deployment**: Same deployment pattern for all actions
3. **Clear Boundaries**: No confusion about where logic resides
4. **Better Encapsulation**: Implementation details truly hidden
5. **Easier Maintenance**: Changes don't cascade through step definitions

## Action Development Guidelines

### When to Create Core Actions

Create Core Actions when you need:
- Single-purpose, atomic operations
- Reusable functionality across multiple workflows
- Standardized error handling and logging
- Consistent input/output patterns

### When to Create Composite Actions

Create Composite Actions when you need:
- Multi-step processes that form a cohesive business operation
- Complex logic that combines multiple atomic operations
- Domain-specific workflows that hide implementation complexity
- Reusable patterns that appear across multiple workflows

### Best Practices

1. **Follow the Single Responsibility Principle**: Each Core Action should do one thing well
2. **Use Environment Variables**: Follow GitHub's input/output conventions
3. **Implement Comprehensive Testing**: Both unit and integration tests are required
4. **Document Thoroughly**: Clear descriptions and usage examples
5. **Handle Errors Gracefully**: Provide meaningful error messages and appropriate exit codes
6. **Maintain Consistency**: Follow established patterns and conventions

### LCMCP Principles in Action Development

When developing actions in this toolkit, follow these LCMCP principles:

1. **Maintain Module Independence**: Each action should function without knowledge of other actions
2. **Use Explicit Interfaces**: All inputs and outputs must be clearly defined
3. **Avoid Hidden Dependencies**: Don't rely on external state or side effects
4. **Compose, Don't Inherit**: Build complex behavior by combining simple actions
5. **Encapsulate Completely**: Hide all implementation details behind the action interface

## Integration with FCM Bridge

Many Core Actions are generated from FCM (Formal Conceptual Model) definitions. These actions include a `.bridge-sync` file that tracks their generation metadata:

```yaml
source: axioms/git/branch-operations.fcm
generated: 2024-01-15T10:30:00Z
checksum: sha256:abc123...
```

**Important**: Never edit generated actions directly. Instead, modify the FCM definition and regenerate the action using the bridge system.

## Testing Requirements

All actions must include comprehensive test suites:

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test complete action workflows
- **Coverage**: Minimum 80% code coverage required
- **Fixtures**: Use standardized test fixtures from `actions/test_framework/`

See the [Testing Framework Guide](testing-framework.md) for detailed testing patterns and requirements.

## Related Guides

- [Understanding Workflows](understanding-workflows.md) - Learn how actions are used in workflows
- [Understanding FCM Bridge](understanding-fcm-bridge.md) - Understand action generation
- [Testing Framework](testing-framework.md) - Testing patterns and requirements