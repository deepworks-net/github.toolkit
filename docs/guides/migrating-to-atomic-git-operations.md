# Migrating to Atomic Git Operations

This guide helps you transition from monolithic Git operation scripts to the new atomic, reusable actions following the core/composite pattern.

## Why Migrate?

The new core/composite pattern offers several advantages:

1. **Improved Maintainability**: Smaller, focused actions with single responsibilities
2. **Better Error Handling**: Standardized error handling across all Git operations
3. **Enhanced Testing**: Easier to test smaller, atomic components
4. **Flexible Composability**: Build custom workflows by combining atomic actions
5. **Simplified Workflows**: Use composite actions for common scenarios

## Migration Strategies

### Strategy 1: Direct Replacement

Replace individual Git commands with their equivalent atomic actions.

#### Before:

```yaml
- name: Create and push tag
  run: |
    git tag v1.0.0
    git push origin v1.0.0
```

#### After:

```yaml
- name: Create and push tag
  uses: ./actions/core/tag_operations
  with:
    action: create
    tag_name: v1.0.0
    remote: true
```

### Strategy 2: Replace Script Blocks

Replace multi-step script blocks with appropriate core or composite actions.

#### Before:

```yaml
- name: Prepare release
  run: |
    # Create release branch
    git checkout -b release/${{ inputs.version }}
    git push origin release/${{ inputs.version }}
    
    # Update changelog
    sed -i "s/## Unreleased/## ${{ inputs.version }} ($(date +'%Y-%m-%d'))/g" CHANGELOG.md
    git add CHANGELOG.md
    git commit -m "Update changelog for ${{ inputs.version }}"
    git push
    
    # Create tag
    git tag ${{ inputs.version }}
    git push origin ${{ inputs.version }}
```

#### After:

```yaml
- name: Prepare release
  uses: ./actions/composite/release_operations
  with:
    action: create
    version: ${{ inputs.version }}
    release_branch: release/${{ inputs.version }}
    update_changelog: true
    message: "Release ${{ inputs.version }}"
```

### Strategy 3: Gradual Migration

Migrate one operation at a time while keeping existing scripts for other operations.

```yaml
# Step 1: Migrate tag operations
- name: Create tag
  uses: ./actions/core/tag_operations
  with:
    action: create
    tag_name: v1.0.0

# Still using script for branch operations (to be migrated later)
- name: Create branch
  run: |
    git checkout -b feature/new-feature
    git push origin feature/new-feature
```

## Core Actions Reference

### Tag Operations

```yaml
- name: Create tag
  uses: ./actions/core/tag_operations
  with:
    action: create  # create, delete, push, list, check
    tag_name: v1.0.0
    message: "Release v1.0.0"  # Optional for annotated tags
    ref: main  # Optional reference
    remote: true  # Push to remote
    force: false  # Force operation
```

### Branch Operations

```yaml
- name: Create branch
  uses: ./actions/core/branch_operations
  with:
    action: create  # create, delete, checkout, merge, list
    branch_name: feature/new-feature
    base_branch: main
    remote: true
```

### Commit Operations

```yaml
- name: Create commit
  uses: ./actions/core/commit_operations
  with:
    action: create  # create, amend, list, get, cherry-pick, revert
    message: "Add new feature"
    files: "file1.txt, file2.js"  # Optional
```

## Composite Actions Reference

### Release Operations

```yaml
- name: Create release
  uses: ./actions/composite/release_operations
  with:
    action: create  # create, publish, update, delete
    version: v1.0.0
    message: "Release v1.0.0"
    release_branch: release/1.0  # Optional
    update_changelog: true
```

## Common Migration Patterns

### Git Tag Operations

| Git Command | Atomic Action |
|-------------|---------------|
| `git tag v1.0.0` | `tag_operations` with `action: create, tag_name: v1.0.0` |
| `git tag -a v1.0.0 -m "Message"` | `tag_operations` with `action: create, tag_name: v1.0.0, message: "Message"` |
| `git push origin v1.0.0` | `tag_operations` with `action: push, tag_name: v1.0.0` |
| `git tag -d v1.0.0` | `tag_operations` with `action: delete, tag_name: v1.0.0` |

