# Testing Overview

## Test Structure and Organization

### File Structure

```markdown
.github/workflows/
├── core.action.*.yml               # Core action workflows
├── test.core.action.*.yml         # Core action tests
└── test.composite.action.*.yml    # Composite action tests

docs/tests/                        # Test documentation
├── index.md                       # This overview
├── core/                          # Core action test docs
│   ├── version_calculator.md
│   └── version_updater.md
└── composite/                     # Composite action test docs
```

## Test Naming Convention

- `test.core.action.<name>.yml` - Tests for core (atomic) actions
- `test.composite.action.<name>.yml` - Tests for composite actions

## Common Test Patterns

### 1. Input Validation Tests

```yaml
test-invalid-input:
  steps:
    - Run action with invalid input
    - Verify appropriate error
    - Check error messaging
```

### 2. Output Format Tests

```yaml
test-output-format:
  steps:
    - Run action
    - Verify all outputs exist
    - Validate output format
    - Check output values
```

### 3. Error Cases

```yaml
test-error-handling:
  steps:
    - Create error condition
    - Run action with continue-on-error
    - Verify failure behavior
    - Check error messaging
```

## Standard Test Components

### Environment Setup

```yaml
steps:
  - uses: actions/checkout@v4
  - name: Clean Environment
    run: |
      # Setup steps
```

### Output Verification

```yaml
- name: Verify Outputs
  run: |
    # Check output existence
    if [[ -z "${% raw %}{{ steps.action.outputs.output_name }}{% endraw %}" ]]; then
      echo "Missing required output"
      exit 1
    fi
    # Verify output value
    if [[ "${% raw %}{{ steps.action.outputs.output_name }}{% endraw %}" != "expected" ]]; then
      echo "Expected 'expected', got '${% raw %}{{ steps.action.outputs.output_name }}{% endraw %}'"
      exit 1
    fi
```

## Test Categories

### 1. Core Action Tests

- Focus on atomic functionality
- Verify input/output contract
- Test error conditions
- Example: [Version Calculator Tests](core/version_calculator.md)

### 2. Composite Action Tests

- Test integration of core actions
- Verify workflow logic
- Test end-to-end scenarios
- Handle workflow outputs

## Test Documentation

Each test workflow should have corresponding documentation that includes:

1. **Overview**
    - Purpose of tests
    - Test categories
    - Required setup

2. **Test Cases**
    - Individual test descriptions
    - Expected inputs/outputs
    - Error scenarios

3. **Implementation Details**
    - Environment setup
    - Verification methods
    - Clean-up procedures

4. **Local Testing**
    - Setup instructions
    - Required tools
    - Execution steps

## Local Test Execution

To run tests locally:

```bash
# Install act
brew install act  # or equivalent for your OS

# Run specific test workflow
act pull_request -W .github/workflows/test.core.action.version_calculator.yml

# Run all tests
act pull_request
```

## Adding New Tests

When adding new tests:

1. **Follow Naming Convention**

   ```markdown
   test.core.action.<name>.yml
   test.composite.action.<name>.yml
   ```

2. **Include Standard Sections**
    - Environment setup
    - Test cases
    - Output verification
    - Error handling

3. **Document Tests**
    - Create test documentation
    - Update index if needed
    - Include local testing instructions

4. **Test Categories**
    - Input validation
    - Output verification
    - Error handling
    - Edge cases

## Best Practices

1. **Test Independence**
    - Each test should be self-contained
    - Clean up after tests
    - Don't rely on other test results

2. **Clear Error Messages**
    - Descriptive failure outputs
    - Expected vs actual values
    - Clear error conditions

3. **Comprehensive Coverage**
    - Test all inputs
    - Verify all outputs
    - Include error cases
    - Test edge conditions

4. **Documentation**
    - Document test purpose
    - Include example usage
    - Provide troubleshooting tips

## Available Test Suites

### Core Actions

- [Version Calculator Tests](core/version_calculator.md)
- [Version Updater Tests](core/version_updater.md)

### Composite Actions

- [Update Changelog Tests](composite/update_changelog.md)

## Contributing

When contributing new tests:

1. Follow existing patterns
2. Include documentation
3. Test error cases
4. Provide local test instructions
5. Update this index

See [Contributing Guide](../contributing.md) for more details.