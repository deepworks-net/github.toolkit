#!/usr/bin/env python3

import os
import re
import subprocess
from typing import Optional, List, Pattern, Tuple


class GitValidator:
    """
    Provides validation functions for Git operations.
    
    This class contains methods to validate Git references, paths,
    and other inputs to ensure they are safe and correct before
    performing Git operations.
    """
    
    def __init__(self):
        """Initialize the GitValidator."""
        pass
    
    def is_valid_repository(self) -> bool:
        """
        Check if the current directory is a valid Git repository.
        
        Returns:
            bool: True if valid repository, False otherwise
        """
        try:
            subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def is_valid_branch_name(self, branch_name: str) -> bool:
        """
        Validate a branch name according to Git's rules.
        
        Args:
            branch_name: The branch name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Git branch naming rules:
        # Cannot contain these characters: ~ ^ : ? * [ \ space
        # Cannot start with a -
        # Cannot be empty
        # Cannot contain double dots (..)
        
        if not branch_name:
            return False
            
        if branch_name.startswith('-'):
            return False
            
        if '..' in branch_name:
            return False
            
        # Check for invalid characters
        invalid_chars = r'[\s~^:?*[\]\\]'
        if re.search(invalid_chars, branch_name):
            return False
            
        return True
    
    def is_valid_tag_name(self, tag_name: str) -> bool:
        """
        Validate a tag name according to Git's rules.
        
        Args:
            tag_name: The tag name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Git tag naming rules are similar to branch names
        return self.is_valid_branch_name(tag_name)
    
    def branch_exists(self, branch_name: str, remote: bool = False) -> bool:
        """
        Check if a branch exists.
        
        Args:
            branch_name: The branch name to check
            remote: Whether to check remote branches
            
        Returns:
            bool: True if exists, False otherwise
        """
        try:
            if remote:
                cmd = ['git', 'ls-remote', '--heads', 'origin', branch_name]
                output = subprocess.check_output(cmd, text=True).strip()
                return bool(output)
            else:
                cmd = ['git', 'show-ref', '--verify', f'refs/heads/{branch_name}']
                subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                return True
        except subprocess.CalledProcessError:
            return False
    
    def tag_exists(self, tag_name: str, remote: bool = False) -> bool:
        """
        Check if a tag exists.
        
        Args:
            tag_name: The tag name to check
            remote: Whether to check remote tags
            
        Returns:
            bool: True if exists, False otherwise
        """
        try:
            if remote:
                cmd = ['git', 'ls-remote', '--tags', 'origin', tag_name]
                output = subprocess.check_output(cmd, text=True).strip()
                return bool(output)
            else:
                cmd = ['git', 'show-ref', '--verify', f'refs/tags/{tag_name}']
                subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                return True
        except subprocess.CalledProcessError:
            return False
    
    def commit_exists(self, commit_hash: str) -> bool:
        """
        Check if a commit exists.
        
        Args:
            commit_hash: The commit hash to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        try:
            cmd = ['git', 'rev-parse', '--verify', f'{commit_hash}^{{commit}}']
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def is_valid_file_path(self, file_path: str) -> bool:
        """
        Validate a file path.
        
        Args:
            file_path: The file path to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Check for potential command injection patterns
        dangerous_patterns = [
            ';', '&', '|', '>', '<', '`', '$', '(', ')', '{', '}', '[', ']',
            '&&', '||', '\n', '\r'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in file_path:
                return False
                
        # Check if the path is relative to the repository
        # This prevents operations on files outside the repository
        try:
            full_path = os.path.abspath(file_path)
            repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
            return full_path.startswith(repo_root)
        except subprocess.CalledProcessError:
            return False
    
    def is_valid_ref(self, ref: str) -> bool:
        """
        Check if a Git reference (branch, tag, or commit) is valid.
        
        Args:
            ref: The reference to check
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            cmd = ['git', 'rev-parse', '--verify', ref]
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def pattern_to_regex(self, pattern: str) -> Pattern:
        """
        Convert a Git-style pattern to a regex pattern.
        
        Args:
            pattern: Git-style pattern (with * and ? wildcards)
            
        Returns:
            Pattern: Compiled regex pattern
        """
        # Escape special regex chars except * and ?
        regex = re.escape(pattern)
        # Convert git wildcards to regex wildcards
        regex = regex.replace('\\*', '.*').replace('\\?', '.')
        # Ensure it matches the whole string
        regex = f'^{regex}$'
        return re.compile(regex)
    
    def safe_git_command(self, command: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate and execute a Git command safely.
        
        Args:
            command: The Git command as a list of arguments
            
        Returns:
            tuple: (success, output)
        """
        # Validate the command is a git command
        if not command or command[0] != 'git':
            return False, "Not a git command"
            
        # Check for dangerous arguments
        dangerous_args = ['--upload-pack', '--exec', '-c', '--config', '--git-dir', '--work-tree']
        for arg in command:
            if arg in dangerous_args or arg.startswith('--upload-pack='):
                return False, f"Potentially dangerous argument: {arg}"
                
        # Execute the command
        try:
            output = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
            return True, output
        except subprocess.CalledProcessError as e:
            return False, str(e)