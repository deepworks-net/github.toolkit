# Custom Actions

This section documents the custom GitHub Actions created for the Deepworks ecosystem. These actions are designed to be reusable components that handle specific tasks across our workflows.

## Available Actions

### Version Calculation

**[View Documentation](version-calculation/index.md)**

Calculates the next semantic version number based on Git history and commit count. Used in:

- Release preparation
- Version tracking
- Changelog management

**Key Features:**

- Automatic version calculation
- Semantic versioning support
- Git history integration
- Container-based execution

## Using Custom Actions

Custom actions can be used in workflows like this:

```yaml
steps:
  - name: Use Custom Action
    uses: ./actions/action-name
```

### Best Practices

1. **Version Reference**
    - Use specific commits or tags for production
    - Use relative paths for local development

2. **Input/Output**
    - Document all inputs and outputs
    - Use meaningful step IDs for output references

3. **Error Handling**
    - Handle action failures gracefully
    - Provide clear error messages

## Action Development

### Structure

Each action should follow this structure:

```directory
actions/
└── action-name/
    ├── action.yml      # Action definition
    ├── Dockerfile      # If container-based
    ├── script.ext      # Main logic
    └── README.md       # Action documentation
```

### Requirements

1. **Documentation**
    - Clear usage examples
    - Input/output documentation
    - Error scenarios
    - Dependencies

2. **Testing**
    - Test in isolation
    - Test in workflows
    - Test error cases

3. **Maintenance**
    - Regular updates
    - Version tracking
    - Dependency management

## Integration with Workflows

Our custom actions are designed to integrate seamlessly with our workflows. See the [Workflows section](../workflows/index.md) for detailed examples of how these actions are used in practice.

## Contributing

To contribute a new action:

1. Create action directory:

    ```bash
    mkdir -p actions/your-action-name
    ```

2. Required files:

    ```git
    - action.yml
    - README.md
    - Implementation files
    ```

3. Document the action:
    - Create documentation under docs/actions/
    - Add to mkdocs.yml navigation
    - Update this index

4. Submit pull request:
    - Include tests
    - Update documentation
    - Follow naming conventions

## Future Actions

Planned custom actions:

1. Semantic changelog parsing
2. Documentation validation
3. Configuration management

## Related Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Custom Actions Guide](https://docs.github.com/en/actions/creating-actions)
- [Container Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)