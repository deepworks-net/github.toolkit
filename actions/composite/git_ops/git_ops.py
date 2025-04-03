#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime
import importlib.util
from pathlib import Path

# Dynamic imports for git operations modules
def import_module(module_path, module_name):
    """Dynamically import a module from a specific path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Set paths
current_dir = Path(__file__).parent
branch_module_path = current_dir / "branch" / "src" / "git_branch_operations.py"
commit_module_path = current_dir / "commit" / "src" / "git_commit_operations.py"
tag_module_path = current_dir / "tag" / "src" / "git_tag_operations.py"

# Import modules
try:
    branch_module = import_module(branch_module_path, "git_branch_operations")
    commit_module = import_module(commit_module_path, "git_commit_operations")
    tag_module = import_module(tag_module_path, "git_tag_operations")
    
    # Create operation objects
    branch_ops = branch_module.GitBranchOperations()
    commit_ops = commit_module.GitCommitOperations()
    tag_ops = tag_module.GitTagOperations()
except Exception as e:
    print(f"Error importing git operation modules: {e}")
    sys.exit(1)

def setup_git():
    """Configure git settings."""
    try:
        subprocess.check_call(['git', 'config', '--local', 'user.email', 'action@github.com'])
        subprocess.check_call(['git', 'config', '--local', 'user.name', 'GitHub Action'])
        # The individual modules already handle safe.directory configuration
    except subprocess.CalledProcessError as e:
        print(f"Error configuring git: {e}")
        sys.exit(1)

def delete_prep_tag():
    """Delete the prep tag as it's no longer needed."""
    try:
        print("Deleting prep tag...")
        tag_ops.delete_tag('prep', remote=True)
    except Exception as e:
        print(f"Warning: Failed to delete prep tag: {e}")
        # Don't exit with error as this is not critical

def create_branch():
    """Create and checkout branch if specified."""
    try:
        branch_name = os.environ.get('BRANCH_NAME')
        if not branch_name:
            # If no branch specified and creating PR, generate release branch name
            if os.environ.get('CREATE_PR', 'false').lower() == 'true':
                version = os.environ.get('PR_TITLE', '').replace('Release ', '')
                branch_name = f'release/{version}'
        
        if branch_name:
            print(f"Creating branch: {branch_name}")
            # First ensure we have latest staging
            branch_ops.checkout_branch('staging')
            subprocess.check_call(['git', 'pull', 'origin', 'staging'])
            # Create release branch from staging
            branch_ops.checkout_branch(branch_name, create=True)
            
    except Exception as e:
        print(f"Error creating branch: {e}")
        sys.exit(1)

def commit_changes():
    """Commit specified files."""
    try:
        files = os.environ.get('FILES', '').split() if os.environ.get('FILES') else None
        message = os.environ.get('COMMIT_MESSAGE', 'Update from GitHub Action')
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not result.stdout and not files:
            print("No changes to commit")
            return False
        
        # Use commit operations to create commit
        result = commit_ops.create_commit(
            message=message,
            files=files,
            all_changes=not files  # If no files specified, commit all changes
        )
        
        return result
        
    except Exception as e:
        print(f"Error committing changes: {e}")
        sys.exit(1)

def push_changes():
    """Push changes to remote."""
    try:
        branch = os.environ.get('BRANCH_NAME') or subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        subprocess.check_call(['git', 'push', 'origin', branch])
    except subprocess.CalledProcessError as e:
        print(f"Error pushing changes: {e}")
        sys.exit(1)

def create_pr():
    """Create pull request if specified."""
    if os.environ.get('CREATE_PR', 'false').lower() != 'true':
        return

    try:
        title = os.environ.get('PR_TITLE', os.environ.get('COMMIT_MESSAGE'))
        body = os.environ.get('PR_BODY', '')
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], text=True).strip()
        
        cmd = ['gh', 'pr', 'create',
               '--fill',
               '--base', 'main',
               '--head', branch,  # Explicitly specify the head branch
               '--title', title]
               
        if body:
            cmd.extend(['--body', body])
            
        subprocess.check_call(cmd)
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating PR: {e}")
        sys.exit(1)

def main():
    """Main function."""
    setup_git()
    create_branch()
    if commit_changes():
        push_changes()  # Make sure branch is pushed first
        if os.environ.get('CREATE_PR', 'false').lower() == 'true':
            # Add a small delay to ensure branch is available
            subprocess.run(['sleep', '2'])  # Give GitHub a moment to register the branch
            create_pr()
            delete_prep_tag()  # clean up the prep tag

if __name__ == "__main__":
    main()