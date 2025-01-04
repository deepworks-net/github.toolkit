# Create Release Tag Workflow

This workflow is part of the release automation process. It creates and pushes version tags when release PRs are merged to the main branch, triggering the final release publication.

## Workflow File

`.github/workflows/create-tag.yml`

## Trigger

The workflow triggers when pull requests targeting the `main` branch are closed:

```yaml
on:
  pull_request:
    branches:
      - main
    types: [closed]
```

## Conditions

The workflow only runs when:

1. The PR was merged (not just closed)
2. The source branch name starts with `release/v`

```yaml
if: github.event.pull_request.merged == true && startsWith(github.event.pull_request.head.ref, 'release/v')
```

## Process

1. Checks out the repository
2. Extracts version number from the release branch name
3. Creates a git tag with that version
4. Pushes the tag to the repository

## Integration Points

This workflow is part of the release process chain:

1. **Prepare Release** workflow creates release branch (`release/vX.Y.Z`)
2. PR is created targeting main branch
3. PR is reviewed and merged
4. **Create Tag** workflow (this one) creates version tag
5. **Release Drafter** workflow publishes final release

## Version Tag Format

Tags created by this workflow match the release branch name:

- Branch: `release/v1.0.34`
- Creates tag: `v1.0.34`

## Prerequisites

1. Source branch must:
   - Start with `release/v`
   - Contain valid version number
   - Be merged to main branch

2. Repository settings:
   - Allow workflows to create tags
   - Proper access permissions set

## Permissions

The workflow requires:

- Read access to repository
- Write access for tags
- Uses `GITHUB_TOKEN` with default permissions

## Error Handling

The workflow will fail if:

- PR is not actually merged
- Branch name doesn't match pattern
- Tag already exists
- Insufficient permissions

## Usage Example

1. Release PR is created:

   ```
   release/v1.0.34 -> main
   ```

2. PR is merged to main

3. Workflow automatically:

   ```bash
   git tag v1.0.34
   git push origin v1.0.34
   ```

## Troubleshooting

Common issues and solutions:

1. **Tag Creation Fails**
   - Check if tag already exists
   - Verify branch name format
   - Check workflow permissions

2. **Workflow Doesn't Trigger**
   - Verify PR target is main branch
   - Check branch name starts with `release/v`
   - Ensure PR was merged, not just closed

3. **Push Fails**
   - Check repository permissions
   - Verify token access
   - Review workflow logs

## Related Workflows

- [Prepare Release](prepare-release.md)
- [Release Drafter](release-drafter.md)
- [Update Changelog](update-changelog.md)

## Next Steps

After this workflow runs:

1. Version tag is created
2. Release Drafter workflow triggers
3. Final release is published

## Contributing

To modify this workflow:

1. Fork the repository
2. Edit `.github/workflows/create-tag.yml`
3. Test with a release branch
4. Submit a pull request