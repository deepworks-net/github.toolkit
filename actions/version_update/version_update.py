#!/usr/bin/env python3

import os
import sys
import yaml
import re

def update_mkdocs_version(filename, version):
    """Update version in mkdocs.yml."""
    try:
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'extra' not in config:
            config['extra'] = {}
        
        # Remove 'v' prefix if present for consistency
        version_num = version.lstrip('v')
        config['extra']['version'] = version_num
        
        # Preserve formatting with dump
        with open(filename, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
            
        print(f"Updated version in {filename} to {version_num}")
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