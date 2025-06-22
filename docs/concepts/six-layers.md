# Six-Layer Architecture

> ⚠️ **Documentation Warning**: This page describes a conceptual architectural model that may not fully reflect the current implementation. The "six-layer" terminology and specific layer definitions need validation against the actual codebase. See [Documentation Gaps](../development/documentation-gaps.md) for more information.

The GitHub Toolkit appears to employ a layered architecture that organizes capabilities from basic operations to complex solutions. This page attempts to document the observed patterns but requires verification.

## Architecture Overview

```
┌─────────────────────────────────────┐
│        6. ECOSYSTEMS               │ Complete solutions
├─────────────────────────────────────┤
│        5. ORGANISMS                │ Complex workflows
├─────────────────────────────────────┤
│        4. MOLECULES                │ Composite actions
├─────────────────────────────────────┤
│        3. ATOMS                    │ Basic actions
├─────────────────────────────────────┤
│        2. PARTICLES                │ Shared utilities
├─────────────────────────────────────┤
│        1. AXIOMS                   │ Core capabilities
└─────────────────────────────────────┘
```

## Layer Definitions

### 1. Axioms (Foundation Layer)
**Purpose**: Define fundamental capabilities as FCM (Functional Capability Model) files

**Characteristics**:
- Source of truth for all generated actions
- Domain-specific capability definitions
- No implementation logic, pure specifications
- Located in `axioms/` directory

**Example**:
```fcm
Model: git.branch-operations
Version: 1.0.0
Layer: Axiom
Domain: git
Capability: Create, delete, list branches
```

### 2. Particles (Utility Layer)
**Purpose**: Shared utilities and helper functions used across multiple actions

**Characteristics**:
- Reusable code snippets
- Common patterns and functions
- Not exposed as actions themselves
- Support code for higher layers

**Examples**:
- Git command utilities
- Error handling functions
- Input validation helpers
- Output formatting utilities

### 3. Atoms (Core Actions Layer)
**Purpose**: Basic, single-purpose GitHub Actions generated from Axioms

**Characteristics**:
- Generated automatically from FCM definitions
- Atomic operations (do one thing well)
- Hyphenated names (e.g., `branch-operations`)
- Located in `actions/core/`

**Examples**:
- `branch-operations`: Create, delete, list branches
- `tag-operations`: Manage Git tags
- `commit-operations`: Handle commits

### 4. Molecules (Composite Actions Layer)
**Purpose**: Combine multiple atoms into higher-level operations

**Characteristics**:
- Manually created composite actions
- Underscore naming (e.g., `git_ops`)
- Orchestrate multiple atomic actions
- Located in `actions/composite/`

**Examples**:
- `git_ops`: Combines branch, commit, and push operations
- `release_operations`: Orchestrates release workflow
- `update_changelog`: Manages changelog updates

### 5. Organisms (Workflow Layer)
**Purpose**: Complete workflow implementations for specific processes

**Characteristics**:
- Full GitHub workflow files
- Implement business processes
- Use molecules and atoms
- Located in `.github/workflows/`

**Examples**:
- `prepare-release.yml`: Complete release preparation
- `update-changelog.yml`: Changelog management workflow
- `create-release-tag.yml`: Tag creation workflow

### 6. Ecosystems (Solution Layer)
**Purpose**: Complete, integrated solutions for entire domains

**Characteristics**:
- Full end-to-end automation
- Multiple workflows working together
- Complete CI/CD pipelines
- Domain-specific solutions

**Examples**:
- Complete release management system
- Full project automation suite
- Integrated development workflow

## Layer Interactions

### Bottom-Up Dependencies
```
Axioms → Atoms → Molecules → Organisms → Ecosystems
```

Each layer can only depend on layers below it:
- Atoms are generated from Axioms
- Molecules use Atoms
- Organisms use Molecules and Atoms
- Ecosystems orchestrate Organisms

### Communication Patterns

1. **Parameter Passing**: Higher layers pass parameters to lower layers
2. **Output Consumption**: Higher layers consume outputs from lower layers
3. **Error Propagation**: Errors bubble up through layers
4. **State Management**: Each layer manages its own state

## Implementation Guidelines

### Axiom Layer Rules
1. Define capabilities, not implementations
2. Keep specifications atomic and focused
3. Version changes carefully
4. Document all parameters and outputs

### Atom Layer Rules
1. Never edit generated files directly
2. Implement single, focused operations
3. Follow LCMCP pattern for Git operations
4. Provide comprehensive error handling

### Molecule Layer Rules
1. Combine atoms for specific use cases
2. Add value through orchestration
3. Handle complex state management
4. Provide clear interfaces

### Organism Layer Rules
1. Implement complete business processes
2. Handle all edge cases
3. Provide clear documentation
4. Include error recovery

### Ecosystem Layer Rules
1. Provide complete solutions
2. Document integration points
3. Include deployment guides
4. Maintain backward compatibility

## Benefits of Layered Architecture

### 1. Modularity
- Each layer has clear responsibilities
- Components are loosely coupled
- Easy to modify individual layers

### 2. Reusability
- Lower layers used by multiple higher layers
- Common patterns implemented once
- Reduced code duplication

### 3. Testability
- Each layer can be tested independently
- Clear interfaces between layers
- Isolated failure points

### 4. Maintainability
- Changes isolated to specific layers
- Clear dependency management
- Predictable impact analysis

### 5. Scalability
- New capabilities added at appropriate layer
- Existing layers extended without breaking changes
- Growth doesn't increase complexity exponentially

## Practical Examples

### Example 1: Creating a Release
```
Ecosystem: Release Management System
    ↓
Organism: prepare-release.yml workflow
    ↓
Molecules: git_ops, release_operations
    ↓
Atoms: branch-operations, tag-operations, commit-operations
    ↓
Axioms: git.branch-operations.fcm, git.tag-operations.fcm
```

### Example 2: Managing Versions
```
Organism: Version update workflow
    ↓
Molecules: version_update composite action
    ↓
Atoms: version-calculator, version-updater
    ↓
Axioms: versioning.calculator.fcm, versioning.updater.fcm
```

## Best Practices

### 1. Layer Selection
- Start at the lowest appropriate layer
- Don't skip layers unnecessarily
- Consider reusability needs

### 2. Interface Design
- Keep interfaces simple and clear
- Document all inputs and outputs
- Version interfaces carefully

### 3. Error Handling
- Handle errors at appropriate layer
- Provide meaningful error messages
- Include recovery mechanisms

### 4. Documentation
- Document each layer's purpose
- Provide usage examples
- Maintain architecture diagrams

## Migration Strategy

When adding new capabilities:

1. **Identify the Layer**: Determine appropriate architectural layer
2. **Check Existing Components**: Reuse lower-layer components
3. **Design Interfaces**: Define clear inputs and outputs
4. **Implement**: Follow layer-specific guidelines
5. **Test**: Validate at each layer
6. **Document**: Update architecture documentation

## Summary

The six-layer architecture provides a robust foundation for building scalable GitHub automation. By understanding and following this architecture, you ensure that your contributions maintain the toolkit's quality, consistency, and maintainability standards.