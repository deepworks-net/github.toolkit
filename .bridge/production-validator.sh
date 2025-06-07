#!/bin/bash
# Production Bridge Validator
# Ensures all generated actions are valid and complete

set -e

echo "=== Production Bridge Validator ==="

errors=0
warnings=0

# Check all action directories
for action_dir in actions/core/* actions/composite/*; do
    if [[ -d "$action_dir" ]]; then
        action_name=$(basename "$action_dir")
        action_yml="$action_dir/action.yml"
        bridge_sync="$action_dir/.bridge-sync"
        
        echo "Validating: $action_name"
        
        # Check action.yml exists
        if [[ ! -f "$action_yml" ]]; then
            echo "  ✗ ERROR: Missing action.yml"
            ((errors++))
            continue
        fi
        
        # Check required fields
        if ! grep -q "^name:" "$action_yml"; then
            echo "  ✗ ERROR: Missing name field"
            ((errors++))
        fi
        
        if ! grep -q "^description:" "$action_yml"; then
            echo "  ✗ ERROR: Missing description field"
            ((errors++))
        fi
        
        if ! grep -q "^runs:" "$action_yml"; then
            echo "  ✗ ERROR: Missing runs section"
            ((errors++))
        fi
        
        # Check bridge sync
        if [[ ! -f "$bridge_sync" ]]; then
            echo "  ! WARNING: Missing .bridge-sync metadata"
            ((warnings++))
        else
            # Verify FCM source exists
            source_fcm=$(grep '"source_fcm"' "$bridge_sync" | cut -d'"' -f4)
            if [[ ! -f "$source_fcm" ]]; then
                echo "  ✗ ERROR: Source FCM missing: $source_fcm"
                ((errors++))
            fi
        fi
        
        # For docker actions, check Dockerfile
        if grep -q "using: docker" "$action_yml" && [[ ! -f "$action_dir/Dockerfile" ]]; then
            echo "  ✗ ERROR: Docker action missing Dockerfile"
            ((errors++))
        fi
        
        if [[ $errors -eq 0 ]] && [[ $warnings -eq 0 ]]; then
            echo "  ✓ Valid"
        fi
    fi
done

echo ""
echo "=== Validation Summary ==="
echo "Errors: $errors"
echo "Warnings: $warnings"

if [[ $errors -gt 0 ]]; then
    echo "FAILED: Fix errors before deploying to production"
    exit 1
else
    echo "PASSED: All actions are valid"
    exit 0
fi
