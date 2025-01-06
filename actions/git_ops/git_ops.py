#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime

def setup_git():
    """Configure git settings."""
    try:
        subprocess.check_call(['git', 'config', '--local', 'user.email', 'action@github.com'])
        subprocess.check_call(['git', 'config', '--local', 'user.name', 'GitHub Action'])
        subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
    except subprocess.CalledProcessError as e:
        print(f"Error configuring git: {e}")
        sys.exit(1)

def delete_prep_tag():
    """Delete the prep tag as it's no longer needed."""
    try:
        print("Deleting prep tag...")
        subprocess.check_call(['git', 'push', 'origin', ':refs/tags/prep'])
    except subprocess.CalledProcessError as e:
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
            subprocess.check_call(['git', 'checkout', 'staging'])
            subprocess.check_call(['git', 'pull', 'origin', 'staging'])
            # Create release branch from staging
            subprocess.check_call(['git', 'checkout', '-b', branch_name])
            
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e}")
        sys.exit(1)

def commit_changes():
    """Commit specified files."""
    try:
        files = os.environ.get('FILES', '').split()
        message = os.environ.get('COMMIT_MESSAGE', 'Update from GitHub Action')
        
        # Add files
        for file in files:
            subprocess.check_call(['git', 'add', file])
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not result.stdout:
            print("No changes to commit")
            return False
            
        # Commit changes
        subprocess.check_call(['git', 'commit', '-m', message])
        return True
        
    except subprocess.CalledProcessError as e:
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