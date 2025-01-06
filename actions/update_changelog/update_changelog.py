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
        
        # Clean up the content - remove the "Draft Release" header if present
        content_lines = content.split('\n')
            
        if content_lines and content_lines[0].startswith('## Draft Release'):
            content_lines = content_lines[1:]
        content = '\n'.join(line for line in content_lines if line.strip())

        # Process lines
        for i, line in enumerate(lines):
            # Keep header content (first two lines)
            if i < 2:
                new_lines.append(line)
                continue
                
            # If we hit a versioned section and haven't added unreleased,
            # add it here
            if not found_section and line.startswith('## **['):
                if mode == 'unreleased':
                    new_lines.append(f'\n## **{today} - {version} Unreleased**\n')
                    if content:
                        new_lines.append(content + '\n\n')
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
                if content:
                    new_lines.append(content + '\n\n')
                skip_old = True
                continue
            
            # Skip old content until next section
            if skip_old:
                if line.startswith('## '):
                    skip_old = False
                    new_lines.append(line)
                continue
                    
            # Add other content
            if not skip_old:
                new_lines.append(line)
        
        # If we haven't added the section yet, add it after headers
        if not found_section:
            new_lines.append(f'\n## **{today} - {version} Unreleased**\n')
            if content:
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