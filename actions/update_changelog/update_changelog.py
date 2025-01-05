#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime
import json
import re

def setup_git():
    """Configure git to trust the workspace."""
    try:
        subprocess.check_output(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error configuring git: {e}")
        sys.exit(1)

def get_draft_release_content():
    """Fetch content from draft release using GitHub API."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not set")
        sys.exit(1)

    try:
        # Get repository information from environment
        repository = os.environ.get('GITHUB_REPOSITORY')
        if not repository:
            print("Error: GITHUB_REPOSITORY not set")
            sys.exit(1)

        # Use gh CLI to fetch draft release
        cmd = [
            'gh', 'api',
            '-H', 'Accept: application/vnd.github+json',
            f'repos/{repository}/releases',
            '--jq', '.[] | select(.draft == true) | .body'
        ]
        
        content = subprocess.check_output(cmd, text=True, env={'GITHUB_TOKEN': token})
        
        # Extract PR entries
        pr_entries = []
        for line in content.split('\n'):
            if line.strip().startswith('-'):
                pr_entries.append(line.strip())
        
        if not pr_entries:
            print("Warning: No content found in draft release")
            return None
            
        return '\n'.join(pr_entries)
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching draft release: {e}")
        sys.exit(1)

def update_changelog(content):
    """Update CHANGELOG.md with new content."""
    if not content:
        print("No content to update")
        return

    try:
        version = os.environ.get('VERSION', 'UNKNOWN')
        today = datetime.now().strftime("%m/%d/%Y")
        
        with open('CHANGELOG.md', 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        found_unreleased = False
        skip_old_unreleased = False
        
        # Process lines
        for line in lines:
            # Keep header content
            if not found_unreleased and not line.startswith('## '):
                new_lines.append(line)
                continue
                
            # Handle unreleased section
            if re.search(r'## \*\*.*[Uu]nreleased\*\*', line):
                found_unreleased = True
                new_lines.append(f'## **{today} - {version} Unreleased**\n')
                new_lines.append(content + '\n')
                skip_old_unreleased = True
                continue
            
            # Skip old unreleased content until we hit next section
            if skip_old_unreleased:
                if line.startswith('## '):
                    skip_old_unreleased = False
                    new_lines.append('\n')  # Add extra newline before first release
                else:
                    continue
                    
            # Add versioned sections and other content
            new_lines.append(line)
        
        # Add unreleased section at end if not found
        if not found_unreleased:
            if new_lines and new_lines[-1] != '\n':
                new_lines.append('\n')
            new_lines.append(f'## **{today} - {version} Unreleased**\n')
            new_lines.append(content + '\n')
        
        # Write updated changelog
        with open('CHANGELOG.md', 'w') as f:
            f.writelines(new_lines)
            
        # Commit changes
        subprocess.check_call(['git', 'config', '--local', 'user.email', 'action@github.com'])
        subprocess.check_call(['git', 'config', '--local', 'user.name', 'GitHub Action'])
        subprocess.check_call(['git', 'add', 'CHANGELOG.md'])
        subprocess.check_call(['git', 'commit', '-m', 'Update CHANGELOG.md to match draft release content [skip ci]'])
        subprocess.check_call(['git', 'push', 'origin', 'staging'])
        
    except Exception as e:
        print(f"Error updating changelog: {e}")
        sys.exit(1)

def main():
    """Main function."""
    setup_git()
    content = get_draft_release_content()
    update_changelog(content)

if __name__ == "__main__":
    main()