# version_calculation.py
# Reusable script for version calculation

import subprocess
import re
import sys

def get_latest_tag():
    """Retrieve the latest version tag."""
    try:
        output = subprocess.check_output(['git', 'tag', '-l', 'v*', '--sort=-v:refname'], text=True).strip()
        latest_tag = output.splitlines()[0] if output else None
        if not latest_tag:
            raise ValueError("No version tags found.")
        return latest_tag
    except subprocess.CalledProcessError as e:
        print(f"Error fetching tags: {e}")
        sys.exit(1)

def calculate_next_version(latest_tag):
    """Calculate the next version based on the latest tag."""
    match = re.match(r'v(\d+)\.(\d+)\.(\d+)', latest_tag)
    if not match:
        print(f"Invalid version format: {latest_tag}")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())
    commit_count = get_commit_count_since_tag(latest_tag)
    next_patch = patch + commit_count

    return f"v{major}.{minor}.{next_patch}"

def get_commit_count_since_tag(tag):
    """Count commits since the latest tag."""
    try:
        output = subprocess.check_output(['git', 'rev-list', f'{tag}..HEAD', '--count'], text=True).strip()
        return int(output)
    except subprocess.CalledProcessError as e:
        print(f"Error counting commits: {e}")
        sys.exit(1)

def main():
    latest_tag = get_latest_tag()
    print(f"Latest tag: {latest_tag}")

    next_version = calculate_next_version(latest_tag)
    print(f"Next version: {next_version}")

    # Output the next version for GitHub Actions
    print(f"::set-output name=next_version::{next_version}")

if __name__ == "__main__":
    main()