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

def update_file(filename, version, strip_v=True):
    """Update version in a file based on its type."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ['.yml', '.yaml']:
        return update_yaml_file(filename, version, strip_v)
    elif ext == '.json':
        return update_json_file(filename, version, strip_v)
    else:
        return update_generic_file(filename, version, strip_v)

def main():
    """Main function."""
    # Get required inputs
    version = os.environ.get('INPUT_VERSION')
    if not version:
        print("Error: version input not set")
        sys.exit(1)
    
    # Process files input
    files_input = os.environ.get('INPUT_FILES', '')
    
    # Split the multiline string into a list of files
    # Strip quotes and whitespace from each line
    files = [
        f.strip().strip('"').strip("'")
        for f in files_input.splitlines()
        if f.strip()
    ]
    
    if not files:
        print("No files specified to update")
        print("::set-output name=files::[]")
        sys.exit(0)
    
    # Get strip_v_prefix option
    strip_v = os.environ.get('INPUT_STRIP_V_PREFIX', 'true').lower() == 'true'
    
    # Keep track of successfully updated files
    updated_files = []
    
    # Process each file
    for filename in files:
        if update_file(filename, version, strip_v):
            updated_files.append(filename)
    
    # Output results for GitHub Actions
    print(f"::set-output name=files::{json.dumps(updated_files)}")
    
    # Exit with success only if all files were updated
    if len(updated_files) != len(files):
        print(f"Warning: Only updated {len(updated_files)} of {len(files)} files")
        sys.exit(1)

if __name__ == "__main__":
    main()