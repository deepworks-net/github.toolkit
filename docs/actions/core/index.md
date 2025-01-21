# Core Action Structure

This document outlines the standard structure and components required for a core action in the GitHub toolkit.

## Directory Structure

```markdown
actions/core/<action_name>/              # Action root directory
├── action.yml                          # Action metadata and interface
├── Dockerfile                          # Standardized container setup
├── main.py                            # Primary action logic
├── requirements.txt                    # Action dependencies (optional)
└── README.md                          # Action-specific documentation

.github/workflows/
├── core.action.<action_name>.yml       # Reusable workflow wrapper
└── test.core.action.<action_name>.yml  # Test workflow

docs/
├── actions/core/<action_name>/
│   └── index.md                       # Action usage documentation
└── workflows/
    └── <action_name>.md               # Workflow usage documentation
```

## Component Specifications

### 1. action.yml

```yaml
name: "Action Name"
description: "Clear, concise description of action purpose"
author: "Deepworks"

inputs:
  input_name:
    description: "Clear description of input"
    required: false
    default: "default_value"

outputs:
  output_name:
    description: "Clear description of output"

runs:
  using: "docker"
  image: "Dockerfile"

branding:
  icon: "appropriate-icon"
  color: "appropriate-color"
```

### 2. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /action

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Configure git for workspace
RUN git config --global --add safe.directory /github/workspace

# Install Python dependencies (If present)
COPY requirements.txt /action/
RUN pip install --no-cache-dir -r requirements.txt

# Copy action files
COPY *.py /action/
COPY action.yml /action/

ENTRYPOINT ["python", "/action/main.py"]
```

### 3. main.py

```python
#!/usr/bin/env python3

import os
import sys

def validate_inputs():
    """Validate all action inputs."""
    pass

def main():
    """Main action logic."""
    # Get inputs with defaults
    inputs = {
        'input_name': os.environ.get('INPUT_INPUT_NAME', 'default')
    }
    
    # Validate inputs
    validate_inputs(inputs)
    
    # Process action
    outputs = {
        'output_name': 'value'
    }
    
    # Set outputs for GitHub Actions
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        for key, value in outputs.items():
            f.write(f"{key}={value}\n")

if __name__ == "__main__":
    main()
```

### 4. Reusable Workflow (core.action.<action_name>.yml)

```yaml
name: Core (Atomic) Action - Action Name

on:
  workflow_dispatch:
  workflow_call:
    inputs:
      input_name:
        type: string
        required: false
        default: 'default_value'
    outputs:
      output_name:
        description: "Output description"
        value: ${% raw %}{{ jobs.action-job.outputs.output_name }}{% endraw %}

jobs:
  action-job:
    runs-on: ubuntu-latest
    outputs:
      output_name: ${% raw %}{{ steps.action-step.outputs.output_name }}{% endraw %}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Run Action
        id: action-step
        uses: deepworks-net/github.toolkit/actions/core/<action_name>@v1
        with:
          input_name: ${% raw %}{{ inputs.input_name }}{% endraw %}
```

### 5. Test Workflow (test.core.action.<action_name>.yml)

```yaml
name: Test Core Action - Action Name

on:
  pull_request:
    paths:
      - 'actions/core/<action_name>/**'
      - '.github/workflows/core.action.<action_name>.yml'
      - '.github/workflows/test.core.action.<action_name>.yml'
  workflow_dispatch:

jobs:
  test-basic:
    name: Test Basic Functionality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Test Action
        id: action
        uses: ./actions/core/<action_name>
      
      - name: Verify Output Existence
        run: |
          if [[ -z "${% raw %}{{ steps.action.outputs.output_name }}{% endraw %}" ]]; then
            echo "Missing required output"
            exit 1
          fi
      
      - name: Verify Output Value
        run: |
          if [[ "${% raw %}{{ steps.action.outputs.output_name }}{% endraw %}" != "expected_value" ]]; then
            echo "Expected 'expected_value', got '${% raw %}{{ steps.action.outputs.output_name }}{% endraw %}'"
            exit 1
          fi

  test-error-cases:
    # Add error case tests
```

### 6. Documentation Structure

#### Action Documentation (index.md)

``````markdown
# Core Action: Name

## Overview
Clear description of action purpose and functionality

## Usage
```yaml
Example usage code
```

## Inputs
Input documentation table

## Outputs
Output documentation table

## Behavior Matrix
Clear matrix of input/output combinations

## Example Use Cases
Real-world examples

## Error Handling
Documentation of error cases and handling
``````

#### Workflow Documentation (<action_name>.md)

``````markdown
# Action Name Workflow

## Overview
Description of workflow

## Usage
```yaml
Example workflow usage
```

## Inputs/Outputs
Clear documentation of workflow interface

## Behavior
Detailed behavior documentation

## Implementation Examples

Real-world workflow usage examples

``````

## Implementation Requirements

1. **Input Validation**
    - All inputs must be validated
    - Clear error messages for invalid inputs
    - Sensible defaults where possible

2. **Output Handling**
    - All outputs must be documented
    - Use GITHUB_OUTPUT environment file
    - Consistent output format

3. **Error Handling**
    - Clear error messages
    - Appropriate exit codes
    - Comprehensive error documentation

4. **Testing**
    - Test basic functionality
    - Test all error cases
    - Test edge cases
    - Verify all outputs

5. **Documentation**
    - Clear usage examples
    - Complete behavior documentation
    - Error case documentation
    - Real-world examples
