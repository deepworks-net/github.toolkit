#!/bin/bash
# Bridge Alignment Validator (Shell version)

echo "=== Bridge Alignment Validation ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

VALID=true
CHECKS=0
PASSED=0

# Check 1: Verify all FCMs have corresponding actions
echo "Checking FCM coverage..."
FCM_COUNT=0
MISSING_ACTIONS=""
for fcm in axioms/*/*.fcm; do
    if [ -f "$fcm" ]; then
        FCM_COUNT=$((FCM_COUNT + 1))
        # Extract action name from FCM
        MODEL=$(grep "^Model:" "$fcm" | cut -d: -f2- | tr -d ' ')
        ACTION_NAME=$(echo "$MODEL" | rev | cut -d. -f1 | rev | tr _ -)
        
        if [ ! -d "actions/core/$ACTION_NAME" ]; then
            MISSING_ACTIONS="$MISSING_ACTIONS $fcm"
            VALID=false
        fi
    fi
done
CHECKS=$((CHECKS + 1))
if [ -z "$MISSING_ACTIONS" ]; then
    echo "  ✓ FCM Coverage: All $FCM_COUNT FCMs have generated actions"
    PASSED=$((PASSED + 1))
else
    echo "  ✗ FCM Coverage: Missing actions for:$MISSING_ACTIONS"
fi

# Check 2: Verify all generated actions have sync files
echo "Checking sync files..."
ACTION_COUNT=0
MISSING_SYNC=""
for action_dir in actions/core/*/; do
    if [ -d "$action_dir" ]; then
        ACTION_COUNT=$((ACTION_COUNT + 1))
        if [ ! -f "$action_dir/.bridge-sync" ]; then
            MISSING_SYNC="$MISSING_SYNC $action_dir"
            VALID=false
        fi
    fi
done
CHECKS=$((CHECKS + 1))
if [ -z "$MISSING_SYNC" ]; then
    echo "  ✓ Sync Files: All $ACTION_COUNT actions have sync files"
    PASSED=$((PASSED + 1))
else
    echo "  ✗ Sync Files: Missing sync files in:$MISSING_SYNC"
fi

# Check 3: Verify generation headers
echo "Checking for manual edits..."
MANUAL_EDITS=""
for action_yml in actions/core/*/action.yml; do
    if [ -f "$action_yml" ]; then
        if ! grep -q "# Generated from" "$action_yml"; then
            MANUAL_EDITS="$MANUAL_EDITS $action_yml"
            VALID=false
        elif ! grep -q "# DO NOT EDIT" "$action_yml"; then
            MANUAL_EDITS="$MANUAL_EDITS $action_yml"
            VALID=false
        fi
    fi
done
CHECKS=$((CHECKS + 1))
if [ -z "$MANUAL_EDITS" ]; then
    echo "  ✓ Manual Edit Detection: No manual edits detected"
    PASSED=$((PASSED + 1))
else
    echo "  ✗ Manual Edit Detection: Possible manual edits in:$MANUAL_EDITS"
fi

# Check 4: Verify GitHub compatibility
echo "Checking GitHub compatibility..."
COMPAT_ISSUES=""
for action_yml in actions/core/*/action.yml; do
    if [ -f "$action_yml" ]; then
        # Check for required fields
        if ! grep -q "^name:" "$action_yml"; then
            COMPAT_ISSUES="$COMPAT_ISSUES $action_yml:missing-name"
        fi
        if ! grep -q "^runs:" "$action_yml"; then
            COMPAT_ISSUES="$COMPAT_ISSUES $action_yml:missing-runs"
        fi
    fi
done
CHECKS=$((CHECKS + 1))
if [ -z "$COMPAT_ISSUES" ]; then
    echo "  ✓ GitHub Compatibility: All actions are GitHub-compatible"
    PASSED=$((PASSED + 1))
else
    echo "  ✗ GitHub Compatibility: Issues found:$COMPAT_ISSUES"
fi

# Summary
echo ""
echo "Summary:"
echo "  Total Checks: $CHECKS"
echo "  Passed: $PASSED"
echo "  Failed: $((CHECKS - PASSED))"
echo ""

if [ "$VALID" = true ]; then
    echo "Overall Status: VALID"
    exit 0
else
    echo "Overall Status: INVALID"
    exit 1
fi