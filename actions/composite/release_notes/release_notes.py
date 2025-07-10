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
    token = os.environ.get('INPUT_GITHUB_TOKEN')
    if not token:
        print("Error: github-token input not set")
        sys.exit(1)

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
        
        # Find draft release and process content
        draft = next((r for r in releases if r.get('draft', False)), None)
        
        if draft:
            
            # Get the full content
            content = draft.get('body', '').strip()
            lines = content.split('\n')
            
            # Keep everything except the header
            content_lines = []
            for line in lines:
                if not line.startswith('## Draft Release'):
                    if line.strip():  # Keep non-empty lines
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

def extract_pr_entries(content):
    """Extract PR entries from content."""
    entries = []
    for line in content.split('\n'):
        if line.strip().startswith('-'):
            entries.append(line.strip())
    return entries

def get_commits_since_last_release():
    """Get commits since the last release tag."""
    try:
        # Get the latest release tag
        latest_tag = subprocess.check_output([
            'git', 'tag', '-l', 'v*', '--sort=-v:refname'
        ], text=True).strip().split('\n')[0] if subprocess.check_output([
            'git', 'tag', '-l', 'v*', '--sort=-v:refname'
        ], text=True).strip() else None
        
        if latest_tag:
            # Get commits since the last tag
            commits = subprocess.check_output([
                'git', 'log', f'{latest_tag}..HEAD', '--pretty=format:- %s', '--no-merges'
            ], text=True).strip()
        else:
            # No previous tags, get last 10 commits
            commits = subprocess.check_output([
                'git', 'log', '--pretty=format:- %s', '--no-merges', '--max-count=10'
            ], text=True).strip()
        
        return commits, latest_tag
    except subprocess.CalledProcessError:
        return "- Updates and improvements", None

def create_meaningful_release_content(version=None):
    """Create meaningful release content based on actual changes."""
    commits, last_tag = get_commits_since_last_release()
    
    if not commits:
        commits = "- Updates and improvements"
    
    # Categorize commits
    features = []
    fixes = []
    improvements = []
    other = []
    
    for line in commits.split('\n'):
        if not line.strip():
            continue
        lower_line = line.lower()
        if any(word in lower_line for word in ['add', 'new', 'implement', 'create']):
            features.append(line)
        elif any(word in lower_line for word in ['fix', 'bug', 'error', 'issue']):
            fixes.append(line)
        elif any(word in lower_line for word in ['improve', 'enhance', 'update', 'optimize']):
            improvements.append(line)
        else:
            other.append(line)
    
    # Build categorized content
    content_parts = []
    
    if features:
        content_parts.append("### ✨ New Features\n" + '\n'.join(features))
    
    if fixes:
        content_parts.append("### 🐛 Bug Fixes\n" + '\n'.join(fixes))
    
    if improvements:
        content_parts.append("### 🔧 Improvements\n" + '\n'.join(improvements))
    
    if other:
        content_parts.append("### 📝 Other Changes\n" + '\n'.join(other))
    
    if not content_parts:
        content_parts.append("### 📝 Changes\n- Updates and improvements")
    
    content = '\n\n'.join(content_parts)
    
    # Add comparison link if we have a previous tag
    if last_tag and version:
        content += f"\n\n**Full Changelog**: https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'deepworks-net/github.toolkit')}/compare/{last_tag}...{version}"
    
    return content

def create_draft_release():
    """Create new draft release."""
    try:
        token = os.environ.get('INPUT_GITHUB_TOKEN')
        
        # Create meaningful content based on actual changes
        body = create_meaningful_release_content()
        
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
                'body': body
            })
        ]
        
        subprocess.check_call(cmd)
        print("Created new draft release with meaningful content")
        
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
        # Need to properly escape newlines for GitHub Actions set-output
        escaped_content = content.replace('\n', '%0A')
        print(f"::set-output name=content::{escaped_content}")
    else:
        print("No draft release content")

def handle_prepare_release():
    """
    Handle prepare-release mode.
    
    Intended flow:
    1. release-drafter.yml maintains draft release with PR content during development
    2. prep tag workflow reuses existing draft content for final release
    3. Only generates new content if draft is empty or contains placeholder text
    """
    try:
        # Still process PR merge if info is provided
        pr_number = os.environ.get('INPUT_PR_NUMBER')
        pr_title = os.environ.get('INPUT_PR_TITLE')
        if pr_number and pr_title:
            handle_pr_merge()
        
        # Get version for better content generation
        version = os.environ.get('INPUT_VERSION', 'v1.0.0')
        
        # Get existing draft content (release-drafter should have created this)
        draft = get_draft_release()
        if not draft:
            print("No draft release found - this should have been created by release-drafter workflow")
            print("Creating fallback draft release...")
            create_draft_release()
            draft = get_draft_release()
            
        if not draft:
            print("Failed to create/get draft release")
            sys.exit(1)
        
        # Use existing draft content if it exists and is meaningful
        placeholder_texts = ['Recent Changes', 'Updates and improvements', 'No changes', 'What\'s Changed', 'No Changes']
        is_placeholder = any(placeholder in draft['body'] for placeholder in placeholder_texts)
        
        if draft['body'] and draft['body'].strip() and not is_placeholder:
            print("Using existing draft release content...")
            content = draft['body'].strip()
        else:
            print("Draft release is empty or contains placeholder content, generating meaningful content...")
            content = create_meaningful_release_content(version)
        
        if content:
            escaped_content = content.replace('\n', '%0A')
            print(f"::set-output name=content::{escaped_content}")
        else:
            print("Warning: No content generated")
            # Return basic content instead of failing
            fallback_content = "### 📝 Changes\n- Updates and improvements"
            escaped_content = fallback_content.replace('\n', '%0A')
            print(f"::set-output name=content::{escaped_content}")
        
    except Exception as e:
        print(f"Error in prepare_release mode: {e}")
        sys.exit(1)

def handle_update_draft():
    """Handle update-draft mode - create or update draft release with provided content."""
    try:
        content = os.environ.get('INPUT_CONTENT', '')
        version = os.environ.get('INPUT_VERSION', 'v1.0.0')
        
        print(f"Received content for draft update: {content[:100]}...")  # Debug output
        
        if not content:
            print("No content provided for draft update, generating new content...")
            content = create_meaningful_release_content(version)
        
        # Decode the content if it was escaped from GitHub Actions
        content = content.replace('%0A', '\n')
        
        print(f"Final content to update: {content[:100]}...")  # Debug output
        
        # Update the draft release with the provided content
        update_draft_release(content)
        
    except Exception as e:
        print(f"Error in update-draft mode: {e}")
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
    elif mode == 'update-draft':
        handle_update_draft()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
