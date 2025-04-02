# Branch Operations Tests

This page describes the testing approach for the Branch Operations action.

## Test Structure

The Branch Operations action follows the standard testing framework with:

1. **Unit Tests** - Testing individual functions in isolation
2. **Integration Tests** - Testing the action as a whole
3. **Mocked Git Operations** - Using pytest fixtures to avoid actual git calls

## Running Tests

```bash
# Navigate to action directory
cd actions/core/branch_operations

# Run all tests
python -m pytest

# Run only unit tests
python -m pytest -m unit

# Run only integration tests
python -m pytest -m integration

# Run with coverage
python -m pytest --cov=. --cov-report=term-missing
```

## Test Cases

### Unit Tests

| Test | Description |
|------|-------------|
| `test_create_branch_success` | Verify branch creation works |
| `test_delete_branch_success` | Verify branch deletion works |
| `test_delete_current_branch` | Test behavior when deleting current branch |
| `test_delete_remote_branch` | Test remote branch deletion |
| `test_list_branches` | Test branch listing functionality |
| `test_list_branches_with_pattern` | Test pattern-based branch filtering |
| `test_checkout_branch` | Test branch checkout |
| `test_merge_branch` | Test branch merging |
| `test_create_action` | Test create action in main function |
| `test_list_action` | Test list action in main function |

### Integration Tests

| Test | Description |
|------|-------------|
| `test_branch_lifecycle` | End-to-end test of branch creation, listing, checkout, merge, and deletion |
| `test_remote_operations` | Test remote branch operations |
| `test_force_operations` | Test force flags for various operations |

## Test Fixtures

The tests use several fixtures from the standard testing framework:

1. `mock_subprocess` - Mocks subprocess calls to git
2. `mock_git_env` - Sets up GitHub Actions environment variables
3. `branch_outputs` - Provides sample branch command outputs

## Example Test

```python
def test_create_branch_success(mock_subprocess, mock_git_env):
    """Test successful branch creation."""
    # Arrange
    branch_ops = GitBranchOperations()
    
    # Act
    result = branch_ops.create_branch('feature/test-branch', 'main')
    
    # Assert
    assert result is True
    assert mock_subprocess['check_call'].call_count == 3
    expected_calls = [
        call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace']),
        call(['git', 'checkout', 'main']),
        call(['git', 'pull', 'origin', 'main']),
        call(['git', 'checkout', '-b', 'feature/test-branch'])
    ]
    mock_subprocess['check_call'].assert_has_calls(expected_calls)
```