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

def validate_inputs():
    """Validate required inputs."""
    mode = os.environ.get('INPUT_MODE')
    if not mode:
        print("Error: mode input not set")
        sys.exit(1)
    if mode not in ['pr-merge', 'prepare-release']:
        print(f"Error: invalid mode: {mode}")
        sys.exit(1)
        
    token = os.environ.get('INPUT_GITHUB_TOKEN')
    if not token:
        print("Error: github-token input not set")
        sys.exit(1)
        
    if mode == 'pr-merge':
        pr_number = os.environ.get('INPUT_PR_NUMBER')
        pr_title = os.environ.get('INPUT_PR_TITLE')
        if not pr_number or not pr_title:
            print("Error: PR number and title required for pr-merge mode")
            sys.exit(1)
    elif mode == 'prepare-release':
        version = os.environ.get('INPUT_VERSION')
        if not version:
            print("Error: version required for prepare-release mode")
            sys.exit(1)

def get_draft_release():
    """Get current draft release content."""
    token = os.environ.get('INPUT_GITHUB_TOKEN')
    try:
        repository = os.environ.get('GITHUB_REPOSITORY')
        if not repository:
            print("Error: GITHUB_REPOSITORY not set")
            sys.exit(1)

        cmd = [
            'curl', '-s',
            '-H', f'Authorization: token {token}',
            '-H', 'Accept: application/vnd.github+json',
            f'https://api.github.com/repos/{repository}/releases'
        ]
        
        result = subprocess.check_output(cmd, text=True)
        releases = json.loads(result)
        draft = next((r for r in releases if r.get('draft', False)), None)
        
        if draft:
            content = draft.get('body', '').strip()
            lines = content.split('\n')
            content_lines = []
            for line in lines:
                if not line.startswith('## Draft Release'):
                    if line.strip():
                        content_lines.append(line)
            
            content = '\n'.join(content_lines).strip()
            return {'id': draft['id'], 'body': content}
            
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching draft release: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing API response: {e}")
        sys.exit(1)

def create_draft_release():
    """Create new draft release."""
    token = os.environ.get('INPUT_GITHUB_TOKEN')
    try:
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
        return get_draft_release()
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating draft release: {e}")
        sys.exit(1)

def manage_release(content=None):
    """Handle release management based on mode."""
    mode = os.environ.get('INPUT_MODE')
    draft = get_draft_release()
    
    if not draft:
        draft = create_draft_release()
        
    if not draft:
        print("Failed to create/get draft release")
        sys.exit(1)
    
    if mode == 'pr-merge':
        pr_number = os.environ.get('INPUT_PR_NUMBER')
        pr_title = os.environ.get('INPUT_PR_TITLE')
        content = f"- PR #{pr_number}: {pr_title}\n" + draft['body']
    elif mode == 'prepare-release':
        version = os.environ.get('INPUT_VERSION')
        content = draft['body']  # Use existing content for release
        
    try:
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
        
        # Set output for GitHub Actions
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"content={content}\n")
        
    except subprocess.CalledProcessError as e:
        print(f"Error updating draft release: {e}")
        sys.exit(1)

def main():
    """Main function."""
    setup_git()
    validate_inputs()
    manage_release()

if __name__ == "__main__":
    main()