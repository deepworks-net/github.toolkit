#!/usr/bin/env python3

import os
import sys
import yaml
import re

def custom_yaml_constructor(loader, node):
    """Custom constructor for handling special YAML tags."""
    return loader.construct_scalar(node)

def update_mkdocs_version(filename, version):
    """Update version in mkdocs.yml."""
    try:
        # Read the file
        with open(filename, 'r') as f:
            content = f.read()
            
        print("DEBUG: Original content:", content)
        
        # First find the version line
        lines = content.split('\n')
        new_lines = []
        in_extra = False
        
        for line in lines:
            if line.strip().startswith('extra:'):
                in_extra = True
                new_lines.append(line)
            elif in_extra and line.strip().startswith('version:'):
                # Replace version while maintaining indentation
                indent = line[:line.index('version:')]
                new_lines.append(f"{indent}version: {version.lstrip('v')}")
            else:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        print("DEBUG: New content:", new_content)
        
        with open(filename, 'w') as f:
            f.write(new_content)
            
        print(f"Updated version in {filename} to {version.lstrip('v')}")
        return True
            
    except Exception as e:
        print(f"Error updating {filename}: {e}")
        return False

def main():
    """Main function."""
    version = os.environ.get('INPUT_VERSION')
    if not version:
        print("Error: version input not set")
        sys.exit(1)
    
    files = os.environ.get('INPUT_FILES', 'mkdocs.yml').split(',')
    success = True
    
    for file in files:
        file = file.strip()
        if file.endswith('mkdocs.yml'):
            if not update_mkdocs_version(file, version):
                success = False
        # Add more file types here as needed
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()