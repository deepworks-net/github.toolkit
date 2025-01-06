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
    token = os.environ.get('INPUT_GITHUB_TOKEN')  # Note: this is how the input is passed
    if not token:
        print("Error: github-token input not set")
        sys.exit(1)

    try:
        # Get repository information from environment
        repository = os.environ.get('GITHUB_REPOSITORY')
        if not repository:
            print("Error: GITHUB_REPOSITORY not set")
            sys.exit(1)

        # Use curl instead of gh cli
        cmd = [
            'curl', '-s',
            '-H', f'Authorization: token {token}',
            '-H', 'Accept: application/vnd.github+json',
            f'https://api.github.com/repos/{repository}/releases'
        ]
        
        result = subprocess.check_output(cmd, text=True)
        releases = json.loads(result)
        
        # Find draft release
        draft = next((r for r in releases if r.get('draft', False)), None)
        return draft
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching draft release: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing API response: {e}")
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
        token = os.environ.get('INPUT_GITHUB_TOKEN')
        cmd = [
            'curl', '-s',
            '-X', 'POST',
            '-H', f'Authorization: token {token}',
            '-H', 'Accept: application/vnd.github+json',
            f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/releases',
            '-d', json.dumps({
                'tag_name': 'DRAFT',
                'name': 'Draft Release',
                'draft': True,
                'body': ' '
            })
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
            
        token = os.environ.get('INPUT_GITHUB_TOKEN')
        cmd = [
            'curl', '-s',
            '-X', 'PATCH',
            '-H', f'Authorization: token {token}',
            '-H', 'Accept: application/vnd.github+json',
            f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/releases/{draft["id"]}',
            '-d', json.dumps({'body': content})
        ]
        
        subprocess.check_call(cmd)
        
    except subprocess.CalledProcessError as e:
        print(f"Error updating draft release: {e}")
        sys.exit(1)

def handle_pr_merge():
    """Handle PR merge mode."""
    pr_number = os.environ.get('INPUT_PR_NUMBER')
    pr_title = os.environ.get('INPUT_PR_TITLE')
    
    if not pr_number or not pr_title:
        print("Missing PR information")
        sys.exit(1)
        
    draft = get_draft_release()
    if draft and draft['body']:
        content = draft['body'].strip()
    else:
        print("No draft release content")
        content = ""
    
    # Don't add our own entry - let release-drafter handle it
    print(f"::set-output name=content::{content}")

def handle_prepare_release():
    """Handle prepare-release mode."""
    try:
        # Still process PR merge if info is provided
        pr_number = os.environ.get('INPUT_PR_NUMBER')
        pr_title = os.environ.get('INPUT_PR_TITLE')
        if pr_number and pr_title:
            handle_pr_merge()
        
        # Get full draft content
        draft = get_draft_release()
        if not draft:
            print("No draft release found")
            sys.exit(1)
        
        content = draft['body'].strip()
        if not content:
            print("Warning: Draft release is empty")
            content = ""  # Don't exit, just use empty content
        
        # No need to extract entries - pass full content
        print(f"::set-output name=content::{content}")
        
    except Exception as e:
        print(f"Error in prepare_release mode: {e}")
        sys.exit(1)

def main():
    """Main function."""
    setup_git()
    
    mode = os.environ.get('INPUT_MODE')
    if not mode:
        print("INPUT_MODE environment variable not set")
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
