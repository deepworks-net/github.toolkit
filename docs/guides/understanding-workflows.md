# Understanding Workflows in GitHub Toolkit

This guide explains the different types of workflows in the GitHub Toolkit and how they orchestrate actions to create complete automation solutions.

## Overview

Workflows in the GitHub Toolkit are organized into three distinct categories, each serving a specific purpose in the automation ecosystem:

1. **Core Workflows**: Execute single actions with defined interfaces
2. **Flow Workflows**: Orchestrate multi-step business processes
3. **Test Workflows**: Validate and verify system components

## Core Workflows

Core Workflows provide standardized interfaces for executing individual Core Actions. They act as wrappers that make actions reusable across different contexts.

### Characteristics

- **Single Action Execution**: Each workflow executes one Core Action
- **Reusable Interface**: Can be called from other workflows
- **Standardized Parameters**: Consistent input/output patterns
- **Error Handling**: Proper error propagation and status reporting

### Structure Pattern

Core Workflows follow a consistent structure:

```yaml
name: Core - [Action Name]

on:
  workflow_dispatch:  # Manual triggering
  workflow_call:      # Reusable workflow
    inputs:
      # Action-specific inputs
      action:
        type: string
        required: true
        description: "Operation to perform"
    outputs:
      # Action-specific outputs
      result:
        description: "Operation result"
        value: ${{ jobs.main.outputs.result }}

jobs:
  main:
    runs-on: ubuntu-latest
    outputs:
      result: ${{ steps.action.outputs.result }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Execute action
        id: action
        uses: ./actions/core/[action-name]
        with:
          action: ${{ inputs.action }}
          # ... other inputs
```

### Example: Branch Operations Core Workflow

**Location**: `.github/workflows/core.action.branch_operations.yml`

**Purpose**: Provides a reusable interface for branch operations

**Key Features**:
- Supports all branch operations (create, delete, list, checkout, merge, push)
- Configurable parameters for different use cases
- Proper output handling and error propagation
- Manual and programmatic execution support

**Usage**:
```yaml
jobs:
  create-branch:
    uses: ./.github/workflows/core.action.branch_operations.yml
    with:
      action: create
      branch_name: feature/new-feature
      base_branch: main
      remote: true
```

## Flow Workflows

Flow Workflows orchestrate complex business processes by combining multiple Core Workflows and actions in logical sequences.

### Characteristics

- **Multi-Step Processes**: Combine multiple operations
- **Business Logic**: Implement organizational workflows
- **Conditional Execution**: Support branching logic based on conditions
- **State Management**: Handle data flow between steps

### Example: Prepare Release Flow

**Location**: `workflows/prepare-release.yml`

**Purpose**: Automates the complete release preparation process

**Process Flow**:
1. **Trigger**: Activated by pushing a 'prep' tag
2. **Version Calculation**: Determines next version number
3. **Version Updates**: Updates version in configuration files
4. **Release Notes**: Generates release documentation
5. **Changelog Update**: Updates CHANGELOG.md with release information
6. **Branch Creation**: Creates release branch and pull request

**Implementation**:
```yaml
name: Prepare Release Branch

on:
  push:
    tags:
      - 'prep'

jobs:
  create-release-branch:
    if: github.ref_type == 'tag' && github.ref == 'refs/tags/prep'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          ref: staging
          fetch-depth: 0
          
      - name: Calculate Version
        uses: deepworks-net/github.toolkit/actions/version_calculation
        id: version

      - name: Update Version Numbers
        uses: deepworks-net/github.toolkit/actions/version_update
        with:
          version: ${{ steps.version.outputs.next_version }}
          files: 'mkdocs.yml'

      - name: Get Release Content
        uses: deepworks-net/github.toolkit/actions/release_notes
        id: notes
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          mode: 'prepare-release'
          version: ${{ steps.version.outputs.next_version }}

      - name: Update Changelog File
        uses: deepworks-net/github.toolkit/actions/update_changelog
        with:
          content: ${{ steps.notes.outputs.content }}
          mode: 'release'
          version: ${{ steps.version.outputs.next_version }}

      - name: Create Release Branch & PR
        uses: deepworks-net/github.toolkit/actions/git_ops
        with:
          files: 'CHANGELOG.md'
          commit-message: 'Prepare release ${{ steps.version.outputs.next_version }}'
          create-pr: true
          pr-title: 'Release ${{ steps.version.outputs.next_version }}'
```

This workflow demonstrates key Flow Workflow patterns:
- **Sequential Execution**: Each step depends on the previous one
- **Data Passing**: Outputs from one step become inputs to the next
- **Conditional Logic**: Only runs when specific conditions are met
- **Integration**: Combines multiple actions into a cohesive process

### Example: Update Changelog Flow

**Location**: `workflows/update-changelog.yml`

**Purpose**: Automatically updates changelog when PRs are merged

**Process Flow**:
1. **Trigger**: Activated when PR is merged to staging
2. **Version Calculation**: Determines next version
3. **Content Generation**: Creates changelog content from PR information
4. **File Update**: Updates CHANGELOG.md with new content
5. **Commit**: Commits changes back to repository

