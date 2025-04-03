#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, Dict, List, Tuple


class GitConfig:
    """
    Handles common Git configuration operations.
    
    This class provides methods to configure Git for use in GitHub Actions,
    including setting up identity, configuring safe directories, and handling
    common configuration issues.
    """
    
    def __init__(self, workspace_path: Optional[str] = None):
        """
        Initialize GitConfig with optional workspace path.
        
        Args:
            workspace_path: Path to the GitHub workspace. If not provided,
                           it will use the GITHUB_WORKSPACE environment variable.
        """
        self.workspace_path = workspace_path or os.environ.get('GITHUB_WORKSPACE', '/github/workspace')
        self._verify_git_installed()
    
    def _verify_git_installed(self) -> None:
        """
        Verify that Git is installed and available.
        
        Raises:
            SystemExit: If Git is not installed
        """
        try:
            subprocess.check_output(['git', '--version'], stderr=subprocess.STDOUT)
        except FileNotFoundError:
            print("Error: Git is not installed. Please ensure git is available in the container.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error checking git version: {e}")
            sys.exit(1)
    
    def setup_identity(self, name: Optional[str] = None, 
                      email: Optional[str] = None, 
                      force: bool = False) -> bool:
        """
        Set up Git user identity.
        
        Args:
            name: Git user name. If not provided, it will use GitHub Actions as default.
            email: Git user email. If not provided, it will use github-actions@github.com as default.
            force: Whether to force set the identity even if it's already configured.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Default values
            default_name = "GitHub Actions"
            default_email = "github-actions@github.com"
            
            # Use provided values or defaults
            git_name = name or default_name
            git_email = email or default_email
            
            # Check if identity is already configured
            if not force:
                try:
                    current_name = subprocess.check_output(['git', 'config', 'user.name'], text=True, stderr=subprocess.STDOUT).strip()
                    current_email = subprocess.check_output(['git', 'config', 'user.email'], text=True, stderr=subprocess.STDOUT).strip()
                    
                    # If both are already set, return success
                    if current_name and current_email:
                        return True
                except subprocess.CalledProcessError:
                    # Identity not configured, continue with setup
                    pass
            
            # Set user name and email
            subprocess.check_call(['git', 'config', '--global', 'user.name', git_name])
            subprocess.check_call(['git', 'config', '--global', 'user.email', git_email])
            
            print(f"Configured Git identity: {git_name} <{git_email}>")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git identity: {e}")
            return False
    
    def configure_safe_directory(self, directory: Optional[str] = None) -> bool:
        """
        Configure a directory as safe for Git.
        
        Args:
            directory: The directory to mark as safe. If not provided,
                     it will use the workspace path.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            safe_dir = directory or self.workspace_path
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', safe_dir])
            print(f"Configured safe directory: {safe_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error configuring safe directory: {e}")
            return False
    
    def configure_git_env(self, env_vars: Dict[str, str]) -> bool:
        """
        Configure Git environment variables.
        
        Args:
            env_vars: Dictionary of environment variables to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            for key, value in env_vars.items():
                os.environ[key] = value
                
            return True
        except Exception as e:
            print(f"Error configuring git environment: {e}")
            return False
    
    def setup_github_token(self, token: Optional[str] = None) -> bool:
        """
        Set up GitHub token for authentication.
        
        Args:
            token: GitHub token. If not provided, it will try to use the GITHUB_TOKEN environment variable.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get token from input or environment
            github_token = token or os.environ.get('GITHUB_TOKEN')
            
            if not github_token:
                print("Warning: No GitHub token provided. Some operations may fail.")
                return False
            
            # Extract the repository from the environment
            github_repository = os.environ.get('GITHUB_REPOSITORY')
            
            if not github_repository:
                print("Warning: GITHUB_REPOSITORY environment variable not set.")
                return False
            
            # Configure Git to use the token
            auth_url = f"https://x-access-token:{github_token}@github.com/{github_repository}.git"
            subprocess.check_call(['git', 'remote', 'set-url', 'origin', auth_url])
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting up GitHub token: {e}")
            return False
    
    def setup_git_config(self, options: Dict[str, str], scope: str = 'global') -> bool:
        """
        Set up multiple Git configuration options.
        
        Args:
            options: Dictionary of Git configuration options
            scope: Scope of the configuration (global, system, local)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            for key, value in options.items():
                subprocess.check_call(['git', 'config', f'--{scope}', key, value])
                
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting git config options: {e}")
            return False
    
    def is_inside_work_tree(self) -> bool:
        """
        Check if the current directory is inside a Git work tree.
        
        Returns:
            bool: True if inside a Git work tree, False otherwise
        """
        try:
            result = subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'], text=True).strip()
            return result == 'true'
        except subprocess.CalledProcessError:
            return False