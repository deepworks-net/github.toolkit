#!/usr/bin/env python3

import os
import sys
import subprocess
import json

def get_draft_release():
    """Get current draft release content."""
    try:
        cmd = [
            'gh', 'api',
            '-H', 'Accept: application/vnd.github+json',
            f'repos/{os.environ["GITHUB_REPOSITORY"]}/releases',
            '--jq', '.[] | select(.draft == true)'
        ]
        
        result = subprocess.check_output(cmd, text=True)
        return json.loads(result) if result else None
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching draft release: {e}")
        sys.exit(1)

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
    content = draft['body'] if draft else ''
    
    # Add new PR entry
    new_entry = f"- PR #{pr_number}: {pr_title}\n"
    if content:
        content = new_entry + content
    else:
        content = new_entry
        
    update_draft_release(content)
    print(f"::set-output name=content::{content}")

def handle_prepare_release():
    """Handle prepare-release mode."""
    draft = get_draft_release()
    if not draft:
        print("No draft release found")
        sys.exit(1)
        
    content = draft['body']
    print(f"::set-output name=content::{content}")

def main():
    """Main function."""
    mode = os.environ.get('MODE')
    
    if mode == 'pr-merge':
        handle_pr_merge()
    elif mode == 'prepare-release':
        handle_prepare_release()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()