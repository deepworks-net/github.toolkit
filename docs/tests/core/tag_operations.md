# Tag Operations Tests

This document outlines the testing approach for the Tag Operations action.

## Overview

The Tag Operations action includes comprehensive tests to ensure that it functions correctly in all scenarios. The tests are organized into two categories:

- **Unit Tests**: Test individual functions in isolation, using mocks to avoid actual Git operations.
- **Integration Tests**: Test the full functionality by performing actual Git operations in a temporary repository.

## Test Requirements

- All tests must pass before merging any changes to the action.
- Test coverage should be at least 80%.
- Both unit and integration tests must be included.

## Unit Tests

Unit tests verify that each function in the `GitTagOperations` class works correctly in isolation. These tests use mocks to avoid making actual Git operations.

### Test Cases

- Creating lightweight tags
- Creating annotated tags
- Creating tags at specific references
- Force creating tags
- Validating tag names
- Deleting tags (local and remote)
- Pushing tags
- Listing tags with different patterns and sorting methods
- Checking if tags exist
- Getting tag messages

### Running Unit Tests

```bash
python -m pytest tests/test_unit.py -v
```

## Integration Tests

Integration tests verify that the action works correctly in a real Git environment. These tests create a temporary Git repository, perform actual Git operations, and verify the results.

### Test Cases

- Creating and deleting tags
- Creating annotated tags and retrieving their messages
- Creating tags at specific references
- Listing tags with pattern filtering
- Tag name validation
- Force creating tags

### Running Integration Tests

```bash
python -m pytest tests/test_integration.py -v
```

## CI/CD Testing

The action is tested in CI/CD pipelines using the test workflow. This ensures that the action works correctly in a GitHub Actions environment.

### Test Workflow

The test workflow creates a temporary Git repository, configures the Git environment, and runs the action with various inputs. It verifies that the action produces the expected outputs and exit codes.

```yaml
name: Test Tag Operations

on:
  push:
    paths:
      - 'actions/core/tag_operations/**'
  pull_request:
    paths:
      - 'actions/core/tag_operations/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Git
        run: |
          git config --global user.name "Test User"
          git config --global user.email "test@example.com"
      
      - name: Run Unit Tests
        run: |
          cd actions/core/tag_operations
          python -m pytest tests/test_unit.py -v --cov=main --cov-report=term
      
      - name: Run Integration Tests
        run: |
          cd actions/core/tag_operations
          python -m pytest tests/test_integration.py -v
```

## Test Coverage

Test coverage is monitored using the `pytest-cov` plugin. The coverage report is generated during test execution and displayed in the CI/CD pipeline.

## Edge Cases and Error Handling

The tests include a range of edge cases to ensure that the action handles all scenarios correctly:

- Invalid tag names
- Duplicate tag creation
- Deleting non-existent tags
- Force operations
- Various tag name patterns
- Different sorting methods

Error handling is verified to ensure that the action provides clear error messages and appropriate exit codes in all error scenarios.