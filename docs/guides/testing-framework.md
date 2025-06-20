# Testing Framework Guide

This guide explains the comprehensive testing framework used throughout the GitHub Toolkit. The framework provides standardized approaches for testing both Core Actions and Composite Actions with consistent patterns and quality requirements.

## Overview

The testing framework ensures reliability and maintainability through:

- **Standardized Structure**: Consistent test organization across all actions
- **Common Fixtures**: Reusable testing utilities and mocks
- **Coverage Requirements**: Minimum 80% code coverage for all actions
- **Multi-Level Testing**: Unit, integration, and end-to-end testing
- **CI/CD Integration**: Automated testing in GitHub workflows

## Testing Architecture

### Framework Components

The testing framework consists of several key components:

```
actions/test_framework/
├── README.md                    # Framework documentation
├── conftest.py                  # Shared fixtures and utilities
├── pytest.ini                  # Global test configuration
└── test_templates/              # Template files for new tests
    ├── test_unit_template.py
    └── test_integration_template.py
```

### Action Test Structure

Every action follows this standardized test structure:

```
actions/core/[action-name]/
├── main.py                      # Implementation
├── pytest.ini                  # Test configuration
└── tests/                       # Test suite
    ├── conftest.py              # Action-specific fixtures
    ├── test_unit.py             # Unit tests
    └── test_integration.py      # Integration tests
```

## Test Configuration

### pytest.ini Configuration

Each action includes a `pytest.ini` file that defines testing behavior:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: unit tests
    integration: integration tests
    branch: tests for branch operations
