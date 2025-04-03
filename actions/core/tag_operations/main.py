#!/usr/bin/env python3

import os
import sys
import subprocess
import re
from typing import Optional, List, Dict, Union, Tuple, Pattern

class GitTagOperations:
    """Handles atomic Git tag operations."""
    
    def __init__(self):
        self._configure_git()
    
    def _configure_git(self) -> None:
        """Configure git for safe directory operations."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git: {e}")
            sys.exit(1)
    
    def create_tag(self, tag_name: str, message: Optional[str] = None, 
                   ref: Optional[str] = None, force: bool = False) -> bool:
        """
        Create a new git tag.
        
        Args:
            tag_name: The name of the tag to create
            message: Optional message for annotated tag
            ref: Optional reference (commit SHA, branch, etc.) to tag
            force: Whether to force create the tag (replace if exists)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._validate_tag_name(tag_name):
            print(f"Invalid tag name: {tag_name}")
            return False
            
        try:
            cmd = ['git', 'tag']
            
            if force:
                cmd.append('-f')
                
            if message:
                cmd.extend(['-a', tag_name, '-m', message])
            else:
                cmd.append(tag_name)
                
            if ref:
                cmd.append(ref)
                
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating tag {tag_name}: {e}")
            return False
    
    def delete_tag(self, tag_name: str, remote: bool = False) -> bool:
        """
        Delete a git tag locally and optionally from remote.
        
        Args:
            tag_name: The name of the tag to delete
            remote: Whether to also delete from remote
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._validate_tag_name(tag_name):
            print(f"Invalid tag name: {tag_name}")
            return False
            
        try:
            # Delete local tag
            subprocess.check_call(['git', 'tag', '-d', tag_name])
            
            # Delete remote tag if requested
            if remote:
                subprocess.check_call(['git', 'push', 'origin', f':refs/tags/{tag_name}'])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error deleting tag {tag_name}: {e}")
            return False
    
    def push_tag(self, tag_name: str, force: bool = False) -> bool:
        """
        Push a specific tag to remote.
        
        Args:
            tag_name: The name of the tag to push
            force: Whether to force push
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._validate_tag_name(tag_name):
            print(f"Invalid tag name: {tag_name}")
            return False
            
        try:
            cmd = ['git', 'push', 'origin']
            
            if force:
                cmd.append('--force')
                
            cmd.append(f'refs/tags/{tag_name}')
            
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pushing tag {tag_name}: {e}")
            return False
    
    def list_tags(self, pattern: Optional[str] = None, sort: str = 'alphabetic') -> List[str]:
        """
        List all tags, optionally filtered by pattern.
        
        Args:
            pattern: Optional pattern to filter tags
            sort: Sort method ('alphabetic', 'version', 'date')
            
        Returns:
            list: List of tag names
        """
        try:
            cmd = ['git', 'tag']
            
            if pattern:
                cmd.extend(['-l', pattern])
                
            if sort == 'date':
                # Use a different approach to get tags sorted by date
                cmd = ['git', 'for-each-ref', '--sort=-creatordate', '--format=%(refname:short)', 'refs/tags/']
                if pattern:
                    # Apply pattern filtering through grep since for-each-ref doesn't support -l
                    cmd = ['git', 'for-each-ref', '--sort=-creatordate', '--format=%(refname:short)', 'refs/tags/']
                    output = subprocess.check_output(cmd, text=True)
                    # Filter tags manually
                    tags = [tag for tag in output.strip().split('\n') if tag]
                    pattern_regex = self._pattern_to_regex(pattern)
                    return [tag for tag in tags if pattern_regex.match(tag)]
            
            output = subprocess.check_output(cmd, text=True)
            tags = [tag for tag in output.strip().split('\n') if tag]
            
            # Sort tags by semantic versioning if requested
            if sort == 'version' and tags:
                return self._sort_tags_by_version(tags)
                
            return tags
        except subprocess.CalledProcessError as e:
            print(f"Error listing tags: {e}")
            return []
    
    def check_tag_exists(self, tag_name: str) -> bool:
        """
        Check if a tag exists.
        
        Args:
            tag_name: The tag name to check
            
        Returns:
            bool: True if tag exists, False otherwise
        """
        try:
            output = subprocess.check_output(['git', 'tag', '-l', tag_name], text=True).strip()
            return output == tag_name
        except subprocess.CalledProcessError:
            return False
    
    def get_tag_message(self, tag_name: str) -> str:
        """
        Get the message associated with a tag.
        
        Args:
            tag_name: The tag name
            
        Returns:
            str: The tag message or empty string if not found or not annotated
        """
        try:
            return subprocess.check_output(['git', 'tag', '-n', tag_name], text=True).strip()
        except subprocess.CalledProcessError:
            return ""
    
    def _validate_tag_name(self, tag_name: str) -> bool:
        """
        Validate a tag name according to git's rules.
        
        Args:
            tag_name: The tag name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Git tag cannot contain spaces, control chars, or these: ~^:?*[]\
        invalid_chars = r'[\s~^:?*[\]\\]'
        if re.search(invalid_chars, tag_name):
            return False
            
        # Tag cannot start with a dash
        if tag_name.startswith('-'):
            return False
            
        # Tag cannot be empty
        if not tag_name:
            return False
            
        # Cannot contain double dots ".."
        if '..' in tag_name:
            return False
            
        return True
    
    def _pattern_to_regex(self, pattern: str) -> Pattern:
        """
        Convert a git-style pattern to regex.
        
        Args:
            pattern: Git-style pattern (with * and ? wildcards)
            
        Returns:
            Pattern: Compiled regex pattern
        """
        # Escape special regex chars except * and ?
        regex = re.escape(pattern)
        # Convert git wildcards to regex wildcards
        regex = regex.replace('\\*', '.*').replace('\\?', '.')
        # Ensure it matches the whole string
        regex = f'^{regex}$'
        return re.compile(regex)
    
    def _sort_tags_by_version(self, tags: List[str]) -> List[str]:
        """
        Sort tags by semantic versioning.
        
        Args:
            tags: List of tag names
            
        Returns:
            list: Sorted list of tag names
        """
        def extract_version(tag):
            # Extract version components
            # Remove 'v' prefix if present
            if tag.startswith('v'):
                tag = tag[1:]
                
            try:
                # Split by dots and convert to integers where possible
                parts = []
                for part in tag.split('.'):
                    try:
                        parts.append(int(part))
                    except ValueError:
                        parts.append(part)
                return parts
            except:
                # If we can't parse as version, return original for lexicographic sort
                return [tag]
        
        # Sort tags by their version components
        return sorted(tags, key=extract_version, reverse=True)


def main():
    """Main entry point for the action."""
    tag_ops = GitTagOperations()
    
    # Get inputs
    action = os.environ.get('INPUT_ACTION')
    tag_name = os.environ.get('INPUT_TAG_NAME')
    message = os.environ.get('INPUT_MESSAGE')
    ref = os.environ.get('INPUT_REF')
    pattern = os.environ.get('INPUT_PATTERN')
    remote = os.environ.get('INPUT_REMOTE', 'false').lower() == 'true'
    force = os.environ.get('INPUT_FORCE', 'false').lower() == 'true'
    sort = os.environ.get('INPUT_SORT', 'alphabetic')
    
    result = False
    output = None
    tag_exists = False
    tag_message = ""
    
    # Validate inputs
    if action in ['create', 'delete', 'push'] and not tag_name:
        print(f"Error: tag_name is required for {action} action")
        sys.exit(1)
    
    # Execute requested operation
    if action == 'create':
        if tag_ops.check_tag_exists(tag_name):
            tag_exists = True
            if not force:
                print(f"Tag {tag_name} already exists. Use force=true to overwrite.")
                result = False
            else:
                result = tag_ops.create_tag(tag_name, message, ref, force)
        else:
            result = tag_ops.create_tag(tag_name, message, ref, force)
            
        if result and remote:
            result = tag_ops.push_tag(tag_name, force)
    
    elif action == 'delete':
        if not tag_ops.check_tag_exists(tag_name) and not remote:
            print(f"Tag {tag_name} doesn't exist locally.")
            result = True  # Consider it success if tag doesn't exist
        else:
            result = tag_ops.delete_tag(tag_name, remote)
    
    elif action == 'push':
        result = tag_ops.push_tag(tag_name, force)
    
    elif action == 'list':
        tags = tag_ops.list_tags(pattern, sort)
        output = tags
        result = True
    
    elif action == 'check':
        if not tag_name:
            print("Error: tag_name is required for check action")
            sys.exit(1)
        
        tag_exists = tag_ops.check_tag_exists(tag_name)
        tag_message = tag_ops.get_tag_message(tag_name)
        result = True
    
    else:
        print(f"Invalid action: {action}")
        sys.exit(1)
    
    # Set outputs
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        if output is not None and isinstance(output, list):
            f.write(f"tags={','.join(output)}\n")
        
        f.write(f"result={'success' if result else 'failure'}\n")
        f.write(f"tag_exists={'true' if tag_exists else 'false'}\n")
        
        if tag_message:
            # Escape newlines for GitHub Actions output
            tag_message = tag_message.replace('\n', '%0A')
            f.write(f"tag_message={tag_message}\n")
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()