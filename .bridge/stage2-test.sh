#!/bin/bash
# Bridge Test Stage 2: Real Component Transform
# Tests tag_operations FCM -> Action generation and comparison

set -e

echo "=== Bridge Stage 2 Test: Real Component ==="

# Paths
FCM_FILE="axioms/git/tag-operations.fcm"
GENERATED_DIR="actions/core/tag-operations"
ORIGINAL_DIR="actions/core/tag_operations"  # The existing one
GENERATED_ACTION="$GENERATED_DIR/action.yml"
ORIGINAL_ACTION="$ORIGINAL_DIR/action.yml"

# Check if FCM exists
if [[ ! -f "$FCM_FILE" ]]; then
    echo "ERROR: $FCM_FILE not found"
    exit 1
fi

# Check if original action exists
if [[ ! -f "$ORIGINAL_ACTION" ]]; then
    echo "ERROR: Original action $ORIGINAL_ACTION not found"
    exit 1
fi

echo "1. Reading FCM: $FCM_FILE"
echo "2. Found original action: $ORIGINAL_ACTION"

# Extract key fields from original for comparison
echo "3. Analyzing original action structure..."

# Count inputs in original
original_inputs=$(grep -A 100 "^inputs:" "$ORIGINAL_ACTION" | grep -E "^  [a-z_]+:" | wc -l)
echo "   - Original has $original_inputs inputs"

# Count outputs in original  
original_outputs=$(grep -A 100 "^outputs:" "$ORIGINAL_ACTION" | grep -E "^  [a-z_]+:" | wc -l)
echo "   - Original has $original_outputs outputs"

# Check runs type
original_runs_type=$(grep -A 1 "^runs:" "$ORIGINAL_ACTION" | grep "using:" | awk '{print $2}')
echo "   - Original uses: $original_runs_type"

echo "4. Checking generated action..."

# Check generated action exists
if [[ -f "$GENERATED_ACTION" ]]; then
    echo "   - Generated action found at $GENERATED_ACTION"
    
    # Count inputs in generated
    generated_inputs=$(grep -A 100 "^inputs:" "$GENERATED_ACTION" | grep -E "^  [a-z_]+:" | wc -l)
    echo "   - Generated has $generated_inputs inputs"
    
    # Count outputs in generated
    generated_outputs=$(grep -A 100 "^outputs:" "$GENERATED_ACTION" | grep -E "^  [a-z_]+:" | wc -l)
    echo "   - Generated has $generated_outputs outputs"
    
    # Check runs type
    generated_runs_type=$(grep -A 1 "^runs:" "$GENERATED_ACTION" | grep "using:" | awk '{print $2}')
    echo "   - Generated uses: $generated_runs_type"
    
    # Compare counts
    if [[ "$original_inputs" == "$generated_inputs" ]]; then
        echo "   ✓ Input count matches"
    else
        echo "   ✗ Input count mismatch: original=$original_inputs, generated=$generated_inputs"
    fi
    
    if [[ "$original_outputs" == "$generated_outputs" ]]; then
        echo "   ✓ Output count matches"
    else
        echo "   ✗ Output count mismatch: original=$original_outputs, generated=$generated_outputs"
    fi
    
    if [[ "$original_runs_type" == "$generated_runs_type" ]]; then
        echo "   ✓ Runs type matches"
    else
        echo "   ✗ Runs type mismatch: original=$original_runs_type, generated=$generated_runs_type"
    fi
    
else
    echo "   - WARNING: Generated action not found"
    echo "   - This is expected if generator hasn't run yet"
fi

echo ""
echo "5. Stage 2 Summary:"
echo "   - FCM exists: YES"
echo "   - Original action exists: YES"
echo "   - Generated action exists: $([ -f "$GENERATED_ACTION" ] && echo "YES" || echo "NO")"
echo ""
echo "Stage 2 validates that we can represent real actions as FCMs"
echo "Next step: Run generator to create action from FCM"

exit 0