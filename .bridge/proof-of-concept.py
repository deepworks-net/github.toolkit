#!/usr/bin/env python3
"""
Proof of Concept: FCM to Action Transform
Stage 1: Minimal implementation to prove the bridge concept works
"""

import sys
import yaml
from pathlib import Path

def read_minimal_fcm():
    """Read the minimal.fcm file and parse basic structure."""
    fcm_path = Path('axioms/test/minimal.fcm')
    
    fcm = {
        'name': 'Test Minimal',
        'description': 'Test minimal bridge functionality',
        'inputs': {
            'message': {
                'description': 'Message',
                'required': True
            }
        },
        'outputs': {
            'result': {
                'description': 'Result'
            }
        },
        'runs': {
            'using': 'composite',
            'steps': [
                {
                    'name': 'Test minimal action',
                    'shell': 'bash',
                    'run': 'echo "Message: ${{ inputs.message }}" >> $GITHUB_OUTPUT'
                }
            ]
        }
    }
    
    return fcm

def main():
    """Generate minimal action.yml and output to stdout."""
    fcm = read_minimal_fcm()
    
    # Output valid action.yml to stdout
    yaml.dump(fcm, sys.stdout, default_flow_style=False, sort_keys=False)

if __name__ == '__main__':
    main()