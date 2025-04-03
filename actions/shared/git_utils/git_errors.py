#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, Dict, List, Any


class GitErrors:
    """
    Handles common Git error cases.
    
    This class provides standardized error handling and reporting
    for Git operations, ensuring consistent behavior across actions.
    """
    
    def __init__(self, github_output: Optional[str] = None):
        """
        Initialize GitErrors with optional GitHub output path.
        
        Args:
            github_output: Path to GitHub output file. If not provided,
                          it will use the GITHUB_OUTPUT environment variable.
        """
        self.github_output = github_output or os.environ.get('GITHUB_OUTPUT')
        
        # Common error patterns and messages
        self.error_patterns = {
            'not a git repository': 'The current directory is not a Git repository.',
            'does not exist': 'The specified reference does not exist.',
            'already exists': 'The specified reference already exists.',
            'Permission denied': 'Permission denied. Check your credentials.',
            'remote: Repository not found': 'Repository not found. Check the repository URL.',
            'failed to push': 'Failed to push to remote. Try fetching changes first.',
            'cannot lock ref': 'Cannot lock reference. Another operation may be in progress.',
            'refusing to merge unrelated histories': 'Cannot merge unrelated histories. Use --allow-unrelated-histories.',
            'error: Your local changes': 'You have uncommitted changes. Commit or stash them first.',
            'fatal: empty ident': 'Git identity not configured. Run "git config --global user.name" and "git config --global user.email".',
            'fatal: bad revision': 'Invalid revision or reference provided.',
            'error: unknown switch': 'Invalid command option provided.',
            'fatal: Not a valid object name': 'The specified object name is not valid.',
            'fatal: path \'': 'File path not found or invalid.',
            'husky > pre-commit': 'Pre-commit hook failed. Check the error message for details.',
            'pre-commit hook': 'Pre-commit hook failed. Check the error message for details.',
            'fatal: could not read': 'Could not read from the repository. Check permissions.',
            'fatal: unable to access': 'Unable to access the repository. Check network and credentials.',
        }
    
    def _set_github_output(self, key: str, value: str) -> None:
        """
        Set a GitHub Actions output variable.
        
        Args:
            key: Output variable name
            value: Output variable value
        """
        if self.github_output:
            try:
                with open(self.github_output, 'a') as f:
                    f.write(f"{key}={value}\n")
            except Exception as e:
                print(f"Error setting GitHub output: {e}")
    
    def _get_detailed_error(self, error: subprocess.CalledProcessError) -> str:
        """
        Get a detailed error message from a CalledProcessError.
        
        Args:
            error: The subprocess.CalledProcessError
            
        Returns:
            str: Detailed error message
        """
        cmd = ' '.join(error.cmd) if isinstance(error.cmd, list) else error.cmd
        error_output = error.output.decode('utf-8') if isinstance(error.output, bytes) else str(error.output)
        
        # Look for known error patterns
        detailed_message = None
        for pattern, message in self.error_patterns.items():
            if pattern in error_output:
                detailed_message = message
                break
        
        # Construct full error message
        full_message = f"Command '{cmd}' failed with exit code {error.returncode}"
        if detailed_message:
            full_message += f": {detailed_message}"
        
        # Add error output if available
        if error_output:
            # Limit to first 500 characters to avoid overwhelming output
            truncated_output = error_output[:500]
            if len(error_output) > 500:
                truncated_output += "... (truncated)"
            full_message += f"\nError output:\n{truncated_output}"
        
        return full_message
    
    def handle_git_error(self, error: subprocess.CalledProcessError, 
                         context: Optional[str] = None,
                         exit_on_error: bool = False,
                         set_output: bool = True) -> str:
        """
        Handle a Git error with standard formatting and reporting.
        
        Args:
            error: The subprocess.CalledProcessError
            context: Additional context about the operation
            exit_on_error: Whether to exit the program on error
            set_output: Whether to set GitHub outputs
            
        Returns:
            str: Error message
        """
        # Get detailed error
        detailed_error = self._get_detailed_error(error)
        
        # Add context if provided
        if context:
            error_message = f"{context}: {detailed_error}"
        else:
            error_message = detailed_error
        
        # Print error
        print(f"Error: {error_message}")
        
        # Set GitHub outputs
        if set_output:
            self._set_github_output("result", "failure")
            self._set_github_output("error_message", error_message.replace("\n", "%0A"))
        
        # Exit if requested
        if exit_on_error:
            sys.exit(error.returncode or 1)
        
        return error_message
    
    def handle_checkout_error(self, error: subprocess.CalledProcessError, branch: str = "") -> str:
        """
        Handle Git checkout errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            branch: The branch being checked out
            
        Returns:
            str: Error message
        """
        context = f"Failed to checkout branch '{branch}'" if branch else "Failed to checkout branch"
        return self.handle_git_error(error, context)
    
    def handle_push_error(self, error: subprocess.CalledProcessError, ref: str = "") -> str:
        """
        Handle Git push errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            ref: The reference being pushed
            
        Returns:
            str: Error message
        """
        context = f"Failed to push '{ref}'" if ref else "Failed to push"
        return self.handle_git_error(error, context)
    
    def handle_merge_error(self, error: subprocess.CalledProcessError, source: str = "", target: str = "") -> str:
        """
        Handle Git merge errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            source: The source branch
            target: The target branch
            
        Returns:
            str: Error message
        """
        context = f"Failed to merge '{source}' into '{target}'" if source and target else "Failed to merge"
        return self.handle_git_error(error, context)
    
    def handle_tag_error(self, error: subprocess.CalledProcessError, action: str = "", tag: str = "") -> str:
        """
        Handle Git tag errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            action: The tag action (create, delete, etc.)
            tag: The tag name
            
        Returns:
            str: Error message
        """
        context = f"Failed to {action} tag '{tag}'" if action and tag else "Failed in tag operation"
        return self.handle_git_error(error, context)
    
    def handle_clone_error(self, error: subprocess.CalledProcessError, repo: str = "") -> str:
        """
        Handle Git clone errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            repo: The repository URL
            
        Returns:
            str: Error message
        """
        # Sanitize URL to remove tokens
        if repo:
            sanitized_repo = repo
            if '@' in repo:
                # Remove anything between :// and @
                parts = repo.split('@')
                protocol_parts = parts[0].split('://')
                if len(protocol_parts) > 1:
                    sanitized_repo = f"{protocol_parts[0]}://***@{parts[1]}"
            context = f"Failed to clone repository '{sanitized_repo}'"
        else:
            context = "Failed to clone repository"
            
        return self.handle_git_error(error, context)
    
    def handle_commit_error(self, error: subprocess.CalledProcessError, message: str = "") -> str:
        """
        Handle Git commit errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            message: The commit message
            
        Returns:
            str: Error message
        """
        # Truncate message if too long
        if message and len(message) > 30:
            short_message = message[:27] + "..."
            context = f"Failed to commit with message '{short_message}'"
        elif message:
            context = f"Failed to commit with message '{message}'"
        else:
            context = "Failed to commit"
            
        return self.handle_git_error(error, context)
    
    def handle_fetch_error(self, error: subprocess.CalledProcessError, remote: str = "") -> str:
        """
        Handle Git fetch errors specifically.
        
        Args:
            error: The subprocess.CalledProcessError
            remote: The remote name
            
        Returns:
            str: Error message
        """
        context = f"Failed to fetch from '{remote}'" if remote else "Failed to fetch"
        return self.handle_git_error(error, context)