### Git Branch Operations

| Git Command | Atomic Action |
|-------------|---------------|
| `git checkout -b feature/x` | `branch_operations` with `action: create, branch_name: feature/x` |
| `git checkout main` | `branch_operations` with `action: checkout, branch_name: main` |
| `git merge feature/x` | `branch_operations` with `action: merge, branch_name: feature/x` |
| `git branch -d feature/x` | `branch_operations` with `action: delete, branch_name: feature/x` |

### Git Commit Operations

| Git Command | Atomic Action |
|-------------|---------------|
| `git commit -m "Message"` | `commit_operations` with `action: create, message: "Message"` |
| `git commit --amend -m "New message"` | `commit_operations` with `action: amend, message: "New message"` |
| `git cherry-pick abc123` | `commit_operations` with `action: cherry-pick, commit_hash: abc123` |
| `git revert abc123` | `commit_operations` with `action: revert, commit_hash: abc123` |

## Advanced Migration Examples

### Example 1: Release Workflow

#### Before:

```yaml
- name: Create Release
  run: |
    # Create release branch
    git checkout -b release/${{ inputs.version }}
    git push origin release/${{ inputs.version }}
    
    # Update version in files
    sed -i "s/version = \".*\"/version = \"${{ inputs.version }}\"/g" version.txt
    git add version.txt
    git commit -m "Bump version to ${{ inputs.version }}"
    
    # Create tag
    git tag ${{ inputs.version }}
    git push origin ${{ inputs.version }}
    
    # Create GitHub Release
    gh release create ${{ inputs.version }} \
      --title "Release ${{ inputs.version }}" \
      --notes "Release notes for ${{ inputs.version }}"
```

#### After:

```yaml
- name: Update version file
  uses: ./actions/core/commit_operations
  with:
    action: create
    message: "Bump version to ${{ inputs.version }}"
    files: "version.txt"

- name: Create Release
  uses: ./actions/composite/release_operations
  with:
    action: create
    version: ${{ inputs.version }}
    release_branch: release/${{ inputs.version }}
    message: "Release ${{ inputs.version }}"
    body: "Release notes for ${{ inputs.version }}"
```

### Example 2: Feature Development Workflow

#### Before:

```yaml
- name: Develop Feature
  run: |
    # Create feature branch
    git checkout -b feature/${{ inputs.feature_name }}
    
    # Make changes
    echo "New content" > feature.txt
    git add feature.txt
    git commit -m "Add ${{ inputs.feature_name }}"
    
    # Push to remote
    git push origin feature/${{ inputs.feature_name }}
```

#### After:

```yaml
- name: Create feature branch
  uses: ./actions/core/branch_operations
  with:
    action: create
    branch_name: feature/${{ inputs.feature_name }}
    base_branch: main
    remote: true

- name: Create feature commit
  uses: ./actions/core/commit_operations
  with:
    action: create
    message: "Add ${{ inputs.feature_name }}"
    files: "feature.txt"
```

## Troubleshooting

### Common Issues

1. **Missing Required Inputs**
   - Error: "tag_name is required for create action"
   - Solution: Check required inputs for each action in the documentation

2. **Permissions Issues**
   - Error: "Permission denied"
   - Solution: Ensure your workflow has the necessary permissions (e.g., `contents: write`)

3. **Input Format Mismatches**
   - Error: "Invalid branch name"
   - Solution: Ensure input formats match requirements (e.g., branch names can't contain spaces)

### Getting Help

If you encounter issues during migration, check:

1. Action documentation for required inputs and behavior
2. GitHub workflow logs for detailed error messages
3. Open an issue in the repository for assistance

## Conclusion

Migrating to atomic Git operations improves maintainability, reusability, and reliability of your workflows. The core/composite pattern allows for flexible combinations of atomic actions while providing ready-to-use composite actions for common scenarios.

By following this guide, you can smoothly transition from monolithic Git script blocks to the new structure, taking advantage of standardized inputs, outputs, and error handling across all Git operations.