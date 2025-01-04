# Prepare Release Workflow

This page documents the **Prepare Release** workflow located in the [.github/workflows/prepare-release.yml](https://github.com/deepworks-net/github.actions/blob/main/.github/workflows/prepare-release.yml) file. This workflow automates the process of preparing a release branch and creating a pull request for review.

---

## Overview

The **Prepare Release** workflow is triggered manually by tagging a commit with the tag: 

`prep` 

It automates the following steps:

- Creates a release branch.
- Moves items from the "Unreleased" section of the changelog to a new versioned section.
- Removes the "Unreleased" section to finalize the changelog for release.
- Creates a pull request (PR) for the release branch.

---

## Trigger

To activate this workflow, push a tag with the prefix `prep-v`. For example:

```bash
git tag prep-v1.0.0
git push origin prep-v1.0.0
```

## Workflow Steps

### 1. **Check Out Repository**

The workflow checks out the repository code to the GitHub Actions runner to perform modifications.

### 2. **Create Release Branch**

A new branch named `release/{version}` is created. The version is extracted from the tag name (e.g., `prep-v1.0.0` creates `release/1.0.0`).

### 3. **Update Changelog**

The workflow:

- Moves all changelog items under the "Unreleased" section to a new version section (e.g., `## [1.0.0]`).
- Adds a date to the new section (based on the workflow run date).
- Removes the "Unreleased" section.

### 4. **Commit Changes**

Commits the updated changelog to the new release branch with a message like:

```arduino
chore: prepare release 1.0.0
```

### 5. **Create Pull Request**

Creates a PR from the release branch to the `main` branch. The PR title includes the version, such as:

makefile

Copy code

`Release: 1.0.0`

---

## Requirements

### Repository Setup

1. A `develop` branch is required for ongoing development.
2. A `Changelog.md` file must exist in the repository root. If not present, the workflow will create one.

### Permissions

- Write access to create branches and push changes.
- Access to create and manage PRs.

---

## Usage Example

1. Ensure your changelog has an "Unreleased" section with pending changes.
2. Tag the repository with a release preparation version:

bash

Copy code

`git tag prep-v2.1.0 git push origin prep-v2.1.0`

3. The workflow will:
    - Create the branch `release/2.1.0`.
    - Update the changelog.
    - Open a PR for review and approval.

---

## Outputs

- **Release Branch:** `release/{version}` (e.g., `release/2.1.0`).
- **Updated Changelog:** Moves changes to the new version section with a date.
- **Pull Request:** A PR for merging the release branch into `main`.

---

## Notes

- If the changelog format deviates from the expected structure, the workflow may fail.
- Manual edits to the changelog after workflow execution are discouraged to maintain consistency.

---

## Troubleshooting

### Workflow Fails

1. Check the workflow logs for details.
2. Verify the tag format (`prep-v{version}`) and changelog structure.

### Missing Changelog

If the `Changelog.md` file is missing, the workflow will create one with a default template.

---

## Contributing

For improvements or fixes to this workflow, follow these steps:

1. Fork the repository.
2. Create a branch from `develop`.
3. Submit a PR with a detailed description of your changes.

---

## License

This workflow is part of the Deepworks project and is licensed under the MIT License.

For more details, visit the repository: [deepworks-net/github.actions](https://github.com/deepworks-net/github.actions)