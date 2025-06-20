# Understanding Actions in GitHub Toolkit

This guide explains the two types of actions in the GitHub Toolkit: Core Actions and Composite Actions. Understanding these concepts is essential for effectively using and extending the toolkit.

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

Composite Actions combine multiple Core Actions or other operations to create higher-level workflows. They orchestrate complex processes by sequencing simpler operations.

### What is a Composite Action

Composite Actions are:
- **Orchestrators**: Combine multiple actions into workflows
- **Higher-level**: Provide business logic and process flows
- **Flexible**: Can include conditional logic and complex decision-making
- **Reusable**: Encapsulate common multi-step processes

### Structure Differences from Core Actions

Composite Actions use a different execution model:

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

runs:
  using: "composite"
  steps:
    - name: "Process changelog content"
      run: |
        # Complex shell logic or call to other actions
        echo "Processing changelog..."
      shell: bash
    
    - name: "Update file"
      uses: ./actions/core/file_operations
      with:
        action: update
        file: CHANGELOG.md
        content: ${{ inputs.content }}
```

### Example: Update Changelog Composite Action

The `update_changelog` action demonstrates Composite Action patterns:

**Location**: `actions/composite/update_changelog/`

**Purpose**: Manages CHANGELOG.md file updates with proper formatting

**Key Features**:
- Processes changelog content with complex logic
- Handles different modes (unreleased, release)
- Maintains changelog formatting standards
- Integrates with version management workflow

**Usage in Workflow**:
```yaml
- uses: ./actions/composite/update_changelog
  with:
    content: "## [1.2.0] - 2024-01-15\n### Added\n- New feature"
    mode: release
    version: "1.2.0"
```

## Action Development Guidelines

### When to Create Core Actions

Create Core Actions when you need:
- Single-purpose, atomic operations
- Reusable functionality across multiple workflows
- Standardized error handling and logging
- Consistent input/output patterns

### When to Create Composite Actions

Create Composite Actions when you need:
- Multi-step processes with complex logic
- Business workflow orchestration
- Conditional execution based on inputs
- Integration of multiple Core Actions

### Best Practices

1. **Follow the Single Responsibility Principle**: Each Core Action should do one thing well
2. **Use Environment Variables**: Follow GitHub's input/output conventions
3. **Implement Comprehensive Testing**: Both unit and integration tests are required
4. **Document Thoroughly**: Clear descriptions and usage examples
5. **Handle Errors Gracefully**: Provide meaningful error messages and appropriate exit codes
6. **Maintain Consistency**: Follow established patterns and conventions

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