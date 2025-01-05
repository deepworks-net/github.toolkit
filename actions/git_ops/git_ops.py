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

def create_branch():
    """Create and checkout branch if specified."""
    branch_name = os.environ.get('BRANCH_NAME')
    if branch_name:
        try:
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
        base = os.environ.get('BASE_BRANCH', 'staging')
        title = os.environ.get('PR_TITLE', os.environ.get('COMMIT_MESSAGE'))
        body = os.environ.get('PR_BODY', '')
        
        cmd = ['gh', 'pr', 'create',
               '--fill',
               '--base', base,
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
        push_changes()
        create_pr()

if __name__ == "__main__":
    main()