# Understanding the FCM Bridge System

The FCM Bridge System is the core innovation of the GitHub Toolkit, enabling the automated generation of GitHub Actions from Formal Conceptual Models (FCMs). This system maintains architectural purity while ensuring practical GitHub compatibility.

## What is the FCM Bridge?

The FCM Bridge is an automated compilation system that:

- **Transforms** FCM definitions into GitHub-compatible actions
- **Maintains** perfect synchronization between source and generated code
- **Validates** alignment between conceptual models and implementations
- **Enforces** the "FCM as single source of truth" principle

### Key Principle: FCMs are Source Code

**Critical Understanding**: Everything in the `actions/` directory is GENERATED. Never edit actions directly—they will be overwritten during regeneration.

```
axioms/git/branch-operations.fcm  →  actions/core/branch_operations/
       (SOURCE)                          (GENERATED)
```

Think of it like compiling source code to binaries:
- FCM files = Source code
- Generated actions = Compiled binaries
- Bridge system = Compiler

## Bridge Architecture

The bridge system resolves the fundamental duality between architectural purity and GitHub's operational requirements:

### Three-Layer Architecture

1. **Source Layer**: Pure FCM definitions (`axioms/`)
2. **Bridge Layer**: Generation and validation machinery (`.bridge/`)
3. **Interface Layer**: GitHub-compatible actions (`actions/`)

```
Repository Structure:
├── axioms/                 # SOURCE: Pure FCM definitions
│   ├── git/               # Git operations
│   │   ├── branch-operations.fcm
│   │   ├── tag-operations.fcm
│   │   └── commit-operations.fcm
│   └── test/              # Test capabilities
│       └── minimal.fcm
│
├── .bridge/               # BRIDGE: Generation system (if exists)
│   ├── generator.py       # FCM-to-action compiler
│   ├── validator.py       # Alignment checker
│   └── manifest.json      # Source mappings
│
└── actions/               # INTERFACE: Generated actions
    ├── core/              # Generated from axioms
    │   ├── branch_operations/
    │   │   ├── action.yml      # Generated
    │   │   ├── Dockerfile      # Generated
    │   │   ├── main.py         # Generated/Manual
    │   │   └── .bridge-sync    # Generation metadata
    │   └── tag_operations/
    └── composite/         # Composite actions
```

## FCM Format Specification

FCMs use a structured format to define capabilities:

### Complete FCM Example

Using `axioms/git/tag-operations.fcm` as reference:

```fcm
# Tag Operations Axiom - Formal Conceptual Model
Model: git.tag-operations
Version: 1.0.0
Layer: Axiom
Domain: git

Capability: Manage git tags with create, delete, list, push, and check operations

Parameters:
  - action: create|delete|list|push|check
  - tag_name: string (optional)
  - message: string (optional)
  - remote: boolean (optional)
  - force: boolean (optional)
  - target_commit: string (optional)
  - prefix: string (optional)

Outputs:
  - tag_created
  - tag_deleted
  - tags_list
  - tag_exists
  - operation_status

Interface:
  type: docker
  image: python:3.9-slim
  requirements: [git]

Dependencies:
  - git
  - github-token (optional)

Patterns:
  - git-operation
  - tag-management
  - version-control
```

### FCM Structure Breakdown

#### Header Section
```fcm
Model: domain.capability-name    # Unique identifier
Version: 1.0.0                 # Semantic version
Layer: Axiom                   # Architectural layer
Domain: git                    # Functional domain
```

#### Capability Description
```fcm
Capability: Brief description of what this capability provides
```

#### Parameters Section
```fcm
Parameters:
  - action: create|delete|list   # Choice parameter with options
  - tag_name: string (optional)  # Optional string parameter
  - force: boolean               # Required boolean parameter
```

**Parameter Types:**
- `string`: Text input
- `boolean`: True/false value
- `number`: Numeric input
- `choice`: Pipe-separated options (`create|delete|list`)
- `(optional)`: Marks parameter as not required

#### Outputs Section
```fcm
Outputs:
  - operation_result    # Simple output name
  - data_list          # List output
  - status_flag        # Boolean output
```

#### Interface Definition
```fcm
Interface:
  type: docker              # Execution type (always docker)
  image: python:3.9-slim    # Base Docker image
  requirements: [git]       # System dependencies
```

#### Dependencies and Patterns
```fcm
Dependencies:
  - git                     # Required system tools
  - github-token (optional) # Optional secrets

Patterns:
  - git-operation          # Capability patterns
  - version-control        # Domain patterns
```

## Generation Process

