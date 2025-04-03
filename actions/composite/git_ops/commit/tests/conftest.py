import os
import pytest
import tempfile
import subprocess
from pathlib import Path

@pytest.fixture
def git_repo():
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to the temporary directory
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            # Initialize git repo
            subprocess.check_call(['git', 'init'])
            subprocess.check_call(['git', 'config', 'user.name', 'Test User'])
            subprocess.check_call(['git', 'config', 'user.email', 'test@example.com'])
            
            # Create and commit a file
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("Initial content")
            subprocess.check_call(['git', 'add', 'test.txt'])
            subprocess.check_call(['git', 'commit', '-m', 'Initial commit'])
            
            yield tmpdir
        finally:
            # Restore original directory
            os.chdir(original_dir)