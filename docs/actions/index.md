# Custom Actions

This guide explains how to use GitHub Actions—tools that automate tasks in your projects to save time and improve reliability.

## What Actions Can Do

### Version Calculator

**[Click Here to Learn More](version_calculator/index.md)**
This action calculates the next version number using your Git history. Ideal for:

- Preparing releases
- Tracking version numbers
- Generating changelogs

**Key Features:**

- Adheres to semantic versioning rules (major, minor, patch)
- Analyzes your Git history to determine the version
- Operates in a containerized environment for consistent execution

### Changelog Update

**[Click Here to Learn More](changelog_update/index.md)**
This action synchronizes the repository's `CHANGELOG.md` with content from the draft release. It ensures an "Unreleased" section reflects all recent changes.

**Key Features:**

- Fetches draft release details using the GitHub API
- Updates or creates an "Unreleased" section with recent changes
- Maintains consistent formatting aligned with the repository's changelog style

---

## How to Use These Actions

You can integrate an action into your workflow with the following syntax:

```yaml
steps:
  - name: Use a GitHub Action
    uses: ./actions/<action-name>
```

### Tips for Success

1. **Choose the Right Version**
    - Use specific tags or commit references for production environments to prevent unexpected changes.
    - Use relative paths when testing actions locally.

2. **Define Inputs and Outputs**
    - Clearly specify required inputs and produced outputs.
    - Use descriptive output names for easy referencing.

3. **Handle Errors Gracefully**
    - Ensure the action manages errors without breaking the workflow.
    - Provide clear, actionable error messages to simplify debugging.

---

## Making New Actions

### Organizing Your Files

Store action-related files in the following structure:

```plaintext
actions/
└── <action-name>/
    ├── action.yml      # Defines the action's behavior
    ├── Dockerfile      # Required if using a container
    ├── script.ext      # The main action logic
    └── README.md       # Documentation for usage
```

### Key Steps

- **Write Clear Documentation**: Include usage examples, input/output descriptions, and dependencies.
- **Thoroughly Test**: Validate your action independently and within workflows, including failure scenarios.
- **Keep It Updated**: Regularly update your action to fix bugs and support new features.

---

## Adding Actions to Workflows

These actions are designed to integrate seamlessly into workflows. Refer to the [Workflows section](../workflows/index.md) for practical examples.

---

## Creating Your Own Actions

Follow these steps to build a custom action:

1. **Set Up**
    - Create a folder: `mkdir -p actions/<your-action-name>`
    - Add the following files:
        - `action.yml`
        - `README.md`
        - Any additional scripts or assets

2. **Document Your Action**
    - Create a usage guide in `docs/actions/`.
    - Update `mkdocs.yml` to include your new action in the navigation menu.

3. **Submit Your Work**
    - Include tests to validate functionality.
    - Follow consistent naming conventions for files and folders.
    - Ensure your documentation is clear and accessible.

---

## Future Action Ideas

Consider developing these actions to enhance workflows:

1. Automatic changelog generation from commits
2. Documentation validation for errors or omissions
3. Configuration file management across projects

---

## Helpful Links

- [GitHub Actions Basics](https://docs.github.com/en/actions)
- [How to Create Actions](https://docs.github.com/en/actions/creating-actions)
- [Actions in Containers](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
