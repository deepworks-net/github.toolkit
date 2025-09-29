#!/usr/bin/env python3
"""
Central Project Data Sync
Aggregates and tracks data from multiple sources (GitHub, GitLab, emails, etc.)
Designed for prototyping before SQL database implementation.
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class ProjectDataSync:
    def __init__(self, data_dir: str = "project_data"):
        """Initialize central project data sync."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Source-specific subdirectories
        self.sources = {
            'github': self.data_dir / 'github',
            'gitlab': self.data_dir / 'gitlab', 
            'email': self.data_dir / 'email',
            'timeline': self.data_dir / 'timeline',
            'metadata': self.data_dir / 'metadata'
        }
        
        for source_dir in self.sources.values():
            source_dir.mkdir(exist_ok=True)
    
    def sync_github_repo(self, repo: str, token: Optional[str] = None):
        """Sync GitHub repository data."""
        try:
            # Import the GitHub sync tool we created
            from github_issues_sync import GitHubIssuesSync
            
            sync = GitHubIssuesSync(repo, token)
            issues = sync.get_issues()
            labels = sync.get_labels()
            
            data = {
                'type': 'github_repo',
                'repo': repo,
                'sync_time': datetime.now().isoformat(),
                'total_items': len(issues),
                'issues': issues,
                'labels': labels,
                'last_updated': max([issue.get('updated_at', '') for issue in issues]) if issues else None
            }
            
            # Save data to structured location
            safe_repo = repo.replace('/', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{safe_repo}_{timestamp}.json"
            filepath = self.sources['github'] / filename
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Synced GitHub {repo}: {len(issues)} issues, {len(labels)} labels")
            print(f"📁 Saved to: {filepath}")
            return data
            
        except Exception as e:
            print(f"❌ GitHub sync failed for {repo}: {e}")
            return None

def main():
    """Test the sync system."""
    sync = ProjectDataSync()
    
    if len(sys.argv) >= 3 and sys.argv[1] == "github":
        repo = sys.argv[2]
        token = sys.argv[3] if len(sys.argv) > 3 else None
        sync.sync_github_repo(repo, token)
    else:
        print("Usage: python3 project_data_sync.py github <repo> [token]")

if __name__ == "__main__":
    main()