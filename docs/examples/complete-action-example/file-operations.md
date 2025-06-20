# File Operations Action Documentation

## Overview

The File Operations action demonstrates a complete implementation of the Loosely Coupled Modular Composition Pattern (LCMCP) for GitHub Actions. It provides comprehensive file system operations while maintaining strict encapsulation and modularity.

## Features

- **Complete File Operations**: Create, read, update, delete, copy, move, and search files
- **Multiple Encodings**: Support for UTF-8, ASCII, and Base64 encoding
- **Directory Management**: Automatic directory creation and management
- **Error Handling**: Comprehensive error handling with descriptive messages
- **LCMCP Compliance**: Follows all LCMCP principles for modularity and composition

## Inputs

| Name | Description | Required | Default | Type |
|------|-------------|----------|---------|------|
| `action` | File operation to perform | Yes | - | Choice: create, read, update, delete, copy, move, search |
| `file_path` | Path to the file to operate on | No* | - | String |
| `content` | Content for create/update operations | No | "" | String |
| `destination` | Destination path for copy/move operations | No* | - | String |
| `pattern` | Pattern for search operations (glob) | No* | - | String |
| `encoding` | File encoding | No | utf-8 | Choice: utf-8, ascii, base64 |
| `create_dirs` | Create parent directories if needed | No | true | Boolean |
| `overwrite` | Overwrite existing files | No | false | Boolean |

*Required depending on the action selected

## Outputs

| Name | Description | Available For |
|------|-------------|---------------|
| `operation_status` | Status of the operation (success/failure) | All actions |
| `file_exists` | Whether the file exists (true/false) | All except search |
| `file_created` | Path of created file | create |
| `file_content` | Content of the file | read |
| `file_deleted` | Path of deleted file | delete |
| `files_found` | Comma-separated list of found files | search |
| `file_size` | Size of the file in bytes | create, update, read |

## Usage Examples

### Basic File Creation

```yaml
- name: Create File
  uses: ./examples/complete-action-example/action
  with:
    action: create
    file_path: docs/example.txt
    content: "Hello, World!"
    create_dirs: true
```

### Read File Content

```yaml
- name: Read Configuration
  id: read-config
  uses: ./examples/complete-action-example/action
  with:
    action: read
    file_path: config/settings.json

- name: Use File Content
  run: echo "Config: ${% raw %}{{ steps.read-config.outputs.file_content }}{% endraw %}"
```

### Copy with Directory Creation

```yaml
- name: Copy Template
  uses: ./examples/complete-action-example/action
  with:
    action: copy
    file_path: templates/default.yml
    destination: instances/new-instance/config.yml
    create_dirs: true
    overwrite: true
```

### Search for Files

```yaml
- name: Find Test Files
  id: find-tests
  uses: ./examples/complete-action-example/action
  with:
    action: search
    pattern: "**/*test*.py"

- name: Process Found Files
  run: |
    IFS=',' read -ra FILES <<< "${% raw %}{{ steps.find-tests.outputs.files_found }}{% endraw %}"
    for file in "${FILES[@]}"; do
      echo "Found test file: $file"
    done
```

### Base64 File Operations

```yaml
- name: Create Binary File
  uses: ./examples/complete-action-example/action
  with:
    action: create
    file_path: data/binary.dat
    content: "SGVsbG8gV29ybGQh"  # "Hello World!" in base64
    encoding: base64
```

## Error Handling

The action provides comprehensive error handling:

```yaml
- name: Safe File Operation
  id: file-op
  continue-on-error: true
  uses: ./examples/complete-action-example/action
  with:
    action: read
    file_path: might-not-exist.txt

- name: Handle Result
  run: |
    if [ "${% raw %}{{ steps.file-op.outputs.operation_status }}{% endraw %}" = "success" ]; then
      echo "File content: ${% raw %}{{ steps.file-op.outputs.file_content }}{% endraw %}"
    else
      echo "File operation failed"
    fi
```

## LCMCP Principles Demonstrated

### 1. Modularity
- Single, well-defined responsibility (file operations)
- No dependencies on external actions or workflows
- Complete self-containment

### 2. Encapsulation
- All implementation details hidden inside Docker container
- Clean input/output interface
- No side effects or global state

### 3. Composition
- Can be easily combined with other actions
- Outputs can be inputs to subsequent actions
- No coupling to specific workflows

### 4. Explicit Interfaces
- All inputs and outputs clearly defined
- Type information provided
- Required vs optional inputs specified

### 5. Error Isolation
- Errors are contained within the action
- Clear success/failure status reporting
- Descriptive error messages

## Testing

The action includes comprehensive tests:

```bash
cd examples/complete-action-example/action
pip install -r requirements.txt
pytest --cov=. --cov-report=term-missing
```

### Test Coverage
- **Unit Tests**: Individual method testing
- **Integration Tests**: Complete workflow testing
- **Error Handling**: Failure scenario testing
- **Encoding Tests**: Multiple encoding validation

## Architecture Notes

### Docker Implementation
The action uses Docker for complete environment isolation:
- No host system dependencies
- Consistent execution across environments
- Easy local testing and development

### State Management
The action maintains no persistent state:
- Each execution is independent
- No configuration files or databases
- Pure functional approach

### Performance Considerations
- Minimal container overhead
- Efficient file operations using Python pathlib
- Memory-conscious for large files

## Extending the Action

To add new file operations:

1. Add the operation to the `action` input choices in `action.yml`
2. Implement the method in the `FileOperations` class
3. Add the operation handling in the `main()` function
4. Write comprehensive tests for the new operation
5. Update documentation

## Related Examples

- **Reusable Workflow**: See `workflow/reusable-workflow.yml` for creating reusable patterns
- **Error Handling**: See `workflow/use-action.yml` for comprehensive error handling
- **Testing Patterns**: See `tests/` directory for testing best practices

This action serves as a complete reference implementation for creating GitHub Actions that follow the LCMCP pattern and integrate seamlessly with the GitHub Toolkit architecture.