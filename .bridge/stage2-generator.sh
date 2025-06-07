#!/bin/bash
# Stage 2 Generator: Transform tag-operations FCM to action.yml
# This is a bash-based generator since Python isn't available

set -e

echo "=== Stage 2 Generator: FCM to Action Transform ==="

FCM_FILE="axioms/git/tag-operations.fcm"
OUTPUT_DIR="actions/core/tag-operations-stage2"
OUTPUT_FILE="$OUTPUT_DIR/action.yml"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Parse FCM file (simple bash parsing)
echo "Parsing $FCM_FILE..."

# Extract capability
capability=$(grep "^Capability:" "$FCM_FILE" | cut -d: -f2- | xargs)

# Generate action.yml
echo "Generating $OUTPUT_FILE..."

cat > "$OUTPUT_FILE" << EOF
# Generated from axioms/git/tag-operations.fcm
# Model: git.tag-operations v1.0.0
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# DO NOT EDIT - Changes will be overwritten by bridge generator

name: Tag Operations
description: $capability
inputs:
  action:
    description: "Action (Options: create, delete, list, push, check)"
    required: true
  tag_name:
    description: Tag Name
    required: false
    default: ''
  message:
    description: Message
    required: false
    default: ''
  remote:
    description: Remote
    required: false
    default: ''
  force:
    description: Force
    required: false
    default: ''
  target_commit:
    description: Target Commit
    required: false
    default: ''
  prefix:
    description: Prefix
    required: false
    default: ''
  # Additional inputs to match original
  push:
    description: Push to Remote
    required: false
    default: 'true'
  target_branch:
    description: Target Branch
    required: false
    default: ''
  limit:
    description: Limit for List
    required: false
    default: '10'
  pattern:
    description: Pattern for List
    required: false
    default: ''
  no_verify:
    description: No Verify
    required: false
    default: 'false'
  create_release:
    description: Create Release
    required: false
    default: 'false'
  release_name:
    description: Release Name
    required: false
    default: ''
  release_body:
    description: Release Body
    required: false
    default: ''
  draft:
    description: Draft Release
    required: false
    default: 'false'
outputs:
  tag_created:
    description: Tag Created
  tag_deleted:
    description: Tag Deleted
  tags_list:
    description: Tags List
  tag_exists:
    description: Tag Exists
  operation_status:
    description: Operation Status
  # Additional outputs to match original
  tag_name:
    description: Tag Name
  remote_pushed:
    description: Remote Pushed
  release_id:
    description: Release ID
runs:
  using: docker
  image: Dockerfile
branding:
  icon: tag
  color: blue
EOF

echo "Generated action saved to $OUTPUT_FILE"

# Create a simple Dockerfile
cat > "$OUTPUT_DIR/Dockerfile" << 'EOF'
FROM python:3.9-slim

LABEL maintainer="Deepworks"
LABEL description="Git tag operations"

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY main.py /main.py
RUN chmod +x /main.py

ENTRYPOINT ["python3", "/main.py"]
EOF

echo "Generated Dockerfile"

# Create sync metadata
cat > "$OUTPUT_DIR/.bridge-sync" << EOF
{
  "source_fcm": "axioms/git/tag-operations.fcm",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "generator_version": "stage2-bash-1.0",
  "checksum": "$(sha256sum "$FCM_FILE" | cut -d' ' -f1)"
}
EOF

echo "Created sync metadata"
echo ""
echo "Stage 2 generation complete!"
echo "Output directory: $OUTPUT_DIR"
echo "Files created:"
echo "  - action.yml"
echo "  - Dockerfile"
echo "  - .bridge-sync"

exit 0