addopts = -v
```

The framework-level configuration includes additional options:

```ini
addopts = -v --cov=src --cov-report=term-missing
```

### Test Markers

The framework uses standardized markers to organize tests:

- `unit`: Fast, isolated unit tests
- `integration`: End-to-end integration tests
- `slow`: Tests that take longer to execute
- `git`: Tests for git operations
- `branch`: Tests for branch operations
- `tag`: Tests for tag operations
- `commit`: Tests for commit operations
- `release`: Tests for release operations
- `changelog`: Tests for changelog operations
- `composite`: Tests for composite actions

## Available Fixtures

The framework provides comprehensive fixtures for consistent testing:

### Core Fixtures

#### mock_subprocess
Mocks all subprocess operations for safe testing:

```python
@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing without executing shell commands."""
    with patch('subprocess.check_call') as mock_check_call, \
         patch('subprocess.check_output') as mock_check_output, \
         patch('subprocess.run') as mock_run:
        
        # Configure default successful behavior
        mock_check_call.return_value = 0
        mock_check_output.return_value = "mocked output"
        
        yield {
            'check_call': mock_check_call,
            'check_output': mock_check_output,
            'run': mock_run
        }
```

**Usage Example:**
```python
def test_git_operation(mock_subprocess):
    # Act
    result = git_ops.create_branch('test-branch')
    
    # Assert
    assert result is True
    mock_subprocess['check_call'].assert_called_with(['git', 'checkout', '-b', 'test-branch'])
```

#### mock_git_env
Sets up GitHub Actions environment variables:

```python
@pytest.fixture
def mock_git_env():
    """Mock environment variables for git operations."""
    env_vars = {
        'GITHUB_REPOSITORY': 'test-org/test-repo',
        'GITHUB_TOKEN': 'mock-token',
        'GITHUB_WORKSPACE': '/github/workspace',
        'GITHUB_OUTPUT': '/tmp/github_output'
    }
    # ... setup and teardown logic
```

**Usage Example:**
```python
def test_github_integration(mock_git_env):
    assert os.environ['GITHUB_REPOSITORY'] == 'test-org/test-repo'
```

#### branch_outputs
Provides sample branch command outputs:

```python
@pytest.fixture
def branch_outputs():
    """Provide sample git branch command outputs for testing."""
    return {
        'show_current': "feature/test-branch",
        'list_local': "* main\n  develop\n  feature/test-branch",
        'list_remote': "* main\n  develop\n  feature/test-branch\n  remotes/origin/main",
        'list_pattern': "  feature/test-branch\n  feature/another-branch"
    }
```

### Specialized Fixtures

Additional fixtures are available for specific testing scenarios:

- `mock_git_repo`: Simulates git repository structure
- `git_outputs`: General git command output samples
- `tag_outputs`: Sample outputs for tag operations
- `commit_outputs`: Sample outputs for commit operations

## Testing Patterns

### Unit Testing

Unit tests focus on testing individual methods and functions in isolation:

```python
@pytest.mark.unit
class TestGitBranchOperations:
    """Unit tests for GitBranchOperations class."""
    
    def test_create_branch_success(self, mock_subprocess, mock_git_env):
        """Test successful branch creation."""
        # Arrange
        branch_ops = GitBranchOperations()
        
        # Act
        result = branch_ops.create_branch('feature/test-branch', 'main')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace']),
            call(['git', 'checkout', 'main']),
            call(['git', 'pull', 'origin', 'main']),
            call(['git', 'checkout', '-b', 'feature/test-branch'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
```

#### Unit Test Best Practices

1. **Single Responsibility**: Test one function/method per test
2. **Clear Naming**: Use descriptive test names that explain the scenario
3. **AAA Pattern**: Arrange, Act, Assert structure
4. **Mock External Dependencies**: Use fixtures to mock subprocess, file operations
5. **Test Both Success and Failure**: Include error handling scenarios

### Integration Testing

Integration tests verify complete workflows and component interactions:

```python
@pytest.mark.integration
class TestBranchOperationsIntegration:
    """Integration tests for branch operations."""
    
    def test_branch_lifecycle(self, mock_subprocess, mock_git_env, branch_outputs):
        """Test the complete lifecycle of a branch: create, list, checkout, merge, delete."""
        # Arrange
        branch_ops = GitBranchOperations()
        branch_name = "feature/test-lifecycle"
        
        # Configure mock outputs for different stages
        mock_subprocess['check_output'].side_effect = [
            'main',                           # Current branch check during create
            branch_outputs['list_local'],     # List branches
            branch_name,                      # Current branch after checkout
            'main',                           # Current branch after merge
        ]
        
        # Act - Execute complete workflow
        create_result = branch_ops.create_branch(branch_name, 'main')
        list_result = branch_ops.list_branches()
        checkout_result = branch_ops.checkout_branch(branch_name)
        merge_result = branch_ops.merge_branch(branch_name, 'main')
        delete_result = branch_ops.delete_branch(branch_name)
        
        # Assert all operations were successful
        assert create_result is True
        assert 'main' in list_result
        assert checkout_result is True
        assert merge_result is True
        assert delete_result is True
```

#### Integration Test Best Practices

1. **End-to-End Flows**: Test complete user scenarios
2. **State Management**: Verify state changes throughout the workflow
3. **Error Propagation**: Test how errors flow through the system
4. **Resource Cleanup**: Ensure proper cleanup after test execution

### Main Function Testing

Test the entry point functions that handle GitHub Actions integration:

```python
@pytest.mark.unit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_create_action(self, mock_subprocess, mock_git_env):
        """Test create action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_BRANCH_NAME'] = 'feature/test-branch'
        os.environ['INPUT_BASE_BRANCH'] = 'develop'
        
        mock_subprocess['check_output'].return_value = 'feature/test-branch'
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'current_branch=feature/test-branch' in output
```

## Coverage Requirements

All actions must maintain minimum 80% code coverage:

### Running Coverage

```bash
# In action directory
pytest --cov=. --cov-report=xml --cov-report=term-missing

# Check coverage percentage
COVERAGE=$(python -c "import xml.etree.ElementTree as ET; tree = ET.parse('coverage.xml'); root = tree.getroot(); print(root.attrib['line-rate'])")
echo "Coverage: $(echo "$COVERAGE * 100" | bc)%"
```

### Coverage Validation

The test framework automatically validates coverage in CI:

```bash
if (( $(echo "$COVERAGE_PCT < 80" | bc -l) )); then
  echo "Error: Code coverage is below 80%"
  exit 1
fi
```

## CI/CD Integration

### Test Framework Workflow

**Location**: `.github/workflows/test.framework.yml`

The framework includes automated testing across all actions:

```yaml
strategy:
  matrix:
    action-path:
      - actions/core/branch_operations
      - actions/core/version_calculator
      - actions/core/version_updater
      - actions/core/manage_release

steps:
  - name: Run tests
    working-directory: ${{ matrix.action-path }}
    run: |
      pytest --cov=. --cov-report=xml --cov-report=term-missing
  
  - name: Verify coverage threshold
    working-directory: ${{ matrix.action-path }}
    run: |
      COVERAGE=$(python -c "import xml.etree.ElementTree as ET; tree = ET.parse('coverage.xml'); root = tree.getroot(); print(root.attrib['line-rate'])")
      COVERAGE_PCT=$(echo "$COVERAGE * 100" | bc)
      if (( $(echo "$COVERAGE_PCT < 80" | bc -l) )); then
        echo "Error: Code coverage is below 80%"
        exit 1
      fi
