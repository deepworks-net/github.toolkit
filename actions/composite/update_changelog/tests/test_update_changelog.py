#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

# Add path to import update_changelog module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import update_changelog as uc

class FixedDateTime:
    """Helper datetime class returning a fixed date."""
    @classmethod
    def now(cls):
        return cls.fake_now

    @staticmethod
    def strftime(fmt):
        return FixedDateTime.fake_now.strftime(fmt)

FixedDateTime.fake_now = __import__('datetime').datetime(2025, 1, 1)

@pytest.mark.unit
@pytest.mark.changelog
def test_unreleased_mode(tmp_path, monkeypatch, mock_git_env):
    changelog = tmp_path / 'CHANGELOG.md'
    changelog.write_text("# Changelog\nNotes\n\n## **[(01/01/2024) - v0.1.0](https://example.com)**\n- old\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(uc, 'datetime', FixedDateTime)

    content = '### Added\n- New stuff'
    uc.update_changelog(content, 'unreleased', 'v0.2.0')

    text = changelog.read_text()
    assert f"## **{FixedDateTime.fake_now.strftime('%m/%d/%Y')} - v0.2.0 Unreleased**" in text
    assert '### Added' in text
    # New section should appear before previous release line
    assert text.index('Unreleased') < text.index('v0.1.0')

@pytest.mark.unit
@pytest.mark.changelog
def test_release_mode(tmp_path, monkeypatch, mock_git_env):
    date = FixedDateTime.fake_now.strftime('%m/%d/%Y')
    unreleased = f"## **{date} - v0.2.0 Unreleased**"
    changelog = tmp_path / 'CHANGELOG.md'
    changelog.write_text(f"# Changelog\nInfo\n\n{unreleased}\nChanges here\n\n## **[(01/01/2024) - v0.1.0](https://example.com)**\n- old\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(uc, 'datetime', FixedDateTime)

    uc.update_changelog('Changes here', 'release', 'v0.2.0')
    text = changelog.read_text()
    expected_link = f"## **[({date}) - v0.2.0](https://github.com/{mock_git_env['GITHUB_REPOSITORY']}/releases/tag/v0.2.0)**"
    assert unreleased not in text
    assert expected_link in text
    # Ensure previous release still present
    assert 'v0.1.0' in text
