#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, List, Dict, Union, Tuple

class GitBranchOperations:
    """Handles atomic Git branch operations."""
    
    def __init__(self):
        self._configure_git()
    
    def _configure_git(self) -> None:
        """Configure git for safe directory operations."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git: {e}")
            sys.exit(1)
    
    def create_branch(self, branch_name: str, base_branch: Optional[str] = 'main') -> bool:
        """
        Create a new git branch.
        
        Args:
            branch_name: The name of the branch to create
            base_branch: The branch to base the new branch on
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First ensure we have latest of base branch
            subprocess.check_call(['git', 'checkout', base_branch])
            subprocess.check_call(['git', 'pull', 'origin', base_branch])
            
            # Create new branch
            subprocess.check_call(['git', 'checkout', '-b', branch_name])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating branch {branch_name}: {e}")
            return False
    
    def delete_branch(self, branch_name: str, remote: bool = False, force: bool = False) -> bool:
        """
        Delete a git branch locally and optionally from remote.
        
        Args:
            branch_name: The name of the branch to delete
            remote: Whether to also delete from remote
            force: Whether to force delete even if not merged
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Make sure we're not on the branch we're trying to delete
            current_branch = self.get_current_branch()
            if current_branch == branch_name:
                subprocess.check_call(['git', 'checkout', 'main'])
            
            # Delete local branch
            delete_flag = '-D' if force else '-d'
            subprocess.check_call(['git', 'branch', delete_flag, branch_name])
            
            # Delete remote branch if requested
            if remote:
                subprocess.check_call(['git', 'push', 'origin', f'--delete', branch_name])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error deleting branch {branch_name}: {e}")
            return False
    
    def checkout_branch(self, branch_name: str, force: bool = False) -> bool:
        """
        Checkout a specific branch.
        
        Args:
            branch_name: The name of the branch to checkout
            force: Whether to force checkout (discard local changes)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cmd = ['git', 'checkout']
            if force:
                cmd.append('-f')
            cmd.append(branch_name)
            
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error checking out branch {branch_name}: {e}")
            return False
    
    def merge_branch(self, branch_name: str, base_branch: Optional[str] = None, 
                   message: Optional[str] = None, force: bool = False) -> bool:
        """
        Merge specified branch into current or specified branch.
        
        Args:
            branch_name: The name of the branch to merge
            base_branch: The branch to merge into (if None, uses current)
            message: Custom commit message for the merge
            force: Whether to force merge (resolve conflicts with ours)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # If base branch specified, check it out first
            if base_branch:
                if not self.checkout_branch(base_branch):
                    return False
            
            # Prepare merge command
            cmd = ['git', 'merge']
            
            if message:
                cmd.extend(['-m', message])
                
            if force:
                cmd.append('--strategy=recursive')
                cmd.append('--strategy-option=theirs')
                
            cmd.append(branch_name)
            
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error merging branch {branch_name}: {e}")
            return False
    
    def list_branches(self, pattern: Optional[str] = None, include_remote: bool = False) -> List[str]:
        """
        List all branches, optionally filtered by pattern.
        
        Args:
            pattern: Optional pattern to filter branches
            include_remote: Whether to include remote branches
            
        Returns:
            list: List of branch names
        """
        try:
            cmd = ['git', 'branch']
            
            if include_remote:
                cmd.append('-a')
                
            if pattern:
                cmd.extend(['--list', pattern])
                
            output = subprocess.check_output(cmd, text=True)
            
            # Clean up branch names (remove leading whitespace and asterisks)
            branches = []
            for line in output.strip().split('\n'):
                if line:
                    # Remove leading whitespace, asterisk, and remote prefix
                    branch = line.strip()
                    if branch.startswith('*'):
                        branch = branch[1:].strip()
                    # Filter out remote tracking branches if not wanted
                    if include_remote or not branch.startswith('remotes/'):
                        branches.append(branch)
            
            return branches
        except subprocess.CalledProcessError as e:
            print(f"Error listing branches: {e}")
            return []
    
    def get_current_branch(self) -> str:
        """
        Get the name of the current branch.
        
        Returns:
            str: Current branch name
        """
        try:
            return subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting current branch: {e}")
            return ""
    
    def push_branch(self, branch_name: Optional[str] = None, force: bool = False) -> bool:
        """
        Push a branch to remote.
        
        Args:
            branch_name: The name of the branch to push (if None, uses current)
            force: Whether to force push
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not branch_name:
                branch_name = self.get_current_branch()
                
            cmd = ['git', 'push', 'origin']
            
            if force:
                cmd.append('--force')
                
            cmd.append(branch_name)
            
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pushing branch {branch_name}: {e}")
            return False


def main():
    """Main entry point for the action."""
    branch_ops = GitBranchOperations()
    
    # Get inputs
    action = os.environ.get('INPUT_ACTION')
    branch_name = os.environ.get('INPUT_BRANCH_NAME')
    base_branch = os.environ.get('INPUT_BASE_BRANCH', 'main')
    force = os.environ.get('INPUT_FORCE', 'false').lower() == 'true'
    message = os.environ.get('INPUT_MESSAGE')
    pattern = os.environ.get('INPUT_PATTERN')
    remote = os.environ.get('INPUT_REMOTE', 'false').lower() == 'true'
    
    result = False
    output = None
    current_branch = branch_ops.get_current_branch()
    
    # Execute requested operation
    if action == 'create':
        if not branch_name:
            print("Error: branch_name is required for create action")
            sys.exit(1)
        result = branch_ops.create_branch(branch_name, base_branch)
        if result:
            current_branch = branch_name
            if remote:
                result = branch_ops.push_branch(branch_name)
    
    elif action == 'delete':
        if not branch_name:
            print("Error: branch_name is required for delete action")
            sys.exit(1)
        result = branch_ops.delete_branch(branch_name, remote, force)
        if result:
            current_branch = branch_ops.get_current_branch()
    
    elif action == 'checkout':
        if not branch_name:
            print("Error: branch_name is required for checkout action")
            sys.exit(1)
        result = branch_ops.checkout_branch(branch_name, force)
        if result:
            current_branch = branch_name
    
    elif action == 'merge':
        if not branch_name:
            print("Error: branch_name is required for merge action")
            sys.exit(1)
        result = branch_ops.merge_branch(branch_name, base_branch, message, force)
        current_branch = branch_ops.get_current_branch()
    
    elif action == 'list':
        branches = branch_ops.list_branches(pattern, remote)
        output = branches
        result = True
    
    elif action == 'push':
        result = branch_ops.push_branch(branch_name, force)
        current_branch = branch_ops.get_current_branch()
    
    else:
        print(f"Invalid action: {action}")
        sys.exit(1)
    
    # Set outputs
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        if output is not None and isinstance(output, list):
            f.write(f"branches={','.join(output)}\n")
        
        f.write(f"result={'success' if result else 'failure'}\n")
        f.write(f"current_branch={current_branch}\n")
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()