# Custom Actions

This guide explains how to use GitHub Actions—tools that automate tasks in your projects so you don’t have to repeat the same work manually. GitHub Actions make your workflows faster and more reliable.

---

## What Actions Can Do

### Version Calculation

**[Click Here to Learn More](version-calculation/index.md)**  
This action calculates the next version number by looking at your Git history. It’s useful for:

- Preparing releases  
- Keeping track of version numbers  
- Generating changelogs  

**Key Features:**  

- Follows semantic versioning rules (major, minor, patch updates)  
- Uses your project’s Git history to decide the version  
- Runs in a containerized environment for consistency  

---

## How to Use These Actions

You can include an action in your workflow like this:

```yaml
steps:
  - name: Use a GitHub Action
    uses: ./actions/<action-name>
```

### Tips for Success

1. **Choose the Right Version**  
    - Use specific versions (tags or commits) in production to avoid unexpected changes.  
    - Use relative paths for testing locally.  

2. **Inputs and Outputs**  
    - Clearly define what inputs the action needs and what outputs it produces.  
    - Use descriptive names for outputs so they’re easy to reference.  

3. **Handling Errors**  
    - Make sure the action can handle errors without breaking the workflow.  
    - Write clear error messages to make debugging easier.  

---

## Making New Actions

### Organizing Your Files

Store your action files in the correct structure:

```plaintext
actions/
└── <action-name>/
    ├── action.yml      # Defines what the action does
    ├── Dockerfile      # Only if the action uses a container
    ├── script.ext      # The main code for the action
    └── README.md       # Documentation on how to use it
```

### Important Steps

- **Write Clear Documentation**: Provide examples, explain inputs and outputs, and list any tools or dependencies needed.  
- **Test Thoroughly**: Test your action by itself, in real workflows, and under failure scenarios.  
- **Keep It Updated**: Regularly review and update your action to fix bugs and support new features.  

---

## Adding Actions to Workflows

These actions are designed to integrate smoothly with your workflows. For examples of how to use them, check the [Workflows section](../workflows/index.md).

---

## Creating Your Own Actions

If you want to build a new action, follow these steps:

1. **Set Up**  
    - Create a folder: `mkdir -p actions/<your-action-name>`  
    - Add these files:  
        - `action.yml`  
        - `README.md`  
        - Any scripts or files the action needs  

2. **Document It**  
    - Write a guide for using the action in `docs/actions/`.  
    - Update the navigation menu in `mkdocs.yml` so it’s easy to find.  

3. **Submit Your Work**  
    - Include tests to make sure the action works as expected.  
    - Follow consistent naming rules for files and folders.  
    - Ensure your instructions are easy to understand.

---

## Future Action Ideas

Here are some ideas for new actions we might create:

1. Automatically generate changelogs from commits  
2. Validate documentation for errors or missing information  
3. Manage configuration files across projects  

---

## Helpful Links

- [GitHub Actions Basics](https://docs.github.com/en/actions)  
- [How to Make Actions](https://docs.github.com/en/actions/creating-actions)  
- [Actions in Containers](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)  

---
