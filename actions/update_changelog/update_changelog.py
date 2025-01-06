#!/usr/bin/env python3

import os
import sys
import re
from datetime import datetime

def update_changelog(content, mode, version):
    """Update CHANGELOG.md with new content."""
    if not content:
        print("No content to update")
        return

    try:
        today = datetime.now().strftime("%m/%d/%Y")
        
        with open('CHANGELOG.md', 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        found_section = False
        skip_old = False
        
        # Process lines
        for line in lines:
            # Keep header content
            if not found_section and not line.startswith('## '):
                new_lines.append(line)
                continue
                
            # If we hit a versioned section before finding unreleased,
            # insert unreleased section here
            if not found_section and line.startswith('## **['):
                if mode == 'unreleased':
                    new_lines.append(f'## **{today} - {version} Unreleased**\n')
                    new_lines.append(content + '\n\n')  # Add extra newline before versioned
                found_section = True
                new_lines.append(line)
                continue
                
            # Handle existing unreleased section
            if re.search(r'## \*\*.*[Uu]nreleased\*\*', line):
                found_section = True
                if mode == 'unreleased':
                    new_lines.append(f'## **{today} - {version} Unreleased**\n')
                else:  # release mode
                    new_lines.append(f'## **[({today}) - {version}](https://github.com/{os.environ["GITHUB_REPOSITORY"]}/releases/tag/{version})**\n')
                new_lines.append(content + '\n\n')  # Add extra newline
                skip_old = True
                continue
            
            # Skip old content until next section
            if skip_old:
                if line.startswith('## '):
                    skip_old = False
                    new_lines.append(line)  # Don't add extra newline, already added
                else:
                    continue
                    
            # Add other content
            if not skip_old:
                new_lines.append(line)
        
        # If we haven't found a place for the section yet, add it after headers
        if not found_section:
            if new_lines and new_lines[-1] != '\n':
                new_lines.append('\n')
            if mode == 'unreleased':
                new_lines.append(f'## **{today} - {version} Unreleased**\n')
                new_lines.append(content + '\n')
            else:  # release mode
                new_lines.append(f'## **[({today}) - {version}](https://github.com/{os.environ["GITHUB_REPOSITORY"]}/releases/tag/{version})**\n')
                new_lines.append(content + '\n')
        
        # Write updated changelog
        with open('CHANGELOG.md', 'w') as f:
            f.writelines(new_lines)
            
    except Exception as e:
        print(f"Error updating changelog: {e}")
        sys.exit(1)

def main():
    """Main function."""
    content = os.environ.get('CONTENT')
    mode = os.environ.get('MODE')
    version = os.environ.get('VERSION')
    
    if not all([content, mode, version]):
        print("Missing required environment variables")
        sys.exit(1)
        
    if mode not in ['unreleased', 'release']:
        print(f"Invalid mode: {mode}")
        sys.exit(1)
        
    update_changelog(content, mode, version)

if __name__ == "__main__":
    main()