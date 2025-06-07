#!/bin/bash
# Stage 3 Generator: Transform all FCMs to Actions

set -e

echo "=== Stage 3 Generator: Full Integration ==="

# Function to transform FCM to action
generate_action() {
    local fcm_file=$1
    local output_dir=$2
    local action_name=$3
    
    echo "Generating action from $fcm_file..."
    
    # Extract metadata from FCM
    local capability=$(grep "^Capability:" "$fcm_file" | cut -d: -f2- | xargs)
    local model=$(grep "^Model:" "$fcm_file" | cut -d: -f2 | xargs)
    local version=$(grep "^Version:" "$fcm_file" | cut -d: -f2 | xargs)
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # Generate action.yml header
    cat > "$output_dir/action.yml" << EOF
# Generated from $fcm_file
# Model: $model v$version
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# DO NOT EDIT - Changes will be overwritten by bridge generator

name: '$action_name'
description: '$capability'
EOF

    # Parse and add inputs
    echo "inputs:" >> "$output_dir/action.yml"
    
    # Extract parameters from FCM (simplified parsing)
    in_params=false
    while IFS= read -r line; do
        if [[ "$line" == "Parameters:" ]]; then
            in_params=true
            continue
        elif [[ "$line" == "Outputs:" ]]; then
            in_params=false
            break
        elif [[ $in_params == true ]] && [[ "$line" =~ ^[[:space:]]*-[[:space:]]([a-z_]+): ]]; then
            param_line=$(echo "$line" | sed 's/^[[:space:]]*-[[:space:]]//')
            param_name=$(echo "$param_line" | cut -d: -f1 | xargs)
            param_rest=$(echo "$param_line" | cut -d: -f2- | xargs)
            
            # Check if optional
            required="true"
            if [[ "$param_rest" == *"(optional)"* ]]; then
                required="false"
            fi
            
            # Handle enum types
            if [[ "$param_rest" == *"|"* ]]; then
                enum_values=$(echo "$param_rest" | cut -d' ' -f1)
                echo "  $param_name:" >> "$output_dir/action.yml"
                echo "    description: \"$(echo $param_name | tr '_' ' ' | sed 's/\b\(.\)/\u\1/g') (Options: $enum_values)\"" >> "$output_dir/action.yml"
            else
                echo "  $param_name:" >> "$output_dir/action.yml"
                echo "    description: '$(echo $param_name | tr '_' ' ' | sed 's/\b\(.\)/\u\1/g')'" >> "$output_dir/action.yml"
            fi
            
            echo "    required: $required" >> "$output_dir/action.yml"
            if [[ "$required" == "false" ]]; then
                echo "    default: ''" >> "$output_dir/action.yml"
            fi
        fi
    done < "$fcm_file"
    
    # Parse and add outputs
    echo "outputs:" >> "$output_dir/action.yml"
    
    in_outputs=false
    while IFS= read -r line; do
        if [[ "$line" == "Outputs:" ]]; then
            in_outputs=true
            continue
        elif [[ "$line" == "Interface:" ]]; then
            in_outputs=false
            break
        elif [[ $in_outputs == true ]] && [[ "$line" =~ ^[[:space:]]*-[[:space:]]([a-z_]+) ]]; then
            output_name=$(echo "$line" | sed 's/^[[:space:]]*-[[:space:]]//' | xargs)
            echo "  $output_name:" >> "$output_dir/action.yml"
            echo "    description: '$(echo $output_name | tr '_' ' ' | sed 's/\b\(.\)/\u\1/g')'" >> "$output_dir/action.yml"
        fi
    done < "$fcm_file"
    
    # Add runs section
    echo "runs:" >> "$output_dir/action.yml"
    echo "  using: docker" >> "$output_dir/action.yml"
    echo "  image: Dockerfile" >> "$output_dir/action.yml"
    
    # Add branding
    echo "branding:" >> "$output_dir/action.yml"
    echo "  icon: 'git-branch'" >> "$output_dir/action.yml"
    echo "  color: 'blue'" >> "$output_dir/action.yml"
    
    # Generate Dockerfile
    cat > "$output_dir/Dockerfile" << 'DOCKERFILE'
FROM python:3.9-slim

LABEL maintainer="Deepworks"
LABEL description="Generated from FCM"

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY main.py /main.py
RUN chmod +x /main.py

ENTRYPOINT ["python3", "/main.py"]
DOCKERFILE

    # Create sync metadata
    cat > "$output_dir/.bridge-sync" << EOF
{
  "source_fcm": "$fcm_file",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "generator_version": "stage3-bash-1.0",
  "model": "$model",
  "version": "$version"
}
EOF

    echo "  ✓ Generated $output_dir"
}

# Process all FCMs
echo "Processing FCMs..."
echo ""

# Git domain FCMs
for fcm in axioms/git/*.fcm; do
    if [[ -f "$fcm" ]]; then
        basename=$(basename "$fcm" .fcm)
        action_name=$(echo "$basename" | tr '-' '_')
        pretty_name=$(echo "$basename" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
        output_dir="actions/core/${basename}-generated"
        generate_action "$fcm" "$output_dir" "$pretty_name"
    fi
done

# Generate summary
total_fcms=$(find axioms -name "*.fcm" | wc -l)
generated_actions=$(find actions -name ".bridge-sync" | wc -l)

echo ""
echo "=== Stage 3 Summary ==="
echo "Total FCMs found: $total_fcms"
echo "Actions generated: $generated_actions"
echo ""
echo "Stage 3 demonstrates full FCM-to-Action generation capability"
echo "Next: Validate generated actions pass existing tests"

exit 0