# Meta-Level Documentation: FCM Architecture and Development Workflows

## Overview

This document provides a meta-level analysis of the repository's Formal Conceptual Model (FCM) architecture and development workflows. The repository has evolved from a traditional action collection to a **six-layer architecture** with bridge-based generation, achieving both architectural purity and GitHub compatibility.

## Architecture Evolution

### Traditional Structure → FCM Architecture

The repository has transformed from mixed architecture-operation structure to pure architectural patterns:

- **Before**: Actions contained both definitions and implementations
- **After**: Pure FCM definitions with generated GitHub interfaces
- **Bridge**: Automated generation maintains GitHub compatibility

### Six-Layer FCM Structure

1. **Axioms** (`axioms/`) - Foundational capability definitions
2. **Logic** (`logic/`) - Compositions and relationships  
3. **Patterns** (`patterns/`) - Reusable workflow structures
4. **Mechanics** (`mechanics/`) - Implementation templates
5. **Reflection** (`reflection/`) - Self-awareness and analysis
6. **Emergence** (`emergence/`) - Discovered system properties

---

## Core Workflows

### 1. **Development Workflow**

#### Purpose

- Supports feature development, bug fixes, and other contributions using a branch-based workflow.

#### Key Components

- **Branches**:
  - `main`: Stable release branch.
  - `staging`: Active development branch for integration testing.
  - Feature branches: For specific tasks or issues.
- **Commits**: Follow conventional commit messages to ensure clarity.
- **Pull Requests (PRs)**: Used to merge feature branches into `staging`.

#### Tools and Actions

- Git CLI for branch management.
- Automated checks triggered by PR events (e.g., linting, testing).

#### Known Issues

- Need for clearer branch naming conventions.
- Standardization of commit message format.

#### Gaps and Recommendations

- Document branch naming conventions explicitly.
- Integrate a commit linter to enforce standards.

---

### 2. **Release Management Workflow**

#### Purpose

- Manages the preparation, validation, and deployment of new releases.

#### Key Components

- **Tagging**:
  - Pre-release tags: `prep-vX.Y.Z` to trigger workflows.
  - Final release tags: `vX.Y.Z` for stable releases.
- **Changelog Updates**: Automated updates during release preparation.
- **Release Branches**: Created during the preparation of major or minor versions.

#### Tools and Actions

- **Release Drafter**: Generates draft release notes based on merged PRs.
- **Generated Actions**: All actions are now generated from FCM axioms:
  - `axioms/version/calculate.fcm` → `actions/core/version-calculator/`
  - `axioms/release/changelog.fcm` → `actions/core/update-changelog/`
  - `axioms/git/tag.fcm` → `actions/core/tag-operations/`

#### Bridge Integration

- **Source of Truth**: FCM definitions in `axioms/`
- **Generated Interface**: GitHub-compatible actions in `actions/`
- **Validation**: Automated alignment checking via `.bridge/validator.py`
- **Regeneration**: Actions updated when FCMs change

#### FCM Migration Status

- ✅ Architecture established
- ✅ Bridge generation system operational  
- ✅ First axiom (tag-operations) generated
- 🔄 Migration of remaining actions in progress

#### Known Issues

- Inconsistent changelog updates during pre-release workflows.
- Potential gaps in tagging validation.

#### Gaps and Recommendations

- Align release draft workflow with GitHub’s generation process.
- Automate validation of tags and ensure consistency with semantic versioning.

---

### 3. **Deployment Workflow**

#### Purpose

- Builds and deploys the documentation site via GitHub Pages.

#### Key Components

- **Pages Workflow**: Automatically deploys changes from `main` to the GitHub Pages site.
- **MkDocs**: Static site generator for documentation.

#### Tools and Actions

- **GitHub Actions**:
  - `mkdocs-gh-pages.yml` for deployment.
- **Dependencies**:
  - Listed in `requirements.txt`.

#### Known Issues

- Occasional version mismatches between deployed site and repository source.
- Lack of validation for MkDocs version consistency.

#### Gaps and Recommendations

- Create a GitHub Action to validate MkDocs version consistency (back burner).
- Add deployment logs for improved troubleshooting.

---

## Testing Strategy

To ensure the reliability of these workflows:

1. **Unit Tests for Custom Actions**:
    - Validate scripts like `version_calculation.py` and `update_changelog.py`.
2. **Integration Tests**:
    - Simulate end-to-end workflows to confirm alignment.
3. **Manual QA**:
    - Periodically review Pages deployments for accuracy.

---

## Documentation Goals

- Create detailed guides for each workflow in the `docs/` directory.
- Ensure README and MkDocs documentation align with actual practices.
- Maintain an up-to-date changelog that reflects all workflow updates.

---

## Next Steps

1. **Audit Existing Workflows**: Review YAML files and custom scripts for inconsistencies.
2. **Refine Documentation**: Ensure all workflows are documented clearly and concisely.
3. **Test and Validate**: Execute workflows to identify and fix gaps.
4. **Abstract and Generalize**: Simplify changelog and versioning processes for flexibility.

---

## Conclusion

By documenting, testing, and refining these workflows, the repository can achieve consistency, clarity, and alignment across development and deployment processes. These steps will help stabilize the repository and move toward the 0.1 milestone.
