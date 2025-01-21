#!/usr/bin/env python3

import os
import sys
import json
import re

def validate_version_format(version):
    """Validate version string format."""
    if not version:
        print("Error: version input not set")
        sys.exit(1)
    
    pattern = r'^v?\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        print(f"Invalid version format: {version}, must match pattern: v1.2.3")
        sys.exit(1)

def validate_files_input(files):
    """Validate files input."""
    if not files:
        print("Error: no files specified to update")
        sys.exit(1)
    
    files_list = [
        f.strip().strip('"').strip("'")
        for f in files.splitlines()
        if f.strip()
    ]
    
    if not files_list:
        print("Error: no valid files provided")
        sys.exit(1)
        
    return files_list

def update_yaml_file(filename, version, strip_v=True):
    """Update version in YAML files."""
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}")
        return False
        
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
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
            return False
        
        with open(filename, 'w') as f:
            f.write('\n'.join(new_lines))
            
        print(f"Updated version in {filename} to {version}")
        return True
            
    except (IOError, OSError) as e:
        print(f"Error updating {filename}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error updating {filename}: {e}")
        return False

def update_json_file(filename, version, strip_v=True):
    """Update version in JSON files."""
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}")
        return False
        
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
        if 'version' not in data:
            print(f"Warning: No version field found in {filename}")
            return False
            
        data['version'] = version.lstrip('v') if strip_v else version
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Updated version in {filename} to {version}")
        return True
            
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filename}: {e}")
        return False
    except (IOError, OSError) as e:
        print(f"Error updating {filename}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error updating {filename}: {e}")
        return False

def update_generic_file(filename, version, strip_v=True):
    """Update version in any text file using regex."""
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}")
        return False
        
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        pattern = r'(version\s*[=:]\s*["\']?)v?\d+\.\d+\.\d+(["\']?)'
        ver = version.lstrip('v') if strip_v else version
        replacement = r'\1' + ver + r'\2'
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
        
        if count == 0:
            print(f"Warning: No version field found in {filename}")
            return False
            
        with open(filename, 'w') as f:
            f.write(new_content)
            
        print(f"Updated {count} version occurrences in {filename} to {version}")
        return True
        
    except (IOError, OSError) as e:
        print(f"Error updating {filename}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error updating {filename}: {e}")
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
    # Validate version input
    version = os.environ.get('INPUT_VERSION')
    validate_version_format(version)
    
    # Validate files input
    files_input = os.environ.get('INPUT_FILES', '')
    files = validate_files_input(files_input)
    
    # Get strip_v_prefix option
    strip_v = os.environ.get('INPUT_STRIP_V_PREFIX', 'true').lower() == 'true'
    
    # Process files
    updated_files = []
    for filename in files:
        if update_file(filename, version, strip_v):
            updated_files.append(filename)
    
    # Output results using new GitHub Actions format
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"files={json.dumps(updated_files)}\n")
    
    # Exit with error if any file failed
    if len(updated_files) != len(files):
        print(f"Error: Only updated {len(updated_files)} of {len(files)} files")
        sys.exit(1)

if __name__ == "__main__":
    main()