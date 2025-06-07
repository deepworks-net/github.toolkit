#!/bin/bash
# Production FCM-to-Action Generator
# Automatically generates all actions from FCMs

set -e

echo "=== Production Bridge Generator ==="

# Function to parse FCM and generate action
generate_from_fcm() {
    local fcm_path=$1
    local domain=$2
    local action_name=$3
    
    echo "Processing: $fcm_path"
    
    # Determine output path based on domain
    local output_dir
    case $domain in
        git|github)
            output_dir="actions/core/$action_name"
            ;;
        release|workflow)
            output_dir="actions/composite/$action_name"
            ;;
        version)
            output_dir="actions/core/$action_name"
            ;;
        *)
            output_dir="actions/misc/$action_name"
            ;;
    esac
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # Extract metadata
    local model=$(grep "^Model:" "$fcm_path" | cut -d: -f2 | xargs)
    local version=$(grep "^Version:" "$fcm_path" | cut -d: -f2 | xargs)
    local capability=$(grep "^Capability:" "$fcm_path" | cut -d: -f2- | xargs)
    local interface_type=$(grep -A1 "^Interface:" "$fcm_path" | grep "type:" | cut -d: -f2 | xargs)
    
    # Generate action.yml with production header
    cat > "$output_dir/action.yml" << EOF
# GENERATED FILE - DO NOT EDIT
# Source: $fcm_path
# Model: $model v$version
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# 
# To modify this action:
# 1. Edit the source FCM at $fcm_path
# 2. Run: make generate-actions
# 3. Commit both FCM and generated files

name: $(echo "$action_name" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
description: $capability
author: 'Deepworks (via FCM Bridge)'

EOF

    # Add inputs section
    echo "inputs:" >> "$output_dir/action.yml"
    
    # Parse parameters with improved logic
    awk '/^Parameters:/{flag=1; next} /^Outputs:/{flag=0} flag && /^[[:space:]]*-/ {
        gsub(/^[[:space:]]*-[[:space:]]/, "")
        split($0, parts, ":")
        param_name = parts[1]
        param_rest = substr($0, index($0, ":")+1)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", param_name)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", param_rest)
        
        print "  " param_name ":"
        
        # Handle description
        desc = param_name
        gsub(/_/, " ", desc)
        desc = toupper(substr(desc, 1, 1)) substr(desc, 2)
        
        # Check for enum values
        if (match(param_rest, /\|/)) {
            split(param_rest, options, " ")
            print "    description: \"" desc " (Options: " options[1] ")\""
        } else {
            print "    description: " desc
        }
        
        # Check if optional
        if (match(param_rest, /\(optional\)/)) {
            print "    required: false"
            print "    default: \"\""
        } else {
            print "    required: true"
        }
    }' "$fcm_path" >> "$output_dir/action.yml"
    
    # Add outputs section
    echo "outputs:" >> "$output_dir/action.yml"
    
    # Parse outputs
    awk '/^Outputs:/{flag=1; next} /^Interface:/{flag=0} flag && /^[[:space:]]*-/ {
        gsub(/^[[:space:]]*-[[:space:]]/, "")
        output_name = $0
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", output_name)
        
        print "  " output_name ":"
        
        desc = output_name
        gsub(/_/, " ", desc)
        desc = toupper(substr(desc, 1, 1)) substr(desc, 2)
        print "    description: " desc
    }' "$fcm_path" >> "$output_dir/action.yml"
    
    # Add runs section based on interface type
    if [[ "$interface_type" == "composite" ]]; then
        cat >> "$output_dir/action.yml" << EOF
runs:
  using: composite
  steps:
    - name: Execute $action_name
      shell: bash
      run: |
        echo "Executing $action_name"
        echo "This is a generated composite action"
        # Implementation would go here
EOF
    else
        cat >> "$output_dir/action.yml" << EOF
runs:
  using: docker
  image: Dockerfile
  
branding:
  icon: 'code'
  color: 'blue'
EOF
        
        # Generate Dockerfile for docker actions
        cat > "$output_dir/Dockerfile" << 'DOCKERFILE'
FROM python:3.9-slim

LABEL maintainer="Deepworks"
LABEL description="Generated from FCM"

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy implementation
COPY main.py /main.py
RUN chmod +x /main.py

ENTRYPOINT ["python3", "/main.py"]
DOCKERFILE
    fi
    
    # Create bridge metadata
    cat > "$output_dir/.bridge-sync" << EOF
{
  "source_fcm": "$fcm_path",
  "model": "$model",
  "version": "$version",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "generator_version": "production-1.0.0",
  "checksum": "$(sha256sum "$fcm_path" | cut -d' ' -f1)"
}
EOF

    echo "  ✓ Generated: $output_dir"
}

# Main generation loop
echo "Scanning for FCMs..."

# Process all FCM files
for fcm in axioms/*/*.fcm; do
    if [[ -f "$fcm" ]]; then
        domain=$(basename $(dirname "$fcm"))
        basename=$(basename "$fcm" .fcm)
        generate_from_fcm "$fcm" "$domain" "$basename"
    fi
done

echo ""
echo "Generation complete!"
echo "Run 'make validate-bridge' to verify all actions"
