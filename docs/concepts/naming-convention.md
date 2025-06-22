# Naming Conventions

> ⚠️ **Documentation Warning**: This page describes observed naming patterns but may overstate their systematic application. The hyphen vs underscore distinction and other conventions need verification against the actual codebase implementation. See [Documentation Gaps](../development/documentation-gaps.md).

The GitHub Toolkit appears to use certain naming patterns that may indicate component characteristics. This documentation attempts to capture observed patterns but requires validation.

## Overview

Naming conventions in the toolkit serve as visual indicators of:
- **Component origin** (generated vs manual)
- **Visibility scope** (private vs public)
- **Architectural layer** (atoms, molecules, organisms)
- **Functional domain** (git, versioning, release)

## Core Naming Patterns

### Hyphen vs Underscore Convention

This is the most important naming distinction in the toolkit:

#### Hyphenated Names (kebab-case)
**Pattern**: `component-name`  
**Indicates**: Generated from FCM files via the bridge system  
**Example**: `branch-operations`, `tag-operations`, `version-calculator`

**Characteristics**:
- Automatically generated
- Should never be edited manually
- Found in `actions/core/` directory
- Have accompanying `.bridge-sync` metadata

#### Underscore Names (snake_case)
**Pattern**: `component_name`  
**Indicates**: Manually created and maintained  
**Example**: `git_ops`, `release_operations`, `update_changelog`

**Characteristics**:
- Hand-crafted implementations
- Can be edited directly
- Found in `actions/composite/` directory
- No bridge synchronization

### Workflow Naming Conventions

#### Private/Internal Workflows
**Pattern**: `.category.name.yml`  
**Purpose**: Repository-specific workflows not for external use  
**Examples**:
- `.flow.update_version.yml`
- `.core.internal_setup.yml`

**Usage**:
```yaml
# Can only be used within the same repository
uses: ./.github/workflows/.flow.update_version.yml
```

#### Public Workflows
**Pattern**: `category.name.yml` (no leading dot)  
**Purpose**: Reusable workflows for external consumption  
**Examples**:
- `flow.prepare-release.yml`
- `core.action.version-calculator.yml`

**Usage**:
```yaml
# Can be used from external repositories
uses: deepworks-net/github.toolkit/.github/workflows/flow.prepare-release.yml@v1
```

### Category Prefixes

#### Core Actions
**Pattern**: `core.action.name`  
**Purpose**: Atomic, reusable operations  
**Example**: `core.action.branch_operations.yml`

#### Flow Workflows
**Pattern**: `flow.name`  
**Purpose**: Higher-level business processes  
**Example**: `flow.prepare-release.yml`

#### Test Workflows
**Pattern**: `test.type.name`  
**Purpose**: Validation and testing  
**Example**: `test.core.action.version_calculator.yml`

## File and Directory Naming

### Action Directories
```
actions/
├── core/                    # Generated actions (hyphenated)
│   ├── branch-operations/
│   ├── tag-operations/
│   └── version-calculator/
├── composite/              # Manual actions (underscored)
│   ├── git_ops/
│   └── release_operations/
```

### FCM Files
**Pattern**: `domain/capability-name.fcm`  
**Location**: `axioms/domain/capability-name.fcm`  
**Examples**:
- `axioms/git/branch-operations.fcm`
- `axioms/versioning/calculator.fcm`

### Documentation Files
**Pattern**: `descriptive-name.md` (always hyphenated)  
**Examples**:
- `understanding-workflows.md`
- `fcm-bridge.md`
- `six-layers.md`

## Domain Naming

### Git Domain
- Prefix: `git.`
- Examples: `git.branch-operations`, `git.tag-operations`

### Versioning Domain
- Prefix: `versioning.`
- Examples: `versioning.calculator`, `versioning.updater`

### Release Domain
- Prefix: `release.`
- Examples: `release.notes`, `release.operations`

## Parameter and Output Naming

### Input Parameters
**Pattern**: `snake_case`  
**Examples**:
- `branch_name`
- `tag_prefix`
- `commit_message`

### Output Variables
**Pattern**: `snake_case`  
**Examples**:
- `operation_status`
- `created_branch`
- `next_version`

## Special Naming Rules

### Version Tags
**Pattern**: `v{major}.{minor}.{patch}`  
**Examples**: `v1.0.0`, `v2.1.3`

### Branch Names
**Development**: `develop`, `main`, `staging`  
**Features**: `feature/description`  
**Releases**: `release/v1.0.0`

### Commit Messages
**Pattern**: `type: description`  
**Types**: `feat`, `fix`, `docs`, `chore`, `test`

## Anti-Patterns to Avoid

### 1. Mixing Conventions
❌ `branch_operations` (underscore for generated action)  
❌ `git-ops` (hyphen for manual action)  
✅ `branch-operations` (generated)  
✅ `git_ops` (manual)

### 2. Unclear Visibility
❌ `flow.internal.yml` (unclear if private)  
✅ `.flow.internal.yml` (clearly private)

### 3. Inconsistent Casing
❌ `Branch-Operations` (mixed case)  
❌ `BRANCH_OPERATIONS` (all caps)  
✅ `branch-operations` (consistent)

### 4. Generic Names
❌ `operations`, `utils`, `helpers`  
✅ `git-operations`, `version-utils`, `release-helpers`

## Migration Guidelines

When renaming components:

1. **Check Dependencies**: Find all references to the old name
2. **Update Systematically**: Rename in order:
   - FCM source (if applicable)
   - Action/workflow files
   - Documentation
   - Tests
3. **Maintain Compatibility**: Consider aliases or redirects
4. **Document Changes**: Update CHANGELOG and migration guides

## Validation Tools

The toolkit includes validation for naming:

```bash
# Check naming conventions
make validate-naming

# Common issues detected:
# - Underscores in generated actions
# - Missing dot prefix for private workflows
# - Inconsistent parameter naming
```

## Quick Reference

| Component Type | Pattern | Example | Location |
|---|---|---|---|
| Generated Action | `hyphen-case` | `branch-operations` | `actions/core/` |
| Manual Action | `snake_case` | `git_ops` | `actions/composite/` |
| Private Workflow | `.prefix.name.yml` | `.flow.internal.yml` | `.github/workflows/` |
| Public Workflow | `prefix.name.yml` | `flow.release.yml` | `.github/workflows/` |
| FCM File | `domain/name.fcm` | `git/branches.fcm` | `axioms/` |
| Parameters | `snake_case` | `branch_name` | Action inputs |
| Documentation | `hyphen-case.md` | `user-guide.md` | `docs/` |

## Summary

Consistent naming conventions are essential for maintaining a clean, understandable codebase. By following these conventions, you help ensure that:
- Component origins are immediately clear
- Public/private boundaries are respected
- The codebase remains navigable
- Automation tools work correctly

Remember: when in doubt, check existing similar components and follow their pattern.