# Git Operations Testing Framework

This framework provides a standardized approach to testing Git operations in GitHub Actions, particularly for the atomic and composite actions in this repository.

## Overview

The testing framework includes:

- Common pytest fixtures for mocking git operations
- Standardized utilities for Git command testing
- Test templates for unit and integration tests
- Support for testing both atomic and composite Git actions
- Standardized markers for organizing tests
- Configuration for code coverage reporting

## Usage

### 1. Set up a new action's test structure

Copy the testing framework files to your action's directory:

```bash
# From your action directory
mkdir -p tests
cp /path/to/test_framework/conftest.py tests/
cp /path/to/test_framework/pytest.ini ./
```

### 2. Create unit tests

Use the unit test template as a starting point:

```bash
cp /path/to/test_framework/test_templates/test_unit_template.py tests/test_unit.py
```

Modify the template to test your specific action functionality.

### 3. Create integration tests

Use the integration test template as a starting point:

```bash
cp /path/to/test_framework/test_templates/test_integration_template.py tests/test_integration.py
```

### 4. Run tests

Run your tests with:

```bash
pytest
```

Or with specific markers:

```bash
pytest -m unit  # Run only unit tests
pytest -m integration  # Run only integration tests
```

## Available Fixtures

- `mock_subprocess`: Mocks subprocess functions (check_call, check_output, run)
- `mock_git_env`: Sets up environment variables needed for GitHub Actions
- `mock_git_repo`: Simulates a git repository structure
- `git_outputs`: Provides sample git command outputs for testing
- `branch_outputs`: Sample outputs for branch operations
- `tag_outputs`: Sample outputs for tag operations
- `commit_outputs`: Sample outputs for commit operations
- `mock_composite_action`: Mocks composite actions for testing interrelated actions

## Markers

- `unit`: Unit tests
- `integration`: Integration tests
- `slow`: Slow-running tests
- `git`: Tests for git operations
- `branch`: Tests for branch operations
- `tag`: Tests for tag operations
- `commit`: Tests for commit operations
- `release`: Tests for release operations
- `changelog`: Tests for changelog operations
- `composite`: Tests for composite actions

## Best Practices

1. Keep unit tests fast and focused on a single function
2. Use integration tests to verify end-to-end workflows
3. Use the provided fixtures to avoid duplicating mock setup code
4. Always check for proper error handling in your tests
5. When testing composite actions, mock each component action appropriately
6. Use the shared git utilities in new action implementations
7. Ensure tests cover all public methods in Git operation classes
8. Test both success and failure paths for all operations

## Testing Atomic Actions vs. Composite Actions

### Atomic Actions

When testing atomic Git operations:

1. Unit test each method in the class
2. Mock all subprocess calls
3. Test with both valid and invalid inputs
4. Verify proper outputs and error handling

### Composite Actions

When testing composite actions:

1. Mock each component action
2. Test the flow between components
3. Verify inputs are correctly passed between steps
4. Test different paths through the action based on inputs