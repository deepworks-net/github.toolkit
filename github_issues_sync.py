#!/usr/bin/env python3
"""
GitHub Issues Sync Tool
Syncs GitHub issues, labels, and metadata for project management integration.
"""

import os
import json
import sys
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

class GitHubIssuesSync:
    def __init__(self, repo: str, token: Optional[str] = None):
        """Initialize GitHub Issues sync."""
        self.repo = repo
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.api_base = "https://api.github.com"
        
    def _make_api_request(self, endpoint: str, method: str = "GET") -> Dict:
        """Make authenticated GitHub API request."""
        headers = [
            "-H", "Accept: application/vnd.github+json",
            "-H", "User-Agent: github-toolkit-sync/1.0"
        ]
        
        if self.token:
            headers.extend(["-H", f"Authorization: token {self.token}"])
            
        cmd = ["curl", "-s", "-X", method] + headers + [f"{self.api_base}{endpoint}"]
        
        try:
            result = subprocess.check_output(cmd, text=True)
            return json.loads(result)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"API request failed: {e}")
            return {}
    
    def get_issues(self, state: str = "all", labels: str = "", per_page: int = 100) -> List[Dict]:
        """Get issues from GitHub repository."""
        endpoint = f"/repos/{self.repo}/issues"
        params = f"?state={state}&per_page={per_page}"
        if labels:
            params += f"&labels={labels}"
            
        data = self._make_api_request(endpoint + params)
        
        # Filter out pull requests (GitHub API returns PRs as issues)
        if isinstance(data, list):
            return [item for item in data if 'pull_request' not in item]
        return []
    
    def get_labels(self) -> List[Dict]:
        """Get repository labels."""
        endpoint = f"/repos/{self.repo}/labels"
        data = self._make_api_request(endpoint)
        return data if isinstance(data, list) else []
    
    def sync_issues_to_local(self, output_file: str = "issues_sync.json"):
        """Sync GitHub issues to local file."""
        print(f"Syncing issues from {self.repo}...")
        
        # Get issues and labels
        issues = self.get_issues()
        labels = self.get_labels()
        
        sync_data = {
            "repo": self.repo,
            "sync_time": datetime.now().isoformat(),
            "total_issues": len(issues),
            "labels": labels,
            "issues": issues
        }
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(sync_data, f, indent=2)
            
        print(f"Synced {len(issues)} issues and {len(labels)} labels to {output_file}")
        return sync_data
    
    def display_summary(self, issues: List[Dict]):
        """Display a summary of issues."""
        if not issues:
            print("No issues found.")
            return
            
        print("\n=== GITHUB ISSUES SUMMARY ===")
        print(f"Repository: {self.repo}")
        print(f"Total Issues: {len(issues)}")
        
        # Count by state
        state_counts = {}
        for issue in issues:
            state = issue.get('state', 'unknown')
            state_counts[state] = state_counts.get(state, 0) + 1
            
        print("\nBy State:")
        for state, count in state_counts.items():
            print(f"  {state.capitalize()}: {count}")
        
        # Show recent issues
        print(f"\n=== RECENT ISSUES ===")
        for issue in issues[:5]:
            number = issue.get('number', 'N/A')
            title = issue.get('title', 'No title')
            state = issue.get('state', 'unknown')
            labels = [l['name'] for l in issue.get('labels', [])]
            labels_str = f" [{', '.join(labels)}]" if labels else ""
            
            print(f"#{number}: {title} ({state}){labels_str}")
            
def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 github_issues_sync.py <repo> [token]")
        print("Example: python3 github_issues_sync.py deepworks-net/github.toolkit")
        sys.exit(1)
        
    repo = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else None
    
    sync = GitHubIssuesSync(repo, token)
    
    # Test API access
    print("Testing GitHub API access...")
    issues = sync.get_issues()
    
    if not issues:
        print("No issues found or API access failed.")
        print("Make sure:")
        print("1. Repository exists and is accessible")
        print("2. Token has 'issues' permission (if private repo)")
        sys.exit(1)
    
    # Display summary
    sync.display_summary(issues)
    
    # Sync to local file
    sync_data = sync.sync_issues_to_local()
    
    print(f"\n✅ GitHub issues sync completed successfully!")
    print(f"Data saved to: issues_sync.json")

if __name__ == "__main__":
    main()