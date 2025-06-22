# Development

Welcome to the Development section of the GitHub Toolkit documentation. This section provides comprehensive guidance for contributors, maintainers, and anyone looking to extend or modify the toolkit.

## Getting Started as a Contributor

### Prerequisites
- Understanding of [Core Concepts](../concepts/index.md)
- Familiarity with GitHub Actions
- Knowledge of Git and Python
- Understanding of the [Architecture](../architecture/index.md)

### Development Environment Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/deepworks-net/github.toolkit.git
   cd github.toolkit
   ```

2. **Install Dependencies**
   ```bash
   # Install Python dependencies (if any)
   pip install -r requirements.txt
   
   # Install development tools
   make install-dev
   ```

3. **Validate Setup**
   ```bash
   # Run validation suite
   make validate
   
   # Check synchronization
   make sync
   ```

## Contribution Guidelines

### Types of Contributions

#### 1. New Capabilities (FCM-based)
**Purpose**: Add new atomic capabilities to the toolkit

**Process**:
1. Create FCM file in appropriate `axioms/` subdirectory
2. Generate action using bridge system
3. Implement Python logic in generated action
4. Add comprehensive tests
5. Update documentation

**Example**: Adding git stash operations
```fcm
# axioms/git/stash-operations.fcm
Model: git.stash-operations
Version: 1.0.0
Layer: Axiom
Domain: git

Capability: Create, apply, list, and drop git stashes

Parameters:
  - action: create|apply|list|drop|show
  - stash_name: string (optional)
  - message: string (optional)
  - include_untracked: boolean (optional)

Outputs:
  - stash_created
  - stash_applied
  - stashes_list
  - operation_status
```

#### 2. Composite Actions
**Purpose**: Combine existing capabilities for higher-level operations

**Process**:
1. Identify combination of existing actions needed
2. Create composite action in `actions/composite/`
3. Use underscore naming convention
4. Implement error handling and state management
5. Add integration tests

#### 3. Workflows
**Purpose**: Complete automation solutions for specific processes

**Process**:
1. Design workflow using existing actions
2. Follow naming conventions (private vs public)
3. Implement proper triggers and conditions
4. Add comprehensive documentation
5. Test in real scenarios

#### 4. Documentation
**Purpose**: Improve understanding and usability

**Process**:
1. Follow documentation structure
2. Include practical examples
3. Update navigation if needed
4. Validate links and references

### Development Workflow

#### Feature Development
1. **Create Feature Branch**
   ```bash
   git checkout -b feature/descriptive-name
   ```

2. **Develop Incrementally**
   - Make small, focused commits
   - Test frequently
   - Validate changes with `make validate`

3. **Update Documentation**
   - Add or update relevant documentation
   - Include examples and usage patterns
   - Update navigation if needed

4. **Submit Pull Request**
   - Provide clear description
   - Reference any related issues
   - Include testing information

#### Bridge Development
When working with FCM files and generated actions:

1. **Modify FCM File**
   ```bash
   # Edit the capability definition
   vim axioms/git/new-capability.fcm
   ```

2. **Generate Actions**
   ```bash
   # Generate from all FCMs
   make generate
   
   # Or generate specific action
   bash .bridge/production-generator.sh axioms/git/new-capability.fcm
   ```

3. **Implement Logic**
   ```python
   # Edit the generated main.py
   vim actions/core/new-capability/main.py
   ```

4. **Validate Results**
   ```bash
   # Check synchronization
   make sync
   
   # Run validation
   make validate
   ```

### Code Standards

#### FCM Files
- Use clear, descriptive capability descriptions
- Define all parameters with appropriate types
- Include comprehensive output definitions
- Version changes appropriately
- Document complex parameter interactions

#### Python Implementation
- Follow PEP 8 style guidelines
- Implement LCMCP pattern for Git operations
- Provide comprehensive error handling
- Include debug logging
- Use type hints where appropriate

#### Action Interfaces
- Clear parameter descriptions
- Appropriate requirement flags
- Comprehensive output definitions
- Proper default values
- Examples in descriptions

#### Documentation
- Use clear, concise language
- Include practical examples
- Maintain consistent formatting
- Update cross-references
- Test all code examples

### Testing Requirements

#### Unit Tests
- Test each function independently
- Cover success and failure scenarios
- Mock external dependencies
- Validate input/output handling

#### Integration Tests
- Test actions in realistic workflows
- Verify cross-action compatibility
- Test error propagation
- Validate end-to-end scenarios

#### Validation Tests
- Ensure FCM files are valid
- Verify generated actions are correct
- Check synchronization consistency
- Validate documentation links

### Release Process

The toolkit follows a structured release process:

#### Version Management
- **Major**: Breaking changes or significant new functionality
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes and minor improvements

#### Release Workflow
1. **[Release Process](release-process.md)** - Detailed release procedures
2. **Version calculation** using semantic versioning
3. **Automated changelog generation**
4. **Tag creation and release notes**

#### Quality Gates
- All tests must pass
- Documentation must be updated
- Validation suite must succeed
- Manual review by maintainers

## Advanced Topics

### Bridge System Development
- Understanding the generation pipeline
- Extending templates and generators
- Adding new FCM features
- Custom validation rules

### Performance Optimization
- Profiling action execution
- Optimizing Docker images
- Reducing workflow complexity
- Caching strategies

### Integration Development
- Adding new domains
- Creating domain-specific patterns
- Implementing custom workflows
- External system integration

## Troubleshooting Development Issues

### Common Problems

#### Generation Failures
```bash
# Check FCM syntax
cat axioms/domain/capability.fcm