The bridge system generates GitHub Actions through these steps:

### 1. FCM Parsing
The generator extracts:
- Model metadata and versioning
- Parameter definitions and types
- Output specifications
- Interface requirements
- Dependencies and patterns

### 2. GitHub Action Generation

**Generated `action.yml`:**
```yaml
name: 'Tag Operations'
description: 'Manage git tags with create, delete, list, push, and check operations'
author: 'Deepworks'
inputs:
  action:
    description: 'Tag operation to perform (create, delete, list, push, check)'
    required: true
  tag_name:
    description: 'Name of the tag to operate on'
    required: false
  # ... other parameters
outputs:
  operation_status:
    description: 'Operation result status'
  # ... other outputs
runs:
  using: 'docker'
  image: 'Dockerfile'
```

**Generated `Dockerfile`:**
```dockerfile
FROM python:3.9-slim

# Install git (from FCM requirements)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy implementation
COPY main.py .

# Set entrypoint
ENTRYPOINT ["python", "/app/main.py"]
```

### 3. Sync Metadata Generation

**Generated `.bridge-sync`:**
```json
{
  "source_fcm": "axioms/git/tag-operations.fcm",
  "model": "git.tag-operations",
  "version": "1.0.0",
  "generated_at": "2025-06-07T16:01:14Z",
  "generator_version": "production-1.0.0",
  "checksum": "97af7b6124d0ed7a87e8e6e87c4c61698aa9c35a5220c5c5a8604e13ab7b25e8"
}
```

This metadata enables:
- **Source tracking**: Links action back to originating FCM
- **Version control**: Tracks FCM and generator versions
- **Integrity validation**: Checksum ensures synchronization
- **Generation history**: Timestamps for change tracking

## Working with the Bridge System

### Creating New Capabilities

1. **Define the FCM**: Create a new `.fcm` file in the appropriate `axioms/` subdirectory

```fcm
# axioms/git/new-operation.fcm
Model: git.new-operation
Version: 1.0.0
Layer: Axiom
Domain: git

Capability: Perform new git operation

Parameters:
  - action: create|delete
  - name: string

Outputs:
  - result

Interface:
  type: docker
  image: python:3.9-slim
  requirements: [git]
```

2. **Generate the Action**: Use the bridge generation system

```bash
# Via Makefile
make generate

# Or directly (if .bridge scripts exist)
bash .bridge/production-generator.sh
```

3. **Implement the Logic**: Create the `main.py` implementation following the patterns from existing actions

4. **Validate**: Ensure the generated action works correctly

```bash
# Validation
make validate
```

### Modifying Existing Capabilities

**IMPORTANT**: Never edit generated actions directly. Always modify the FCM source.

1. **Edit the FCM**: Modify the source definition in `axioms/`

```fcm
# Edit axioms/git/branch-operations.fcm
Parameters:
  - action: create|delete|list|checkout|merge
  - new_parameter: string (optional)  # Add new parameter
```

2. **Regenerate**: Run the bridge generation

```bash
make generate
```

3. **Update Implementation**: Modify `main.py` to handle new parameters (if needed)

4. **Validate**: Check that everything works

```bash
make validate
```

### Bridge Commands

The bridge system provides several operational commands via `Makefile.bridge`:

```bash
# Generate all actions from FCMs
make generate

# Validate all generated actions
make validate

# Check synchronization status
make sync

# Check if regeneration is needed
make check

# Clean generated metadata (preserves FCMs)
make clean

# Show help
make help
```

## Bridge Production Pipeline

The bridge system includes automated CI/CD integration:

**Location**: `.github/workflows/bridge-production.yml`

**Triggers**:
- Changes to FCM files (`axioms/**/*.fcm`)
- Changes to bridge system (`.bridge/**`)
- Manual dispatch
- Version tags

**Process**:
1. **Generate**: Creates actions from all FCMs
2. **Validate**: Ensures generated actions are correct
3. **Commit**: Automatically commits generated changes
4. **Push**: Updates repository with generated actions

**Example workflow run**:
```yaml
- name: Generate Actions from FCMs
  run: |
    bash .bridge/production-generator.sh
    
- name: Validate Generated Actions
  run: |
    bash .bridge/production-validator.sh
    
- name: Commit Generated Actions
  if: steps.check-changes.outputs.changes == 'true'
  run: |
    git add actions/
    git commit -m "chore: Regenerate actions from FCMs [skip ci]"
```

## Validation System

The bridge includes comprehensive validation to ensure integrity:

### Automatic Validation Checks

