# Complete Action Example: File Operations

This example demonstrates the complete structure and configuration for creating a GitHub Action following the Loosely Coupled Modular Composition Pattern (LCMCP) used in the GitHub Toolkit.

## Overview

This example shows how to create a `file_operations` action that:
- Follows the LCMCP design principles
- Includes complete test coverage
- Integrates with the FCM Bridge system
- Provides both Core and Composite action patterns

## Directory Structure

The complete example is located in the repository at:

```
examples/complete-action-example/
├── README.md                           # Overview documentation
├── fcm/                               # Formal Conceptual Model
│   └── file-operations.fcm            # FCM definition
├── action/                            # Complete action implementation
│   ├── action.yml                     # GitHub Action metadata
│   ├── Dockerfile                     # Container definition
│   ├── main.py                       # Implementation
│   ├── requirements.txt              # Python dependencies
│   ├── pytest.ini                    # Test configuration
│   └── tests/                        # Test suite
│       ├── conftest.py               # Test fixtures
│       ├── test_unit.py              # Unit tests
│       └── test_integration.py       # Integration tests
├── workflow/                          # Example workflows
│   ├── use-action.yml                # Direct action usage
│   └── reusable-workflow.yml         # Reusable workflow pattern
└── docs/                             # Documentation
    └── file-operations.md            # Complete documentation
```

## Key Components

### 1. FCM Definition (`fcm/file-operations.fcm`)
Defines the conceptual model for the action, including:
- Parameters and their types
- Expected outputs
- Interface requirements
- Dependencies

### 2. Action Implementation (`action/`)
Complete Docker-based action following LCMCP principles:
- Single responsibility (file operations)
- Explicit interfaces (inputs/outputs)
- Complete encapsulation
- No hidden dependencies

### 3. Test Suite (`action/tests/`)
Comprehensive testing with:
- Unit tests for individual functions
- Integration tests for complete workflows
- 80%+ code coverage requirement
- Standardized fixtures from test framework

### 4. Workflow Examples (`workflow/`)
Shows how to use the action:
- Direct usage in workflows
- Creating reusable workflows
- Integration with other actions

## Design Principles Applied

1. **Modularity**: The action is completely self-contained
2. **Encapsulation**: All implementation details are hidden
3. **Composition**: Can be easily combined with other actions
4. **Testability**: Comprehensive test coverage
5. **Documentation**: Clear, complete documentation

## Getting Started

1. Review the FCM definition to understand the action's purpose
2. Examine the implementation to see LCMCP principles in practice
3. Run the tests to verify functionality
4. Use the workflow examples as templates

## Integration Points

- **FCM Bridge**: Can be generated from the FCM definition
- **Test Framework**: Uses standardized testing patterns
- **GitHub Actions**: Compatible with standard GitHub Actions runtime
- **Docker**: Consistent execution environment

This example serves as a template for creating new actions that follow the GitHub Toolkit's architectural patterns.

## Related Documentation

- [File Operations Action Details](file-operations.md) - Complete API documentation and usage examples
- [Understanding Actions](../../guides/understanding-actions.md) - Learn about the LCMCP pattern
- [Testing Framework](../../guides/testing-framework.md) - Testing patterns used in this example
- [Understanding FCM Bridge](../../guides/understanding-fcm-bridge.md) - How FCMs generate actions