# Validate FCM structure
make validate-fcm

# Check generation logs
bash .bridge/production-generator.sh --verbose
```

#### Synchronization Issues
```bash
# Check sync status
make sync

# Force regeneration
make clean && make generate

# Verify checksums
cat actions/core/action-name/.bridge-sync
```

#### Testing Failures
```bash
# Run specific tests
make test-action action=branch-operations

# Debug test failures
make test-debug

# Check test logs
cat test-results.log
```

### Getting Help

#### Documentation
- Review [Architecture](../architecture/index.md) for deep understanding
- Check [User Guide](../guides/index.md) for usage patterns
- Consult [Reference](../actions/index.md) for API details

#### Community
- Open GitHub issues for bugs
- Create discussions for questions
- Submit pull requests for improvements
- Join development meetings (if available)

#### Documentation
- Check [Documentation Gaps](documentation-gaps.md) for areas needing content
- Contribute to incomplete documentation
- Verify existing content accuracy

## Development Tools

### Makefile Commands
```bash
make help           # Show all available commands
make validate       # Run full validation suite
make generate       # Generate all actions from FCMs
make sync           # Check synchronization status
make test          # Run test suite
make clean         # Clean generated files
make docs          # Build documentation
```

### Scripts and Utilities
- **Bridge Generator**: `.bridge/production-generator.sh`
- **Validation Tools**: `.bridge/production-validator.sh`
- **Sync Checker**: Various sync validation scripts
- **Test Framework**: Comprehensive testing utilities

## Contributing Guidelines

### Pull Request Process
1. **Fork and Branch**: Create feature branch from main
2. **Develop**: Implement changes following standards
3. **Test**: Ensure all tests pass
4. **Document**: Update relevant documentation
5. **Submit**: Create pull request with clear description

### Code Review Process
- Automated checks must pass
- Manual review by maintainers
- Documentation review
- Testing validation
- Approval by at least one maintainer

### Merge Requirements
- All CI checks pass
- Documentation is updated
- Tests are comprehensive
- Code follows standards
- Breaking changes are documented

## Summary

Contributing to the GitHub Toolkit requires understanding of the unique architecture and following established patterns. The development process is designed to maintain high quality while enabling rapid innovation and extension of capabilities.

Whether you're adding new capabilities, improving existing functionality, or enhancing documentation, following these guidelines ensures your contributions integrate seamlessly with the existing system and provide value to the broader community.