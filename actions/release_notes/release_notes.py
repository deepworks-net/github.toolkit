#!/usr/bin/env python3

import os
import sys
import subprocess
import json

def setup_git():
    """Configure git for workspace."""
    try:
        subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
    except subprocess.CalledProcessError as e:
        print(f"Error configuring git: {e}")
        sys.exit(1)

def get_draft_release():
    """Get current draft release content."""
    try:
        cmd = [
            'gh', 'api',
            '-H', 'Accept: application/vnd.github+json',
            f'repos/{os.environ["GITHUB_REPOSITORY"]}/releases',
            '--jq', '.[] | select(.draft == true)'
        ]
        
        # Set both tokens for gh cli
        env = {
            'GITHUB_TOKEN': os.environ['GITHUB_TOKEN'],
            'GH_TOKEN': os.environ['GITHUB_TOKEN']  # Add this line
        }
        
        result = subprocess.check_output(cmd, text=True, env=env)
        return json.loads(result) if result else None
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching draft release: {e}")
        sys.exit(1)

def extract_pr_entries(content):
    """Extract PR entries from content."""
    entries = []
    for line in content.split('\n'):
        if line.strip().startswith('-'):
            entries.append(line.strip())
    return entries

def create_draft_release():
    """Create new draft release."""
    try:
        cmd = [
            'gh', 'api',
            '--method', 'POST',
            f'repos/{os.environ["GITHUB_REPOSITORY"]}/releases',
            '-f', 'tag_name=DRAFT',
            '-f', 'name=Draft Release',
            '-F', 'draft=true',
            '-f', 'body= '
        ]
        
        subprocess.check_call(cmd)
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating draft release: {e}")
        sys.exit(1)

def update_draft_release(content):
    """Update draft release with new content."""
    try:
        draft = get_draft_release()
        if not draft:
            create_draft_release()
            draft = get_draft_release()
            
        if not draft:
            print("Failed to create/get draft release")
            sys.exit(1)
            
        cmd = [
            'gh', 'api',
            '--method', 'PATCH',
            f'repos/{os.environ["GITHUB_REPOSITORY"]}/releases/{draft["id"]}',
            '-f', f'body={content}'
        ]
        
        subprocess.check_call(cmd)
        
    except subprocess.CalledProcessError as e:
        print(f"Error updating draft release: {e}")
        sys.exit(1)

def handle_pr_merge():
    """Handle PR merge mode."""
    pr_number = os.environ.get('PR_NUMBER')
    pr_title = os.environ.get('PR_TITLE')
    
    if not pr_number or not pr_title:
        print("Missing PR information")
        sys.exit(1)
        
    draft = get_draft_release()
    current_entries = []
    if draft and draft['body']:
        current_entries = extract_pr_entries(draft['body'])
    
    # Add new PR entry at the beginning
    new_entry = f"- PR #{pr_number}: {pr_title}"
    entries = [new_entry] + current_entries
    
    content = '\n'.join(entries)
    update_draft_release(content)
    print(f"::set-output name=content::{content}")

def handle_prepare_release():
    """Handle prepare-release mode."""
    draft = get_draft_release()
    if not draft:
        print("No draft release found")
        sys.exit(1)
        
    content = draft['body'].strip()
    if not content:
        print("Warning: Draft release is empty")
        sys.exit(1)
        
    entries = extract_pr_entries(content)
    if not entries:
        print("Warning: No PR entries found in draft release")
        sys.exit(1)
        
    content = '\n'.join(entries)
    print(f"::set-output name=content::{content}")

def main():
    """Main function."""
    setup_git()
    
    mode = os.environ.get('MODE')
    if not mode:
        print("MODE environment variable not set")
        sys.exit(1)
    
    if mode == 'pr-merge':
        handle_pr_merge()
    elif mode == 'prepare-release':
        handle_prepare_release()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
