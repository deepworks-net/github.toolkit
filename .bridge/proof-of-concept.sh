#!/bin/bash
# Proof of Concept: FCM to Action Transform
# Stage 1: Minimal implementation using bash

# Generate minimal action.yml to stdout
cat << 'EOF'
name: Test Minimal
description: Test minimal bridge functionality
inputs:
  message:
    description: Message
    required: true
outputs:
  result:
    description: Result
runs:
  using: composite
  steps:
  - name: Test minimal action
    shell: bash
    run: echo "Message: ${{ inputs.message }}" >> $GITHUB_OUTPUT
EOF