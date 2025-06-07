#!/bin/bash
# Stage 3 Scanner: Identify all actions that need FCMs

set -e

echo "=== Stage 3 Scanner: Action Inventory ==="

# Find all action.yml files
echo "Scanning for GitHub Actions..."
echo ""

# Arrays to track actions
declare -a core_actions
declare -a composite_actions
declare -a has_fcm
declare -a needs_fcm

# Scan core actions
echo "Core Actions:"
for action in actions/core/*/action.yml; do
    if [[ -f "$action" ]]; then
        dir=$(dirname "$action")
        name=$(basename "$dir")
        echo "  - $name"
        core_actions+=("$name")
        
        # Check if FCM exists
        fcm_name=$(echo "$name" | tr '_' '-')
        if [[ -f "axioms/git/${fcm_name}.fcm" ]] || [[ -f "axioms/github/${fcm_name}.fcm" ]] || [[ -f "axioms/version/${fcm_name}.fcm" ]]; then
            has_fcm+=("$name")
        else
            needs_fcm+=("$name")
        fi
    fi
done

echo ""
echo "Composite Actions:"
for action in actions/composite/*/action.yml; do
    if [[ -f "$action" ]]; then
        dir=$(dirname "$action")
        name=$(basename "$dir")
        echo "  - $name"
        composite_actions+=("$name")
        
        # Check if FCM exists
        fcm_name=$(echo "$name" | tr '_' '-')
        if [[ -f "axioms/release/${fcm_name}.fcm" ]] || [[ -f "axioms/workflow/${fcm_name}.fcm" ]]; then
            has_fcm+=("$name")
        else
            needs_fcm+=("$name")
        fi
    fi
done

echo ""
echo "=== Stage 3 Analysis ==="
echo "Total Core Actions: ${#core_actions[@]}"
echo "Total Composite Actions: ${#composite_actions[@]}"
echo "Actions with FCMs: ${#has_fcm[@]}"
echo "Actions needing FCMs: ${#needs_fcm[@]}"

echo ""
echo "Actions that need FCMs:"
for action in "${needs_fcm[@]}"; do
    echo "  - $action"
done

echo ""
echo "Next step: Create FCMs for the ${#needs_fcm[@]} remaining actions"

# Save inventory for Stage 3 generator
cat > .bridge/stage3-inventory.txt << EOF
# Stage 3 Action Inventory
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

CORE_ACTIONS:
$(printf '%s\n' "${core_actions[@]}")

COMPOSITE_ACTIONS:
$(printf '%s\n' "${composite_actions[@]}")

NEEDS_FCM:
$(printf '%s\n' "${needs_fcm[@]}")

HAS_FCM:
$(printf '%s\n' "${has_fcm[@]}")
EOF

echo ""
echo "Inventory saved to .bridge/stage3-inventory.txt"

exit 0