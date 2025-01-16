# Core Actions

## What are Core Actions?

Core actions are atomic, self-contained operations that serve as the fundamental building blocks in our GitHub Actions toolkit. They follow the principle of "do one thing and do it well," making them highly reusable and maintainable.

## Characteristics

### Atomic Operations

- Each core action performs a single, well-defined task
- Inputs and outputs are clearly specified
- No hidden dependencies or side effects

### Self-Contained

- Includes all necessary dependencies
- Uses standardized Docker configurations
- Independent of external services (except GitHub)

### Testable

- Comprehensive test suites
- Predictable outcomes
- Clear error conditions

## Standard Structure

```FILEDIR
actions/core/<action-name>/
├── main.py                 # Primary action logic
├── action.yml             # Action metadata
├── Dockerfile             # Standardized container config
└── README.md             # Action documentation
```

## Docker Configuration Standard

All core actions use a standardized Dockerfile structure:

```dockerfile
FROM python:3.9-slim

WORKDIR /action

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Configure git for workspace
RUN git config --global --add safe.directory /github/workspace

# Install Python dependencies (if needed)
# RUN pip install <dependencies>

# Copy action files
COPY *.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/main.py"]
```

## Available Core Actions

### Version Management

- [Version Calculator](version_calculator/index.md): Calculates next version from Git history
- [Version Updater](version_updater/index.md): Updates version numbers in files

## Best Practices

### Input Validation

- Validate all inputs before processing
- Provide clear error messages
- Fail fast on invalid inputs

### Output Formatting

- Use GitHub Actions output syntax
- Document all possible outputs
- Include error details in outputs

### Error Handling

- Graceful failure modes
- Clear error messages
- Appropriate exit codes

### Documentation

- Clear usage examples
- Complete input/output documentation
- Error handling guidance

## Testing

Each core action includes a test workflow:

```yaml
.github/workflows/test.core.action.<name>.yml
```

Tests validate:

- Basic functionality
- Edge cases
- Error conditions
- Input variations
