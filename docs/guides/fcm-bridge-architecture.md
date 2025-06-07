# FCM Bridge Architecture Guide

## Overview

The FCM Bridge Architecture maintains GitHub Actions compatibility while achieving architectural purity through automated generation. This system resolves the duality between Formal Conceptual Models (FCM) and GitHub's practical requirements.

## Architecture Principles

### Duality Resolution

The bridge system maintains two complementary layers:

- **Source Layer**: Pure FCM definitions without operational concerns
- **Interface Layer**: GitHub-compatible actions for practical use
- **Bridge Layer**: Automated generation maintaining perfect synchronization

### Single Source of Truth

All capabilities are defined once in FCM format:

```
axioms/git/tag-operations.fcm  →  actions/core/tag-operations/
```

The `actions/` directory becomes a "compiled" view of the architecture, similar to how binary files are generated from source code.

## Directory Structure

```
github.toolkit/
├── axioms/                    # SOURCE: Pure FCM definitions
│   ├── git/                   # Git operations
│   ├── version/               # Version management
│   ├── release/               # Release processes
│   └── github/                # GitHub-specific operations
├── logic/                     # SOURCE: Relationships
├── patterns/                  # SOURCE: Workflows
├── mechanics/                 # SOURCE: Templates
├── reflection/                # SOURCE: Meta-capabilities
├── emergence/                 # SOURCE: System properties
│
├── .bridge/                   # BRIDGE: Generation machinery
│   ├── generator.py           # FCM-to-action compiler
│   ├── validator.py           # Alignment checker
│   └── manifest.json          # Source-to-interface map
│
└── actions/                   # INTERFACE: GitHub conventions
    ├── core/                  # Generated from axioms
    └── composite/             # Generated from patterns
```

## FCM Format

### Basic Structure

```
# capability-name.fcm
Model: domain.capability-name
Version: 1.0.0
Layer: Axiom
Domain: git

Capability: Brief description of what this does

Parameters:
  - param_name: type|options (optional)
  - action: create|delete|list|push|check
  - tag_name: string (optional)

Outputs:
  - output_name
  - operation_status

Interface:
  type: docker
  image: python:3.9-slim
  requirements: [git]

Dependencies:
  - git
  - github-token (optional)

Patterns:
  - pattern-name
  - category-operation
```

### Parameter Types

- **string**: Text input
- **boolean**: True/false value
- **choice**: Enumerated options (pipe-separated)
- **optional**: Mark with `(optional)` suffix

## Bridge Generation Process

### 1. FCM Parsing

The generator parses FCM files to extract:
- Capability metadata
- Parameter definitions  
- Output specifications
- Interface requirements
- Dependencies

### 2. Action Generation

Creates GitHub-compatible structure:

```yaml
# Generated action.yml
name: Capability Name
description: FCM capability description
inputs:
  param_name:
    description: Parameter description
    required: true/false
outputs:
  output_name:
    description: Output description
runs:
  using: docker
  image: Dockerfile
```

### 3. Dockerfile Generation

Creates container definition from FCM interface:

```dockerfile
# Generated Dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y git
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

### 4. Metadata Tracking

Creates `.bridge-sync` file:

```json
{
  "source": "axioms/git/tag-operations.fcm",
  "generated": "2025-01-06T12:00:00Z",
  "version": "1.0.0",
  "checksum": "sha256:abc123..."
}
```

## Working with the Bridge

### Creating New Capabilities

1. **Define FCM**: Create new file in appropriate `axioms/` subdirectory
2. **Generate Action**: Run `.bridge/generator.py axioms/domain/name.fcm`
3. **Validate**: Run `.bridge/validator.py` to ensure alignment
4. **Implement**: Provide external implementation package

### Modifying Existing Capabilities

1. **Edit FCM**: Modify source definition in `axioms/`
2. **Regenerate**: Run generator on modified FCM
3. **Validate**: Check alignment and GitHub compatibility
4. **Never Edit Actions**: Changes to `actions/` will be overwritten

### Bridge Commands

```bash
# Generate all actions from FCMs
./.bridge/generator.py --generate-all

# Generate specific action
./.bridge/generator.py axioms/git/tag-operations.fcm

# Validate all alignments
./.bridge/validator.py

# Check specific action alignment
./.bridge/validator.py actions/core/tag-operations
```

## Validation System

### Automatic Checks

The validator ensures:

- ✅ Every FCM has corresponding action
- ✅ Every action has sync metadata
- ✅ Checksums match between source and generated
- ✅ No manual edits in generated files
- ✅ GitHub Actions compatibility

### Sync Monitoring

The bridge tracks:
- **Source-to-interface mappings**
- **Generation timestamps**
- **FCM version tracking**
- **Checksum validation**

## Best Practices

### FCM Development

1. **Single Capability**: Each FCM defines one atomic capability
2. **Clear Parameters**: Use descriptive names and appropriate types
3. **Minimal Dependencies**: Reduce external requirements
4. **Domain Alignment**: Place FCMs in correct domain directories

### Bridge Maintenance

1. **Regular Validation**: Run validator after FCM changes
2. **Clean Generation**: Always regenerate after modifications
3. **Version Tracking**: Update FCM versions for significant changes
4. **Documentation Sync**: Keep documentation aligned with FCMs

### GitHub Integration

1. **Use Generated Actions**: Reference actions from `actions/` directory
2. **External Implementation**: Provide actual functionality via packages
3. **Testing**: Test generated actions in real workflows
4. **Compatibility**: Ensure GitHub Actions requirements are met

## Migration Strategy

### From Traditional Actions

1. **Analyze Existing**: Review current action structure
2. **Extract FCM**: Create FCM definition capturing capability
3. **Generate New**: Create action from FCM
4. **Compare**: Validate functionality equivalence
5. **Replace**: Swap traditional action with generated version

### Validation Process

1. **Functional Testing**: Ensure generated actions work
2. **Parameter Mapping**: Verify all inputs/outputs preserved
3. **Workflow Integration**: Test in actual GitHub workflows
4. **Documentation Update**: Reflect changes in guides

## Troubleshooting

### Common Issues

**Generation Fails**:
- Check FCM syntax
- Verify required sections
- Review parameter definitions

**Validation Errors**:
- Ensure FCM unchanged since generation
- Check for manual edits in actions
- Verify sync file integrity

**GitHub Compatibility**:
- Validate action.yml structure
- Check required GitHub Action fields
- Test in actual workflow

### Debug Commands

```bash
# Check FCM syntax
cat axioms/domain/name.fcm

# View generation manifest
cat .bridge/manifest.json

# Check sync status
cat actions/core/name/.bridge-sync

# Test action locally
act -j test-action
```

## Future Enhancements

### Planned Features

- **Pattern Generation**: Composite actions from workflow patterns
- **Dependency Resolution**: Automatic external package management
- **Live Monitoring**: Real-time sync validation
- **Template Evolution**: Improved mechanics templates

### Integration Opportunities

- **GitHub Packages**: Automatic implementation hosting
- **CI/CD Integration**: Automated generation triggers
- **Documentation Generation**: Automatic docs from FCMs
- **Testing Framework**: Automated action testing

## Conclusion

The FCM Bridge Architecture provides a robust foundation for maintaining both architectural purity and practical GitHub compatibility. By treating actions as compiled artifacts from FCM sources, the system ensures consistency while enabling rapid iteration and reliable automation.