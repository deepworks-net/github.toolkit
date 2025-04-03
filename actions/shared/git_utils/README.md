# Git Utilities

Shared utilities for Git operations across all actions in the GitHub toolkit.

## Purpose

This module provides common Git functions and utilities that can be reused across different actions to avoid duplication and ensure consistent behavior.

## Components

### GitConfig

Handles Git configuration operations:

- Setting up Git identity
- Configuring safe directories
- Setting Git environment variables

### GitValidator

Provides validation functions:

- Validating Git repository
- Validating Git references (branches, tags, commits)
- Validating paths and file patterns

### GitErrors

Common error handling for Git operations:

- Standardized error messages
- Error categorization
- Proper exit status codes

## Usage

```python
from git_utils import GitConfig, GitValidator, GitErrors

# Configure Git
git_config = GitConfig()
git_config.setup_identity()

# Validate a reference
validator = GitValidator()
if not validator.is_valid_branch("feature/my-branch"):
    print("Invalid branch name")
    sys.exit(1)

# Handle errors
try:
    # Git operation
    subprocess.check_call(["git", "checkout", "branch"])
except subprocess.CalledProcessError as e:
    error_handler = GitErrors()
    error_handler.handle_checkout_error(e)
```

## Integration with Actions

To use these utilities in an action:

1. Import the required modules
2. Create instances of the utility classes
3. Use the provided methods instead of duplicating Git command logic

This ensures consistency across all Git-related actions and reduces code duplication.

## Error Handling

The utilities provide standardized error handling for common Git operations, ensuring that:

- Error messages are consistent and informative
- Proper exit codes are used
- Context is provided where possible
- GitHub Actions outputs are set appropriately