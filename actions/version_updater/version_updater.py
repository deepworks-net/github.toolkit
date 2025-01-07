#!/usr/bin/env python3

import os
import sys
import json
import re

def update_yaml_file(filename, version, strip_v=True):
    """Update version in YAML files."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
        # First find the version line
        lines = content.split('\n')
        new_lines = []
        updated = False
        
        for line in lines:
            if 'version:' in line:
                indent = line[:line.index('version:')]
                ver = version.lstrip('v') if strip_v else version
                new_lines.append(f"{indent}version: {ver}")
                updated = True
            else:
                new_lines.append(line)
        
        if not updated:
            print(f"Warning: No version field found in {filename}")
            return True  # Not finding a version field isn't necessarily an error
        
        new_content = '\n'.join(new_lines)
        
        with open(filename, 'w') as f:
            f.write(new_content)
            
        print(f"Updated version in {filename} to {version}")
        return True
            
    except Exception as e:
        print(f"Error updating {filename}: {e}")
        return False

def update_json_file(filename, version, strip_v=True):
    """Update version in JSON files."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
        if 'version' in data:
            data['version'] = version.lstrip('v') if strip_v else version
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"Updated version in {filename} to {version}")
            return True
        else:
            print(f"Warning: No version field found in {filename}")
            return True  # Not finding a version field isn't necessarily an error
            
    except Exception as e:
        print(f"Error updating {filename}: {e}")
        return False

def update_generic_file(filename, version, strip_v=True):
    """Update version in any text file using regex."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Pattern matches common version formats
        pattern = r'(version\s*[=:]\s*["\']?)v?\d+\.\d+\.\d+(["\']?)'
        ver = version.lstrip('v') if strip_v else version
        replacement = r'\1' + ver + r'\2'
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
        
        if count == 0:
            print(f"Warning: No version field found in {filename}")
            return True
            
        with open(filename, 'w') as f:
            f.write(new_content)
            
        print(f"Updated {count} version occurrences in {filename} to {version}")
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
    
    # Handle GitHub Actions multiline string format
    files_input = os.environ.get('INPUT_FILES', '[]')
    try:
        # First try as JSON
        files = json.loads(files_input)
    except json.JSONDecodeError:
        # If that fails, try as multiline string
        files = [f.strip() for f in files_input.split('\n') if f.strip()]
    
    if not files:
        print("No files specified to update")
        sys.exit(0)

if __name__ == "__main__":
    main()