# Release Drafter Workflow

This workflow automates the creation and management of GitHub Releases. It maintains a draft release that updates automatically with new changes. It also allows other workflows to trigger release operations via a workflow call.

## Workflow File

`.github/workflows/release-drafter.yml`

---

## Triggers

The workflow responds to two types of events:

1. **Push to the** `**develop**` **branch**:

    - Updates the draft release.
    - Calculates the next version using a centralized version calculation.
    - Updates release notes dynamically.

2. **Workflow call**:

    - Allows other workflows to trigger release operations.
    - Supports custom tag names and options.

---

## Version Calculation

The workflow calculates the next version number using the **version_calculation** Action, based on:

- The latest version tag (`vX.Y.Z` format).
- The number of commits since the last tag.
This ensures consistent and centralized versioning logic across workflows.

**Example:**

- Latest version: `v1.0.16`
- 3 new commits.
- Next calculated version: `v1.0.19`.

---

## Jobs

### 1. Update Release Draft

Triggered when changes are pushed to the `develop` branch:

```yaml
jobs:
  update_release_draft:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
```

**Steps:**

1. **Checkout Repository**:
    - Ensures the `develop` branch is checked out.
    - Fetches the full Git history for accurate version calculations.
2. **Debugging Steps**:
    - Confirms the repository structure and Action files are present.
3. **Calculate Next Version**:
    - Uses the centralized `version_calculation` Action.
4. **Set Output for Version**:
    - Saves the calculated version as a workflow output for future steps.
5. **Draft Release**:
    - Updates the draft release with the calculated version and release notes.

---

### 2. Publish Release (Conditional)

This job is configured to publish a final release if the workflow is triggered with a `refs/tags/v*` reference. It is conditional on such an event being passed to the workflow:

```yaml
jobs:
  publish_release:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
```

**Steps:**

1. **Checkout Repository**:
    - Ensures the correct repository and tag are available.
2. **Publish Final Release**:
    - Publishes the release using the `release-drafter/release-drafter@v6` Action.
    - Uses the provided tag to finalize release notes.

---

## Input Parameters

|Parameter|Description|Required|Default|
|---|---|---|---|
|`tag-name`|Release tag name|No|Current tag|
|`draft`|Create as draft|No|`false`|

---

## Secrets

|   |   |   |   |
|---|---|---|---|
|Secret|Description|Required|Default|
|`token`|GitHub token|No|`GITHUB_TOKEN`|

---

## Release Format

### Draft Release

```markdown
## Draft Release v1.0.X

[Automatically populated release notes]

See the [Changelog](https://github.com/${{ github.repository }}/blob/main/CHANGELOG.md) for more details.
```

---

## Integration

This workflow integrates with:

- Centralized version calculation logic.
- Draft release management.
- Optional release publishing.

---

## Permissions

Required permissions:

```yaml
permissions:
  contents: write
```

---

## Usage Examples

### As Part of Release Process

1. Push changes to the `develop` branch:
    - Updates the draft release.
    - Dynamically calculates the next version.
    - Updates release notes.

---

### Called from Another Workflow

```yaml
jobs:
  release:
    uses: deepworks-net/github.actions/.github/workflows/release-drafter.yml@main
    with:
      tag-name: 'v1.0.0'
      draft: true
```

---

### Troubleshooting

#### Common Issues and Solutions

1. **Version Calculation Fails**:

    - Ensure the repository has at least one version tag.
    - Verify the `version_calculation` Action is properly configured.

2. **Draft Not Updating**:

    - Ensure the branch name matches `develop`.
    - Verify the workflow has write permissions.
    - Check the release-drafter configuration.

---

## Related Documentation

- [release-drafter action](https://github.com/release-drafter/release-drafter)
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
