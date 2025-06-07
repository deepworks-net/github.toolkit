#!/bin/bash
# Bridge Test Script - Stage 1: Minimal Proof
# Tests that FCM→Action transform works

set -e

echo "=== Bridge Stage 1 Test ==="

# Check if proof-of-concept exists
if [[ ! -f .bridge/proof-of-concept.sh ]]; then
    echo "ERROR: proof-of-concept.sh not found"
    exit 1
fi

# Check if minimal.fcm exists
if [[ ! -f axioms/test/minimal.fcm ]]; then
    echo "ERROR: minimal.fcm not found"
    exit 1
fi

echo "Running proof-of-concept.sh..."

# Run the proof of concept and capture output
output=$(.bridge/proof-of-concept.sh 2>&1)
exit_code=$?

if [[ $exit_code -ne 0 ]]; then
    echo "ERROR: proof-of-concept.sh failed with exit code $exit_code"
    echo "Output: $output"
    exit 1
fi

# Check for required GitHub Action structure
echo "$output" | grep -q "name:" || { echo "ERROR: Missing 'name' field"; exit 1; }
echo "$output" | grep -q "description:" || { echo "ERROR: Missing 'description' field"; exit 1; }
echo "$output" | grep -q "inputs:" || { echo "ERROR: Missing 'inputs' field"; exit 1; }
echo "$output" | grep -q "outputs:" || { echo "ERROR: Missing 'outputs' field"; exit 1; }
echo "$output" | grep -q "runs:" || { echo "ERROR: Missing 'runs' field"; exit 1; }

echo "SUCCESS: Bridge Stage 1 Test PASSED"
echo "SUCCESS: FCM to Action transform works!"
echo ""
echo "Generated action.yml:"
echo "$output"

exit 0