**Key Features**:
- **Event-Driven**: Responds to PR merge events
- **Conditional Execution**: Only runs for merged PRs
- **Automatic Content Generation**: Creates changelog entries from PR data
- **Repository Integration**: Commits changes automatically

## Test Workflows

Test Workflows validate the integrity and functionality of the toolkit components.

### Test Framework Workflow

**Location**: `.github/workflows/test.framework.yml`

**Purpose**: Comprehensive testing of all toolkit components

**Test Categories**:

1. **Unit and Integration Tests**:
   - Matrix testing across multiple actions
   - Coverage verification (minimum 80%)
   - Dependency validation

2. **Framework Validation**:
   - Test template verification
   - Documentation completeness
   - Fixture availability

3. **Code Quality**:
   - Python linting with flake8
   - Syntax validation
   - Complexity analysis

**Implementation Highlights**:
```yaml
strategy:
  matrix:
    action-path:
      - actions/core/branch_operations
      - actions/core/version_calculator
      - actions/core/version_updater
      - actions/core/manage_release

steps:
  - name: Run tests
    working-directory: ${{ matrix.action-path }}
    run: |
      pytest --cov=. --cov-report=xml --cov-report=term-missing
  
  - name: Verify coverage threshold
    working-directory: ${{ matrix.action-path }}
    run: |
      COVERAGE=$(python -c "import xml.etree.ElementTree as ET; tree = ET.parse('coverage.xml'); root = tree.getroot(); print(root.attrib['line-rate'])")
      COVERAGE_PCT=$(echo "$COVERAGE * 100" | bc)
      if (( $(echo "$COVERAGE_PCT < 80" | bc -l) )); then
        echo "Error: Code coverage is below 80%"
        exit 1
      fi
```

## Workflow Naming Conventions

The toolkit uses a structured naming convention to organize workflows:

### Core Workflows
- **Pattern**: `core.action.[action-name].yml`
- **Purpose**: Reusable wrappers for Core Actions
- **Examples**: 
  - `core.action.branch_operations.yml`
  - `core.action.version_calculator.yml`

### Flow Workflows
- **Pattern**: `flow.[process-name].yml` or `[process-name].yml`
- **Purpose**: Business process orchestration
- **Examples**:
  - `flow.prepare-release.yml`
  - `update-changelog.yml`

### Test Workflows
- **Pattern**: `test.[component].yml`
- **Purpose**: Validation and verification
- **Examples**:
  - `test.framework.yml`
  - `test.core.action.branch_operations.yml`

## Workflow Anatomy

### Common Components

All workflows share these common elements:

#### Triggers (on:)
```yaml
on:
  push:
    branches: [main, staging]
  pull_request:
    types: [closed]
  workflow_call:
    inputs:
      # Reusable workflow inputs
  workflow_dispatch:
    # Manual triggering
```

#### Jobs Structure
```yaml
jobs:
  job-name:
    runs-on: ubuntu-latest
    if: # Conditional execution
    outputs:
      # Job outputs
    steps:
      # Sequential steps
```

#### Steps Composition
```yaml
steps:
  - name: Checkout Repository
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
  
  - name: Execute Action
    uses: ./actions/core/action-name
    with:
      # Action inputs
    
  - name: Process Results
    run: |
      # Shell commands
```

### Integration Patterns

#### Parameter Passing
```yaml
# From workflow input to action
with:
  version: ${{ inputs.version }}
  content: ${{ steps.previous.outputs.content }}
```

#### Secret Management
```yaml
# Secure token handling
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}
env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Conditional Execution
```yaml
# Conditional job execution
if: github.event.pull_request.merged == true

# Conditional step execution
- name: Deploy
  if: steps.tests.outputs.result == 'success'
```

## Best Practices

### Workflow Design

1. **Single Responsibility**: Each workflow should have a clear, single purpose
2. **Reusability**: Design workflows to be called from other workflows
3. **Error Handling**: Implement proper error handling and status reporting
4. **Documentation**: Include clear descriptions and usage examples

### Integration Patterns

1. **Consistent Interfaces**: Use standardized input/output patterns
2. **Proper Permissions**: Set minimal required permissions
3. **Secure Secrets**: Handle sensitive information securely
4. **Conditional Logic**: Use conditions to control execution flow

### Testing and Validation

1. **Comprehensive Testing**: Test all workflow paths and conditions
2. **Matrix Testing**: Use matrix strategies for testing multiple configurations
3. **Coverage Requirements**: Maintain minimum 80% test coverage
4. **Automated Validation**: Include automated validation in CI/CD

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure workflows have required permissions
2. **Secret Issues**: Verify secret names and availability
3. **Conditional Logic**: Check condition syntax and evaluation
4. **Action Versions**: Ensure correct action versions are specified

### Debugging Techniques

1. **Enable Debug Logging**: Set `ACTIONS_STEP_DEBUG=true`
2. **Add Debug Steps**: Include debug output in workflows
3. **Check Action Logs**: Review individual action execution logs
4. **Validate Inputs**: Verify input values and types

## Related Guides

- [Understanding Actions](understanding-actions.md) - Learn about actions used in workflows
- [Understanding FCM Bridge](understanding-fcm-bridge.md) - Understand action generation
- [Testing Framework](testing-framework.md) - Testing patterns and requirements