# Bridge Testing Infrastructure

This directory contains comprehensive tests for the FCM-to-GitHub bridge system.

## Structure

- **unit/** - Component-level tests for FCM parser and generator
- **integration/** - Cross-component tests for complete workflows  
- **e2e/** - End-to-end tests with real GitHub Actions
- **fixtures/** - Test data and expected outputs

## Running Tests

### Complete Test Suite
```bash
python .bridge/test-harness.py --all
```

### Specific Test Categories
```bash
python .bridge/test-harness.py --unit           # Unit tests only
python .bridge/test-harness.py --integration    # Integration tests only
python .bridge/test-harness.py --e2e            # End-to-end tests only  
python .bridge/test-harness.py --purity         # Architecture purity tests only
```

### Individual Unit Tests
```bash
python .bridge/tests/unit/test_fcm_parser.py
python .bridge/tests/unit/test_generator.py
```

## Test Types

### Unit Tests
- FCM parsing validation
- Action generation logic
- Parameter type handling
- Error scenarios

### Integration Tests  
- Complete FCM-to-Action cycle
- Bridge validation workflow
- Existing action parity checks

### End-to-End Tests
- Generated action structure validation
- GitHub Actions compatibility
- Real workflow execution

### Purity Tests
- No hardcoded values in FCMs
- All generated actions have sync files
- Manual edit detection
- Architecture alignment

## CI Integration

Tests run automatically on:
- Changes to FCM files (`axioms/**/*.fcm`)
- Bridge infrastructure changes (`.bridge/**`)
- Action modifications (`actions/**`)

See `.github/workflows/test.bridge.yml` for the complete CI workflow.

## Adding Tests

1. **Unit Tests**: Add to appropriate file in `unit/`
2. **Test Fixtures**: Add FCM samples to `fixtures/`
3. **Integration Tests**: Extend `test-harness.py` methods
4. **Expected Outputs**: Add to `fixtures/expected_*` files

## Test Results

Results are saved to:
- `.bridge/test-results.json` - Detailed test results
- `.bridge/validation-report.txt` - Validation summary

These files are uploaded as artifacts in CI runs.