```

### Framework Validation

The workflow also validates the framework itself:

```yaml
- name: Validate test templates
  run: |
    python -c "import sys; import os; sys.path.append(os.path.join(os.getcwd(), 'actions/test_framework')); from test_templates import test_unit_template, test_integration_template; print('Test templates are valid')"
    
- name: Verify test documentation
  run: |
    if [ ! -f "actions/test_framework/README.md" ]; then
      echo "Error: Test framework documentation is missing"
      exit 1
    fi
```

## Setting Up Tests for New Actions

### 1. Create Test Structure

```bash
# From your action directory
mkdir -p tests
cp /path/to/test_framework/conftest.py tests/
cp /path/to/test_framework/pytest.ini ./
```

### 2. Create Unit Tests

```bash
cp /path/to/test_framework/test_templates/test_unit_template.py tests/test_unit.py
```

Customize the template for your specific action:

```python
# Import your action class
from main import YourActionClass

@pytest.mark.unit
class TestYourActionClass:
    """Unit tests for YourActionClass."""
    
    def test_your_method_success(self, mock_subprocess, mock_git_env):
        """Test successful execution of your method."""
        # Arrange
        action = YourActionClass()
        
        # Act
        result = action.your_method('test-input')
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_called_with(['expected', 'command'])
```

### 3. Create Integration Tests

```bash
cp /path/to/test_framework/test_templates/test_integration_template.py tests/test_integration.py
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit
pytest -m integration

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

## Testing Composite Actions

Composite Actions require different testing approaches:

### Mock Component Actions

```python
@pytest.fixture
def mock_composite_action():
    """Mock composite actions for testing interrelated actions."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "success"
        mock_run.return_value = mock_result
        yield mock_run

def test_composite_workflow(mock_composite_action, mock_git_env):
    """Test composite action workflow."""
    # Test the orchestration logic
    # Mock each component action
    # Verify proper parameter passing
```

### Test Action Orchestration

Focus on testing:
1. **Parameter Flow**: How inputs flow between actions
2. **Error Handling**: How failures in one action affect the workflow
3. **Conditional Logic**: Different execution paths based on inputs
4. **Output Aggregation**: How outputs are combined and reported

## Best Practices

### Test Organization

1. **Clear Structure**: Follow the standardized directory structure
2. **Descriptive Names**: Use clear, descriptive test method names
3. **Logical Grouping**: Group related tests in classes
4. **Consistent Markers**: Use appropriate pytest markers

### Test Quality

1. **Single Assertion Focus**: Each test should verify one specific behavior
2. **Independent Tests**: Tests should not depend on each other
3. **Deterministic Results**: Tests should produce consistent results
4. **Resource Cleanup**: Properly clean up any test artifacts

### Mock Usage

1. **Mock External Dependencies**: Always mock subprocess, file operations, network calls
2. **Realistic Mock Data**: Use realistic sample data in fixtures
3. **Verify Mock Calls**: Assert that mocks were called with expected parameters
4. **Configure Mock Behavior**: Set up mocks to return appropriate values

### Error Testing

1. **Test Failure Scenarios**: Include tests for error conditions
2. **Exception Handling**: Verify proper exception handling
3. **Error Messages**: Test that meaningful error messages are provided
4. **Exit Codes**: Verify correct exit codes for different scenarios

## Troubleshooting

### Common Issues

**Test Discovery Problems**:
- Ensure `pytest.ini` is configured correctly
- Check that test files follow naming conventions (`test_*.py`)
- Verify test classes start with `Test`

**Mock Configuration Issues**:
- Check that fixtures are properly imported
- Ensure mock return values match expected types
- Verify mock side effects are configured for multiple calls

**Coverage Issues**:
- Review uncovered lines in coverage reports
- Add tests for missing code paths
- Consider if some code should be excluded from coverage

### Debug Commands

```bash
# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/test_unit.py::TestClass::test_method

# Run tests with debug output
pytest -s

# Generate detailed coverage report
pytest --cov=. --cov-report=html
```

## Related Guides

- [Understanding Actions](understanding-actions.md) - Learn about the actions being tested
- [Understanding Workflows](understanding-workflows.md) - How actions integrate in workflows
- [Understanding FCM Bridge](understanding-fcm-bridge.md) - Testing generated actions

## Summary

The testing framework provides a comprehensive foundation for ensuring the reliability and quality of the GitHub Toolkit. By following the standardized patterns and leveraging the provided fixtures, developers can create robust test suites that maintain the 80% coverage requirement while providing confidence in the system's behavior.