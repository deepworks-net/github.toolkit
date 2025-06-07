# Phase 2 Migration Plan - Action Analysis

## Summary

Based on analysis of the repository structure, the following actions need transformation:

### Core Actions (7)
1. **branch_operations** - Git domain
2. **commit_operations** - Git domain  
3. **tag_operations** - Git domain
4. **version_calculator** - Version domain
5. **version_updater** - Version domain
6. **manage_release** - Release domain

### Composite Actions (4)
1. **git_ops** - Git domain (orchestrates branch/tag/commit)
2. **release_notes** - Release domain
3. **release_operations** - Release domain
4. **update_changelog** - Release domain

## Migration Tasks

### 1. Branch Operations
**Current Location**: `actions/core/branch_operations/`
**Target FCM**: `axioms/git/branch.fcm`

**Steps**:
- Extract action.yml inputs/outputs to FCM
- Parameter: operation type (create, delete, checkout, list, merge)
- Template: Docker operations
- External: main.py → github.com/deepworks-net/branch-operations-action

### 2. Tag Operations
**Current Location**: `actions/core/tag_operations/`
**Target FCM**: `axioms/git/tag.fcm`

**Steps**:
- Extract action.yml structure to FCM
- Parameter: operation type (create, delete, push, list)
- Template: Docker operations
- External: main.py → github.com/deepworks-net/tag-operations-action

### 3. Commit Operations
**Current Location**: `actions/core/commit_operations/`
**Target FCM**: `axioms/git/commit.fcm`

**Steps**:
- Extract action.yml structure to FCM
- Parameter: operation type (create, amend, list, cherry-pick, revert)
- Template: Docker operations
- External: main.py + git_utils.py → github.com/deepworks-net/commit-operations-action

### 4. Version Calculator
**Current Location**: `actions/core/version_calculator/`
**Target FCM**: `axioms/version/calculate.fcm`

**Steps**:
- Extract version calculation logic to FCM
- Parameter: bump type (major, minor, patch)
- Template: Version patterns
- External: main.py → github.com/deepworks-net/version-calculator-action

### 5. Version Updater
**Current Location**: `actions/core/version_updater/`
**Target FCM**: `axioms/version/update.fcm`

**Steps**:
- Extract file update patterns to FCM
- Parameter: version placeholder patterns
- Template: File update operations
- External: main.py → github.com/deepworks-net/version-updater-action

### 6. Manage Release
**Current Location**: `actions/core/manage_release/`
**Target FCM**: `axioms/release/manage.fcm`

**Steps**:
- Extract release workflow to FCM
- Parameter: release type, version
- Template: Release orchestration
- External: main.py → github.com/deepworks-net/manage-release-action

### 7. Git Operations (Composite)
**Current Location**: `actions/composite/git_ops/`
**Target Pattern**: `patterns/git-operations.fcm`

**Steps**:
- Define composition of branch + tag + commit axioms
- Create logic/compositions.fcm entry
- Map dependencies in logic/dependencies.fcm

### 8. Release Notes
**Current Location**: `actions/composite/release_notes/`
**Target FCM**: `axioms/release/notes.fcm`

**Steps**:
- Extract PR/commit parsing logic
- Parameter: note format template
- External: release_notes.py → github.com/deepworks-net/release-notes-action

### 9. Update Changelog
**Current Location**: `actions/composite/update_changelog/`
**Target FCM**: `axioms/release/changelog.fcm`

**Steps**:
- Extract changelog format patterns
- Parameter: changelog template
- External: update_changelog.py → github.com/deepworks-net/update-changelog-action

## Identified Patterns

### Common Hardcoded Values to Extract:
- Python versions in Dockerfiles (3.9, 3.10, etc.)
- File paths (/github/workspace, etc.)
- Default branch names (main, develop)
- Version number formats

### Reusable Templates:
- Docker base images for Python actions
- Git configuration setup
- GitHub token handling
- Error handling patterns

## Next Steps

1. Create first axiom FCM as example (suggest starting with tag_operations)
2. Establish external package structure
3. Create mechanics templates
4. Test transformation with one complete action
5. Automate remaining transformations