# Git Utilities

A shared library of Git utility functions for use across all Git-related actions.

## Overview

The Git Utilities module provides standardized implementations of common Git operations, reducing code duplication and ensuring consistent behavior across all actions in the toolkit. It serves as the foundation for the core/composite pattern by extracting common functionality into reusable components.

## Components

### GitConfig

Manages Git configuration operations:

```python
from git_utils import GitConfig

# Create a GitConfig instance
git_config = GitConfig()

# Set up Git identity
git_config.setup_identity(name="GitHub Actions", email="github-actions@github.com")

# Configure safe directory
git_config.configure_safe_directory('/github/workspace')

# Set up GitHub token authentication
git_config.setup_github_token()
```

#### Key Methods

- `setup_identity(name, email, force)`: Sets the Git user.name and user.email
- `configure_safe_directory(directory)`: Marks a directory as safe for Git operations
- `setup_github_token(token)`: Configures Git to use a GitHub token for authentication
- `setup_git_config(options, scope)`: Sets multiple Git configuration options
- `is_inside_work_tree()`: Checks if the current directory is inside a Git repository

### GitValidator

Provides validation functions for Git operations:

```python
from git_utils import GitValidator

# Create a validator instance
validator = GitValidator()

# Validate a branch name
if validator.is_valid_branch_name("feature/new-feature"):
    print("Branch name is valid")

# Check if a tag exists
if validator.tag_exists("v1.0.0"):
    print("Tag exists")

# Convert a Git pattern to regex
pattern = validator.pattern_to_regex("v1.*")
```

#### Key Methods

- `is_valid_repository()`: Checks if the current directory is a valid Git repository
- `is_valid_branch_name(branch_name)`: Validates a branch name against Git's rules
- `is_valid_tag_name(tag_name)`: Validates a tag name against Git's rules
- `branch_exists(branch_name, remote)`: Checks if a branch exists locally or remotely
- `tag_exists(tag_name, remote)`: Checks if a tag exists locally or remotely
- `commit_exists(commit_hash)`: Checks if a commit exists in the repository
- `is_valid_file_path(file_path)`: Validates a file path for safety
- `pattern_to_regex(pattern)`: Converts a Git-style pattern to a regex pattern

### GitErrors

Provides standardized error handling for Git operations:

```python
from git_utils import GitErrors

# Create an error handler
error_handler = GitErrors()

try:
    # Git operation
    subprocess.check_call(["git", "checkout", "branch"])
except subprocess.CalledProcessError as e:
    # Handle the error
    error_handler.handle_checkout_error(e, "branch-name")
```

#### Key Methods

- `handle_git_error(error, context, exit_on_error, set_output)`: Generic error handler
- `handle_checkout_error(error, branch)`: Specific handler for checkout errors
- `handle_push_error(error, ref)`: Specific handler for push errors
- `handle_merge_error(error, source, target)`: Specific handler for merge errors
- `handle_tag_error(error, action, tag)`: Specific handler for tag operation errors
- `handle_commit_error(error, message)`: Specific handler for commit errors

## Using Git Utilities in Actions

### Integration with Core Actions

```python
#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, List

# Import shared git utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../shared')))
from git_utils import GitConfig, GitValidator, GitErrors

class MyGitAction:
    """Custom Git operation action."""
    
    def __init__(self):
        """Initialize with git configuration."""
        self.git_config = GitConfig()
        self.git_validator = GitValidator()
        self.git_errors = GitErrors()
        
        # Configure git environment
        self.git_config.setup_identity()
        self.git_config.configure_safe_directory()
    
    def my_operation(self, param: str) -> bool:
        """
        Perform a custom Git operation.
        
        Args:
            param: Operation parameter
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.git_validator.is_valid_branch_name(param):
            print(f"Invalid parameter: {param}")
            return False
            
        try:
            # Git operation
            subprocess.check_call(['git', 'operation', param])
            return True
        except subprocess.CalledProcessError as e:
            self.git_errors.handle_git_error(e, f"Error in operation with {param}")
            return False
```

### Best Practices

1. **Always validate inputs**: Use the validator before performing operations
2. **Handle errors consistently**: Use the appropriate error handler methods
3. **Set up Git environment**: Configure Git identity and safe directories
4. **Use with GitHub Actions outputs**: The error handlers can set GitHub outputs

## Error Handling

The GitErrors class provides standardized error handling and reporting for Git operations. It handles common error patterns and provides user-friendly error messages.

### Example Error Messages

| Git Error | Friendly Message |
|-----------|------------------|
| not a git repository | The current directory is not a Git repository. |
| does not exist | The specified reference does not exist. |
| already exists | The specified reference already exists. |
| Permission denied | Permission denied. Check your credentials. |
| refusing to merge unrelated histories | Cannot merge unrelated histories. Use --allow-unrelated-histories. |

### GitHub Actions Integration

When used in GitHub Actions, the error handlers can automatically set outputs:

```
result=failure
error_message=Failed to checkout branch 'main': The specified branch does not exist.
```

## Testing Git Utilities

The Git Utilities are designed to be easily testable:

```python
def test_git_config(mocker):
    # Mock subprocess
    mock_check_call = mocker.patch('subprocess.check_call')
    mock_check_output = mocker.patch('subprocess.check_output')
    
    # Create GitConfig instance
    git_config = GitConfig()
    
    # Test setup_identity
    git_config.setup_identity("Test User", "test@example.com")
    
    # Assert calls
    mock_check_call.assert_any_call(['git', 'config', '--global', 'user.name', 'Test User'])
```

## Future Improvements

Planned enhancements for the Git Utilities:

1. **Performance optimization**: Caching for repeated validation calls
2. **Extended validation**: More comprehensive input validation
3. **Security improvements**: Additional safety checks for file paths
4. **Language support**: Multilingual error messages
5. **Async operations**: Support for asynchronous Git operations