1. **Source-Interface Alignment**: Every FCM has corresponding action
2. **Sync Metadata Validation**: Every generated action has `.bridge-sync`
3. **Checksum Verification**: Generated actions match FCM checksums
4. **GitHub Compatibility**: Actions follow GitHub Action specifications
5. **No Manual Edits**: Ensures generated files haven't been manually modified

### Sync Monitoring

The system tracks:
- **FCM-to-Action mappings**: Which FCM generates which action
- **Generation timestamps**: When actions were last generated
- **Version tracking**: FCM versions and generator versions
- **Integrity checksums**: SHA256 hashes for change detection

### Example Sync Check

```bash
make sync
# Output:
# Checking FCM-Action synchronization...
#   ✓ In sync: axioms/git/branch-operations.fcm
#   ✓ In sync: axioms/git/tag-operations.fcm
#   ✗ Out of sync: axioms/git/commit-operations.fcm
```

## Best Practices

### FCM Development

1. **Single Responsibility**: Each FCM defines one atomic capability
2. **Clear Naming**: Use descriptive model names and parameter names
3. **Proper Typing**: Use appropriate parameter types and constraints
4. **Minimal Dependencies**: Reduce external requirements where possible
5. **Version Management**: Update versions for significant changes

### Bridge Operations

1. **Regular Validation**: Run `make sync` after FCM changes
2. **Clean Generation**: Always regenerate after modifications
3. **Test Generated Actions**: Verify functionality after generation
4. **Document Changes**: Update documentation when FCMs change

### Integration Guidelines

1. **Use Generated Actions**: Always reference actions from `actions/` directory
2. **Implement Logic Separately**: Provide actual functionality in `main.py`
3. **Follow Patterns**: Use established patterns from existing actions
4. **Test Thoroughly**: Include comprehensive test coverage

## Migration from Traditional Actions

### Process

1. **Analyze Existing Action**: Review current structure and functionality
2. **Extract FCM Definition**: Create FCM capturing the capability
3. **Generate New Action**: Use bridge to create action from FCM
4. **Implement Logic**: Port existing logic to generated structure
5. **Validate Functionality**: Ensure equivalent behavior
6. **Replace References**: Update workflows to use generated action

### Example Migration

**Before** (Traditional action):
```yaml
# actions/manual/my-action/action.yml
name: My Action
description: Does something
inputs:
  param1:
    description: Parameter 1
    required: true
# ... manual maintenance
```

**After** (FCM-generated):
```fcm
# axioms/domain/my-action.fcm
Model: domain.my-action
Version: 1.0.0
Layer: Axiom
Domain: domain

Capability: Does something

Parameters:
  - param1: string

Outputs:
  - result

Interface:
  type: docker
  image: python:3.9-slim
```

## Troubleshooting

### Common Issues

**Generation Failures**:
- Check FCM syntax and required sections
- Verify parameter definitions are correct
- Ensure proper indentation and formatting

**Validation Errors**:
- Run `make sync` to check synchronization status
- Verify no manual edits were made to generated files
- Check that FCM hasn't changed since last generation

**Action Compatibility**:
- Validate `action.yml` structure follows GitHub specs
- Test generated actions in actual workflows
- Check Docker image and entrypoint configuration

### Debug Commands

```bash
# Check FCM syntax
cat axioms/git/branch-operations.fcm

# View sync status
cat actions/core/branch_operations/.bridge-sync

# Check generated action
cat actions/core/branch_operations/action.yml

# Test sync status
make sync

# Regenerate specific action (via make)
make clean && make generate
```

## Future Enhancements

The FCM Bridge system is designed for continuous evolution:

### Planned Features
- **Pattern Generation**: Composite actions from workflow patterns
- **Dependency Resolution**: Automatic package management
- **Live Monitoring**: Real-time synchronization validation
- **Enhanced Templates**: Improved generation templates

### Integration Opportunities
- **CI/CD Integration**: Automated generation triggers
- **Documentation Generation**: Automatic docs from FCMs
- **Testing Framework**: Automated action testing
- **Registry Integration**: Automatic action publishing

## Related Guides

- [Understanding Actions](understanding-actions.md) - Learn about generated actions
- [Understanding Workflows](understanding-workflows.md) - How to use generated actions
- [Testing Framework](testing-framework.md) - Testing generated actions

## Summary

The FCM Bridge System is the foundation that enables the GitHub Toolkit to maintain both architectural purity and practical utility. By treating FCMs as source code and actions as compiled artifacts, the system ensures consistency, reliability, and maintainability while providing the flexibility needed for real-world automation.