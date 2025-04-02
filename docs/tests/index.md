# Testing in GitHub Actions Toolkit

This section describes the testing approach, standards, and tools used across the repository.

## Testing Framework

All actions in this repository use a standardized testing framework for consistent testing.

### Test Structure

Tests are organized into three categories:

1. **Unit Tests** - Test individual functions and classes in isolation
2. **Integration Tests** - Test interactions between components
3. **End-to-End Tests** - Test complete workflows in a realistic environment

### Coverage Requirements

All code must maintain a minimum of 80% test coverage. This is enforced by automated checks in the CI pipeline.

## Running Tests

Tests can be run using pytest:

```bash
# Navigate to an action directory
cd actions/core/branch_operations

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## CI/CD Pipeline

A GitHub Actions workflow automatically runs tests on:
- Pull requests to main and develop branches
- Pushes to main and develop branches

The workflow:
1. Runs tests for each action
2. Verifies minimum 80% code coverage
3. Runs linting to ensure code quality

## Test Templates

Standardized test templates are available to maintain consistency:

```bash
# Copy unit test template
cp actions/test_framework/test_templates/test_unit_template.py your_action/tests/test_unit.py

# Copy integration test template
cp actions/test_framework/test_templates/test_integration_template.py your_action/tests/test_integration.py
```

## Available Fixtures

The test framework provides fixtures for common testing scenarios:

- `mock_subprocess` - Mocks subprocess calls to git
- `mock_git_env` - Sets up GitHub Actions environment variables
- `mock_git_repo` - Simulates a git repository structure
- `git_outputs` - Provides sample git command outputs

## Common Test Patterns

### 1. Input Validation Tests

```python
def test_invalid_input(mock_git_env):
    # Arrange
    os.environ['INPUT_INVALID'] = 'invalid-value'
    
    # Act & Assert
    with pytest.raises(SystemExit):
        main()
```

### 2. Output Verification Tests

```python
def test_output_format(mock_subprocess, mock_git_env):
    # Arrange
    os.environ['INPUT_ACTION'] = 'list'
    mock_subprocess['check_output'].return_value = 'branch1\nbranch2'
    
    # Act
    main()
    
    # Assert
    with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
        output = f.read()
    assert 'branches=branch1,branch2' in output
```

### 3. Error Handling Tests

```python
def test_error_handling(mock_subprocess, mock_git_env):
    # Arrange
    mock_subprocess['check_call'].side_effect = subprocess.CalledProcessError(1, 'git')
    
    # Act & Assert
    with pytest.raises(SystemExit):
        main()
```

## Test File Structure

```
actions/
├── core/
│   ├── branch_operations/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_unit.py
│   │   │   └── test_integration.py
│   │   ├── Dockerfile
│   │   ├── action.yml
│   │   ├── main.py
│   │   └── pytest.ini
│   └── ...
└── test_framework/
    ├── conftest.py
    ├── pytest.ini
    ├── README.md
    └── test_templates/
        ├── test_unit_template.py
        └── test_integration_template.py
```

## Available Test Suites

- [Branch Operations Tests](core/branch_operations.md)
- [Version Calculator Tests](core/version_calculator.md)
- [Version Updater Tests](core/version_updater.md)

## Best Practices

1. Use descriptive test names that explain what is being tested
2. Follow the Arrange-Act-Assert pattern
3. Keep unit tests focused on a single function
4. Use the provided fixtures to minimize test setup code
5. Mock external dependencies and API calls
6. Always test error handling and edge cases