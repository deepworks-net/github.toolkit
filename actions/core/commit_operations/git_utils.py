#!/usr/bin/env python3

# This module is now a proxy to the shared git_utils module
# Following the resonance-based modular architecture

import os
import sys

# Establish lateral relationship with shared git_utils
# Use the shared git_utils module
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'shared'))
sys.path.append(module_path)

try:
    from git_utils import GitConfig, GitValidator, GitErrors

    # Re-export the imported classes
    __all__ = ['GitConfig', 'GitValidator', 'GitErrors']
except ImportError:
    raise ImportError(
        "Could not import shared git_utils. Please ensure the shared module is available. "
        "This module now serves as a proxy to maintain lateral relationships between components."
    )