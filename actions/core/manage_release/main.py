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
    token = os.environ.get('INPUT_GITHUB_TOKEN')
    if not token:
        print("Error: github_token input not set")
        sys.exit(1)
        
    operation = os.environ.get('INPUT_OPERATION', 'get')
    if operation not in ['draft', 'get', 'update']:
        print(f"Error: invalid operation: {operation}")
        sys.exit(1)
        
    if operation == 'update':
        content = os.environ.get('INPUT_CONTENT')
        if not content:
            print("Error: content required for update operation")
            sys.exit(1)
            
        mode = os.environ.get('INPUT_UPDATE_MODE', 'replace')
        if mode not in ['replace', 'append', 'prepend']:
            print(f"Error: invalid update mode: {mode}")
            sys.exit(1)

def get_draft_release():
    """Get current draft release."""
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
            return {
                'id': draft['id'],
                'body': draft.get('body', '').strip(),
                'tag_name': draft.get('tag_name', ''),
                'name': draft.get('name', '')
            }
            
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
    name = os.environ.get('INPUT_NAME', 'Draft Release')
    body = os.environ.get('INPUT_BODY', '')
    
    try:
        cmd = [
            'curl', '-s',
            '-X', 'POST',
            '-H', f'Authorization: token {token}',
            '-H', 'Accept: application/vnd.github+json',
            f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/releases',
            '-d', json.dumps({
                'tag_name': 'DRAFT',
                'name': name,
                'draft': True,
                'body': body
            })
        ]
        
        subprocess.check_call(cmd)
        return get_draft_release()
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating draft release: {e}")
        sys.exit(1)

def update_draft_release(draft_id, content, mode='replace'):
    """Update draft release content."""
    token = os.environ.get('INPUT_GITHUB_TOKEN')
    
    try:
        draft = get_draft_release()
        if not draft:
            print("Error: No draft release found to update")
            sys.exit(1)
            
        # Prepare new content based on mode
        if mode == 'append':
            new_content = f"{draft['body']}\n{content}"
        elif mode == 'prepend':
            new_content = f"{content}\n{draft['body']}"
        else:  # replace
            new_content = content
        
        cmd = [
            'curl', '-s',
            '-X', 'PATCH',
            '-H', f'Authorization: token {token}',
            '-H', 'Accept: application/vnd.github+json',
            f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/releases/{draft_id}',
            '-d', json.dumps({'body': new_content.strip()})
        ]
        
        subprocess.check_call(cmd)
        return get_draft_release()
        
    except subprocess.CalledProcessError as e:
        print(f"Error updating draft release: {e}")
        sys.exit(1)

def main():
    """Main function."""
    setup_git()
    validate_inputs()
    
    operation = os.environ.get('INPUT_OPERATION', 'get')
    
    # Handle operations
    if operation == 'draft':
        draft = get_draft_release() or create_draft_release()
    elif operation == 'get':
        draft = get_draft_release()
    else:  # update
        content = os.environ.get('INPUT_CONTENT')
        mode = os.environ.get('INPUT_UPDATE_MODE', 'replace')
        draft = get_draft_release()
        if draft:
            draft = update_draft_release(draft['id'], content, mode)
        else:
            print("Error: No draft release found to update")
            sys.exit(1)
    
    # Set outputs
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        if draft:
            f.write(f"id={draft['id']}\n")
            f.write(f"body={draft['body']}\n")
            f.write(f"tag_name={draft['tag_name']}\n")
            f.write(f"name={draft['name']}\n")
            f.write(f"exists=true\n")
        else:
            f.write("exists=false\n")

if __name__ == "__main__":
    main()